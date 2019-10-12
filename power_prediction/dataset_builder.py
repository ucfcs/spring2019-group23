# Builds a dataframe into a neat format (newest)

# from datetime import timezone, datetime, timedelta
import numpy as np
import pandas as pd

wthr_cols = ['date', 'battery_volt', 'DASTemp', 'RC11_F_180deg_Avg', 'Apogee_180deg_Avg', 'Apogee_180deg_Max',
             'Apogee_180deg_TMx', 'PSP1_Irrad_Avg', 'TUVR1_Irrad_Avg', 'Ambient_Temp1_Avg', 'Ambient_RH1_Avg',
             'Ambient_PRESSURE', 'WIND1_Speed_Avg', 'WIND1_Direction', 'RAIN_mm_Tot', 'T_Soil_Avg', 'VWC_Avg',
             'EC_Avg', 'PIRnet_Avg']

pwr_cols  = ['date', 'SA_WS1_POA', 'SA_Prod1_kWac', 'SA_Prod2_kWac', 'SA_Prod3_kWac', 'SA_Prod4_kWac']

# Read in the file as a Pandas DataFrame
df1 = pd.read_csv('data/rubin-weather-edit.csv', sep=',', names=wthr_cols, skiprows=4, low_memory=False)
df2 = pd.read_csv('data/UCF_SA_POA_mtrs.csv', sep=',', names=pwr_cols, skiprows=1, low_memory=False)

# Get rid of any row that contains an NaN
df1.dropna()
df2.dropna()

# Actually convert the data type and add the UTC timezone
df1.date = pd.to_datetime(df1.date, format='%m/%d/%Y %H:%M')
df2.date = pd.to_datetime(df2.date, format='%m/%d/%Y %H:%M')

# Merge the datasets into one large dataset where the dates match
res = pd.merge(df1, df2, on='date')

# Drop some (potentially?) unnecessary columns
res = res.drop(['RC11_F_180deg_Avg', 'Apogee_180deg_Avg', 'Apogee_180deg_Max', 'Apogee_180deg_TMx', 'T_Soil_Avg',
                'VWC_Avg', 'EC_Avg', 'PIRnet_Avg', 'SA_Prod1_kWac', 'SA_Prod2_kWac', 'SA_Prod3_kWac',
                'SA_Prod4_kWac'], axis=1)

res = res.dropna()

# Change the temperature to Celcius and round some stuff to make the csv look better
res = round(res, 2)

# Export the new dataframe
res.to_csv(path_or_buf='data/final-dataset.csv', index=False, sep=',')


# Some weird thing that turned out to be useless. I didn't want to delete it so I moved it to the bottom and
# commented it out
# wthr_dtype = {'date'              : np.object_,  'batter_volt'       : np.float32, 'DASTemp'           : np.float32,
#               'RC11_F_180deg_Avg' : np.float32,  'Apogee_180deg_Avg' : np.float32, 'Apogee_180deg_Max' : np.float32,
#               'Apogee_180deg_TMx' : np.float32,  'PSP1_Irrad_Avg'    : np.float32, 'TUVR1_Irrad_Avg'   : np.float32,
#               'Ambient_Temp1_Avg' : np.float32,  'Ambient_RH1_Avg'   : np.float32, 'Ambient_PRESSURE'  : np.float32,
#               'WIND1_Speed_Avg'   : np.float32,  'WIND1_Direction'   : np.float32, 'RAIN_mm_Tot'       : np.float32,
#               'T_Soil_Avg'        : np.float32,  'VWC_Avg'           : np.float32, 'EC_Avg'            : np.float32,
#               'PIRnet_Avg'        : np.float32}

# pwr_dtype = {'date'               : np.object_,  'SA_WS1_POA'        : np.float32, 'SA_Prod1_kWac'     : np.float32,
#              'SA_Prod2_kWac'      : np.float32,  'SA_Prod3_kWac'     : np.float32, 'SA_Prod4_kWac'     : np.float32}
