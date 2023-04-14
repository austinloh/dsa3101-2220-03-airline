from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
path = '/content/drive/MyDrive/DSA3101_Share/'

df = pd.read_csv(path+'2006_to_2008_preprocessed.csv')

df.drop(['solarradiation','solarenergy','uvindex','severerisk','sunrise','sunset'], axis=1, inplace=True)
df.drop(['precipprob','preciptype','icon'],axis=1, inplace=True)

for col in df.select_dtypes(include=['object']):
    df[col] = df[col].astype('category')

# Replace missing categorical (factor) values with 'unknown'
for col in df.select_dtypes(include=['category']):
    df[col] = df[col].cat.add_categories(['unknown'])
    df[col].fillna('unknown', inplace=True)

# Replace missing numeric values with mean of that column
for col in df.select_dtypes(include=[np.number]):
    mean_val = df[col].mean()
    df[col].fillna(mean_val, inplace=True)

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
weather_df = df[['temp', 'feelslike', 'dew', 'humidity', 'precip', 'snow', 'snowdepth', 'windgust', 'windspeed', 'winddir', 'sealevelpressure', 'cloudcover', 'visibility', 'moonphase']]
weather_df = (weather_df - weather_df.mean()) / weather_df.std()
pca = PCA()
weather_pca = pca.fit_transform(weather_df)
plt.plot(range(1, pca.n_components_+1), pca.explained_variance_ratio_, 'ro-', linewidth=2)
plt.title('Scree Plot')
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.show()

import statsmodels.api as sm

pca = PCA(n_components=6)
weather_pca = pca.fit_transform(weather_df)
df['Weather_PC1'] = weather_pca[:, 0]
df['Weather_PC2'] = weather_pca[:, 1]
df['Weather_PC3'] = weather_pca[:, 2]
df['Weather_PC4'] = weather_pca[:, 3]
df['Weather_PC5'] = weather_pca[:, 4]
df['Weather_PC6'] = weather_pca[:, 5]

date_str = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2) + '-' + df['DayofMonth'].astype(str).str.zfill(2)
daily_df = df[['Arr_Delay_boolean', 'Weather_PC1', 'Weather_PC2', 'Weather_PC3', 'Weather_PC4', 'Weather_PC5', 'Weather_PC6']].groupby(pd.to_datetime(date_str, format='%Y-%m-%d')).mean()
model = sm.tsa.statespace.SARIMAX(daily_df['Arr_Delay_boolean'], order=(1, 0, 1), seasonal_order=(1, 0, 1, 7), exog=daily_df[['Weather_PC1', 'Weather_PC2', 'Weather_PC3', 'Weather_PC4', 'Weather_PC5', 'Weather_PC6']], trend='c')
results = model.fit()
print(results.summary())

forecast = results.get_forecast(steps=7, exog=daily_df[['Weather_PC1', 'Weather_PC2', 'Weather_PC3', 'Weather_PC4', 'Weather_PC5', 'Weather_PC6']].tail(7))
forecast_summary = forecast.summary_frame()

print(forecast_summary)

from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

# Get the actual values
y_true = daily_df['Arr_Delay_boolean'].tail(7)

# Get the predicted values
y_pred = forecast_summary['mean'].values

# Calculate the MAPE and RMSE
mape = mean_absolute_percentage_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)

print(f'MAPE: {mape:.2%}')
print(f'RMSE: {rmse:.2f}')

import matplotlib.pyplot as plt

# plot time series
plt.figure(figsize=(15, 6))
plt.plot(daily_df.index, daily_df['Arr_Delay_boolean'])
plt.title('Daily Flight Delay Time Series')
plt.xlabel('Date')
plt.ylabel('Mean Arrival Delay')
plt.show()

import matplotlib.pyplot as plt

# Smoothed curve with a rolling window of size 7
rolling_mean = daily_df['Arr_Delay_boolean'].rolling(window=7).mean()

# Plot original data and smoothed curve
plt.figure(figsize=(15, 6))
plt.plot(daily_df.index, daily_df['Arr_Delay_boolean'], label='Original')
plt.plot(daily_df.index, rolling_mean, label='Smoothed')
plt.legend()
plt.show()

# Split the data into training and test sets
train_df = daily_df[:-100]
test_df = daily_df[-100:]

# Fit the SARIMAX model on the training set
model = sm.tsa.statespace.SARIMAX(train_df['Arr_Delay_boolean'], order=(1, 0, 1), seasonal_order=(1, 0, 1, 7), exog=train_df[['Weather_PC1', 'Weather_PC2', 'Weather_PC3', 'Weather_PC4', 'Weather_PC5', 'Weather_PC6']], trend='c')
results = model.fit()

# Get predictions for the test set
forecast = results.get_prediction(start=test_df.index[0], end=test_df.index[-1], exog=test_df[['Weather_PC1', 'Weather_PC2', 'Weather_PC3', 'Weather_PC4', 'Weather_PC5', 'Weather_PC6']])
forecast_summary = forecast.summary_frame()

# Get the actual values for the test set
y_true = test_df['Arr_Delay_boolean']

# Get the predicted values for the test set
y_pred = forecast_summary['mean']

# Calculate the MAPE and RMSE
mape = mean_absolute_percentage_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)

print(f'MAPE: {mape:.2%}')
print(f'RMSE: {rmse:.2f}')

import pickle

with open('/content/drive/MyDrive/DSA3101_Share/sarimax_model.pkl', 'wb') as f:
    pickle.dump(results, f)

# Get predictions for the test set
forecast = results.get_prediction(start=test_df.index[0], end=test_df.index[-1], exog=test_df[['Weather_PC1', 'Weather_PC2', 'Weather_PC3', 'Weather_PC4', 'Weather_PC5', 'Weather_PC6']])
forecast_summary = forecast.summary_frame()

# Get the actual values for the test set
y_true = test_df['Arr_Delay_boolean']

# Get the predicted values for the test set
y_pred = forecast_summary['mean']

# Calculate the MAPE and RMSE
mape = mean_absolute_percentage_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)

# Print the accuracy metrics
print(f'MAPE: {mape:.2%}')
print(f'RMSE: {rmse:.2f}')

# Print the summary table
print(forecast_summary)

# Plot the actual and predicted values
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(test_df.index, y_true, label='Actual')
ax.plot(y_pred.index, y_pred, label='Predicted')
ax.set_xlabel('Date')
ax.set_ylabel('Delay indicator')
ax.legend()
plt.show()

# Get a summary of the model
print(results.summary())