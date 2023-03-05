# Importing necessary modules
import requests, argparse
import pandas as pd
import matplotlib.pyplot as plt

# Setting the URL for the JSON data
url = 'https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json'

# Creating an argument parser to allow for command line input
parser = argparse.ArgumentParser()
parser.add_argument("--channel", default="P1", help="Enter Channel Name. Defaults to P1")
parser.add_argument("--url", default=url, help="Enter URL to JSON data")
args = parser.parse_args()

# Defining a class called "rollingAverage"
class rollingAverage:
    def __init__(self, url, channel):
        self.url = url
        self.channel = channel
    # Method to plot the rolling average of the JSON data
    def plotRA(self):
        
        # Making a request to the API to get the JSON data
        r = requests.get(self.url, allow_redirects=True)
        
        # Saving the JSON data to a file
        open('differential-protons-1-day.json', 'wb').write(r.content)
        
        # Reading the JSON data into a pandas dataframe
        df = pd.read_json('differential-protons-1-day.json')
        
        # Filtering the dataframe to only include data for the specified channel
        channel_p1 = df.loc[df['channel'] == self.channel]
        
        # Adding a new column to the dataframe that contains the moving average for flux
        channel_p1['Moving_Average'] = df['flux'].rolling(window=20).mean()

        # Plotting the moving average data
        plt.plot(channel_p1['Moving_Average'],label= 'Moving_Average')
        plt.legend(loc='best')
        plt.title('Flux Values for ' + self.channel)
        plt.show()

# Creating an instance of the rollingAverage class with the specified arguments
output = rollingAverage(args.url, args.channel)

# Calling the plotRA method to plot the rolling average of the JSON data
output.plotRA()
