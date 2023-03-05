from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import requests
import sqlite3

app = Flask(__name__)

# Define the endpoint
@app.route('/spwx-data', methods=['GET'])
def get_spwx_data():
    # Get the start and end times from the query strings
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Convert the start and end times to datetime objects
    start_time_dt = datetime.fromisoformat(start_time)
    end_time_dt = datetime.fromisoformat(end_time)

    # Check if the start_time is more than 24 hours ago
    if start_time_dt < datetime.now() - timedelta(hours=24):
            return jsonify({'warning': 'Start time is more than 24 hours ago. This dataset is only populated for the last 24 hours.'})

    # Check if the provided window is greater than 1 hour
    if end_time_dt - start_time_dt > timedelta(hours=1):
        return jsonify({'warning': 'Start and end times are more than 1 hour apart.'})

    # Download the JSON data
    json_url = 'https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json'
    response = requests.get(json_url)
    data = response.json()

    # Get the column names
    keys = list(data[0].keys())
    column_names = ', '.join(keys)
    
    # Get the number of columns and form into string for SQL query
    column_values = '?, ' * len(keys)
    column_values = column_values[:-2]

    # Create a SQLite3 database
    conn = sqlite3.connect('spwx_data.db')
    cursor = conn.cursor()

    # Create a table to store the spwx data
    cursor.execute(f'CREATE TABLE IF NOT EXISTS spwx_data({column_names} REAL)')

    # Insert the data into the table
    for item in data:
        values = [item[key] for key in keys]
        cursor.execute(f'INSERT INTO spwx_data ({column_names}) VALUES ({column_values})', values)
    conn.commit()

    # Query the data from the table
    cursor.execute(f'''
        SELECT strftime('%Y-%m-%d %H:', time_tag) || CAST((strftime('%M', time_tag) / 5) * 5 AS TEXT) || ':00' AS time_period,
        {', '.join([f'AVG({col}) AS {col}_avg' for col in keys if col != 'time_tag'])}
        FROM spwx_data
        WHERE time_tag BETWEEN ? AND ?
        GROUP BY time_period
    ''', (start_time, end_time))
    rows = cursor.fetchall()
    
    # Convert the rows to a list of dictionaries
    results = []
    for row in rows:
        result = {}
        for i in range(len(keys)):
            result[keys[i]] = row[i]
        results.append(result)
    # Close the database connection
    conn.close()

    # Return the results as JSON
    return jsonify(results)
