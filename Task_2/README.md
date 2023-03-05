# Task 2
Data handling and basic visualisation test:
Download json GOES 16 proton data at runtime from services.swpc.noaa.gov
https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json
Put into Pandas Dataframe
Plot a 20 minute moving average against the raw inputs for p1

Requires:

- Python 3.9+

## Setup:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Running Task

To run with the default URL for the data, and to filter the data by the default channel (P1)
run the python script with no arguments passed.
```bash
python3 dataframe.py
```

To execute with an alternative URL or channel, run as follows
```bash
python3 dataframe.py --url <URL> --channel <channel>
```
