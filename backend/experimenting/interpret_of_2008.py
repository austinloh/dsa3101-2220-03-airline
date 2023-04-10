import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

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

data = pd.read_csv("../2008.csv", dtype = dtypes)
weather_df = pd.read_csv("../States Climate weather data 2008.csv")
weather_df['name'].unique()
# Define a dictionary mapping state names to abbreviations
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
weather_df['name'] = weather_df['name'].map(state_abbr)

# Find the NaN value in the 'name' column
nan_value = weather_df['name'].isna().any()

# Print the result
print(nan_value)

date_cols = ['Year', 'Month', 'DayofMonth']
data[date_cols] = data[date_cols].astype(str)

# Rename the columns
data_renamed = data[date_cols].rename(columns={'Year': 'year', 'Month': 'month', 'DayofMonth': 'day'})

# Convert the renamed DataFrame to datetime
data['datetime'] = pd.to_datetime(data_renamed, format='%Y-%m-%d')
data.head()

coordinates = pd.read_csv('../2011_february_us_airport_traffic.csv')
airport_state = coordinates.loc[:,['iata','state']]
airport_state = airport_state.rename(columns={'iata':'Origin'})
data = data.merge(airport_state[['Origin', 'state']], on='Origin', how='left')
data = data.rename(columns={'state': 'origin_state'})
data.head()

data['datetime'] = pd.to_datetime(data['datetime']).dt.strftime('%Y-%m-%d')
weather_df = weather_df.rename(columns={'name':'origin_state'})
merged_data = data.merge(weather_df, on=['datetime', 'origin_state'], how='left')

# Check the result
merged_data.head()
merged_data.shape[0]