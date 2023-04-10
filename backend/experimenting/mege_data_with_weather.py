import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from google.colab import drive
drive.mount('/content/drive')
path = '/content/drive/MyDrive/DSA3101_Share/'

dtypes = {
    'Year': np.int16,
    'Month': np.int16,
    'DayofMonth': np.int16,
    'DayOfWeek': np.int16,
    'DepTime': np.float16,
    'CRSDepTime': np.int16,
    'ArrTime': np.float16,
    'CRSArrTime': np.int16,
    'UniqueCarrier': 'object',
    'FlightNum': np.int16,
    'TailNum': 'object',
    'ActualElapsedTime': np.float16,
    'CRSElapsedTime': np.float16,
    'AirTime': np.float16,
    'ArrDelay': np.float16,
    'DepDelay': np.float16,
    'Origin': 'object',
    'Dest': 'object',
    'Distance': np.int16,
    'TaxiIn': np.float16,
    'TaxiOut': np.float16,
    'Cancelled': np.int16,
    'CancellationCode': 'object',
    'Diverted': np.int16,
    'CarrierDelay': np.float16,
    'WeatherDelay': np.float16,
    'NASDelay': np.float16,
    'SecurityDelay': np.float16,
    'LateAircraftDelay': np.float16
}

data_2006 = pd.read_csv(path+"2006.csv",dtype=dtypes)
data_2007 = pd.read_csv(path+"2007.csv",dtype=dtypes)
weather_2006_2007 = pd.read_csv(path+"2006_2007_US_weather_by_state.csv",dtype=dtypes)
weather_2006_2007['name'].unique()

state_abbr = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY', 'Washington D.C.': 'DC'
}

# Use the map() function to replace the full state names with their abbreviations
weather_2006_2007['name'] = weather_2006_2007['name'].map(state_abbr)

# Find the NaN value in the 'name' column
nan_value = weather_2006_2007['name'].isna().any()

# Print the result
print(nan_value)

date_cols = ['Year', 'Month', 'DayofMonth']
data_2006[date_cols] = data_2006[date_cols].astype(str)

# Rename the columns
data_renamed = data_2006[date_cols].rename(columns={'Year': 'year', 'Month': 'month', 'DayofMonth': 'day'})

# Convert the renamed DataFrame to datetime
data_2006['datetime'] = pd.to_datetime(data_renamed, format='%Y-%m-%d')
data_2006.head()

date_cols = ['Year', 'Month', 'DayofMonth']
data_2007[date_cols] = data_2007[date_cols].astype(str)

# Rename the columns
data_renamed = data_2007[date_cols].rename(columns={'Year': 'year', 'Month': 'month', 'DayofMonth': 'day'})

# Convert the renamed DataFrame to datetime
data_2007['datetime'] = pd.to_datetime(data_renamed, format='%Y-%m-%d')
data_2007.head()

coordinates = pd.read_csv(path+'2011_february_us_airport_traffic.csv')

airport_state = coordinates.loc[:,['iata','state']]
airport_state = airport_state.rename(columns={'iata':'Origin'})

data_2006 = data_2006.merge(airport_state[['Origin', 'state']], on='Origin', how='left')
data_2006 = data_2006.rename(columns={'state': 'origin_state'})
data_2006.head()

data_2007 = data_2007.merge(airport_state[['Origin', 'state']], on='Origin', how='left')
data_2007 = data_2007.rename(columns={'state': 'origin_state'})
data_2007.head()

data_2006['datetime'] = pd.to_datetime(data_2006['datetime']).dt.strftime('%Y-%m-%d')
data_2007['datetime'] = pd.to_datetime(data_2007['datetime']).dt.strftime('%Y-%m-%d')
weather_2006_2007 = weather_2006_2007.rename(columns={'name':'origin_state'})
merged_data_2006 = data_2006.merge(weather_2006_2007, on=['datetime', 'origin_state'], how='left')
merged_data_2007 = data_2007.merge(weather_2006_2007, on=['datetime', 'origin_state'], how='left')

file_name = '2006_with_weather.csv'
merged_data_2006.to_csv(path + file_name, index=False)

file_name = '2007_with_weather.csv'
merged_data_2007.to_csv(path + file_name, index=False)