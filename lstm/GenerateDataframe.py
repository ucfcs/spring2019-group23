from datetime import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys

weather_cols  = ['temperature', 'humidity', 'wind_speed', 'wind_gust', 'daily_rain', 'monthly_rain', 'yearly_rain', 'uv_0_11', 'date']
ouc_cols = ['date', 'power_output']

# Read in the file as a Pandas DataFrame
wtr = pd.read_csv('data/weather-trends.csv', sep=';', names=weather_cols, skiprows=1)
ouc = pd.read_csv('data/solar-output201804.csv', sep=',', names=ouc_cols, skiprows=1)

# Convert the time to a proper datetime format (Those unpadded zeroes are a bitch to deal with)
for i, row in ouc.iterrows():
    ouc.loc[i, 'date'] = dt.strptime(row['date'], "%m/%d/%Y %H:%M")

# Actually convert the data type
ouc.date = pd.to_datetime(ouc.date, format='%Y-%m-%d %H:%M:%S')

print(ouc)
print(ouc.dtypes)
