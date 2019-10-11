from datetime import datetime as dt
import pandas as pd
import dateutil.parser
import datetime
from pytz import utc

wtr_cols = ['temperature', 'humidity', 'wind_speed', 'wind_gust', 'daily_rain', 'monthly_rain', 'yearly_rain', 'uv_0_11', 'date']
ouc_cols = ['date', 'power_output']

# Read in the file as a Pandas DataFrame
wtr = pd.read_csv('data/sanitized-weather-trends.csv', sep='\t', names=wtr_cols, skiprows=1)
ouc = pd.read_csv('data/sanitized-solar-output-2018-08.csv', sep='\t', names=ouc_cols, skiprows=1)

# Convert the data type, set utc to true to set them to the same timezone
wtr.date = pd.to_datetime(wtr.date, utc=True)
ouc.date = pd.to_datetime(ouc.date, utc=True)

# Sort by date
ouc = ouc.sort_values(by='date')
wtr = wtr.sort_values(by='date')

fil_wtr = wtr[(wtr.date.dt.month == 8) & (wtr.date.dt.year == 2018)]
res = pd.merge(fil_wtr, ouc, on='date')

print(res)