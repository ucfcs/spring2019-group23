# This is old code that I don't want to delete yet
# Could be useful in the future

from datetime import timezone, datetime, timedelta
import pandas as pd

power_cols = ['date', 'pwr_out']
irdnc_cols = ['date', 'irdnc']
wther_cols = ['date_unix', 'date', 'city_id', 'city_name', 'lat', 'lon', 'temp', 'temp_min', 'temp_max',   \
              'prsure', 'sea_level', 'grnd_level', 'hmdty', 'wnd_spd', 'wnd_deg', 'rain_1h',      \
              'rain_3h', 'rain_24h', 'rain_today', 'snow_1h', 'snow_3h', 'snow_24h', 'snow_today',         \
              'clouds', 'weather_id', 'weather_main', 'weather_description', 'weather_icon']

# Read in the file as a Pandas DataFrame
df1 = pd.read_csv('data/panel-output-2018.csv', sep=',', names=power_cols, skiprows=1)
df2 = pd.read_csv('data/irradiance-2018.csv', sep=',', names=irdnc_cols, skiprows=1)
df3 = pd.read_csv('data/weather-history-2018.csv', sep=',', names=wther_cols, skiprows=1)

# Get rid of a lot of the useless columns
df3 = df3.drop(['date_unix', 'city_id', 'city_name', 'lat', 'lon', 'temp_min', 'temp_max', 'sea_level',    \
                'grnd_level', 'rain_3h', 'rain_24h', 'rain_today', 'snow_1h', 'snow_3h', 'snow_24h',       \
                'snow_today', 'weather_id', 'weather_main', 'weather_description', 'weather_icon'], axis=1)

# Get rid of the NaN's
df3 = df3.fillna(0)

# Actually convert the data type and add the UTC timezone
df1.date = pd.to_datetime(df1.date, format='%m/%d/%Y %H:%M')
df1.date = df1.date - timedelta(hours=5)

df2.date = pd.to_datetime(df2.date, format='%m/%d/%Y %H:%M')

# Get rid of the timezone
df3.date = pd.to_datetime(df3.date, format='%Y-%m-%d %H:%M:%S %z UTC')
df3.date = df3.date.dt.tz_localize(None)

# Merge the datasets into one large dataset where the dates match
res = pd.merge(df1, df2, on='date')
# res = pd.merge(res, df3, on='date')

# Change the temperature to Celcius and round some stuff to make the csv look better
# res.temp = res.temp - 273.15
res = round(res, 2)

# Drop the date because it may be unnecessary?
res = res.drop('date', axis=1)

# Export the new dataframe
res.to_csv(path_or_buf='data/power-irradiance.csv', index=False, sep=',')