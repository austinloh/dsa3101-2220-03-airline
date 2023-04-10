from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
df = pd.read_csv('/content/drive/MyDrive/2008_data_with_weather.csv')

df['Arr_Delay_boolean'] = (df['ArrDelay'] > 0).astype(int)
df.drop(['Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'DepTime', 'CRSDepTime', 'ArrTime', 'CRSArrTime',
                  'FlightNum', 'ActualElapsedTime', 'CRSElapsedTime',
                  'AirTime', 'ArrDelay', 'DepDelay', 'Origin', 'Dest',
                  'TaxiIn', 'TaxiOut', 'Cancelled', 'CancellationCode', 
                  'Diverted', 'CarrierDelay', 'WeatherDelay', 'NASDelay',
                  'SecurityDelay', 'LateAircraftDelay', 'datetime', 
                  'origin_state','sunrise','sunset','stations'], axis=1, inplace=True)

cols = df.columns.tolist()
cols_str = ', '.join(cols)
print(cols_str)

# Assuming you have loaded the dataset in variable 'df'
# Fill missing numerical values with the mean
for column in df.select_dtypes(include=[np.number]).columns:
    df[column].fillna(df[column].mean(), inplace=True)

# Fill missing string values with a default value
for column in df.select_dtypes(include=[object]).columns:
    df[column].fillna("unknown", inplace=True)

# Label encode categorical variables
for column in df.select_dtypes(include=[object]).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])

# Separate features and target
X = df.drop("Arr_Delay_boolean", axis=1).values
y = df["Arr_Delay_boolean"].values

# Split the dataset into train and validation sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Convert the dataset to DMatrix format
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(X_val, label=y_val)
dtest = xgb.DMatrix(X_test, label=y_test)  # Additional test set

# Set up the watchlist and train the model
watchlist = [(dtrain, "train"), (dval, "val")]
num_rounds = 20000  # Increase the number of rounds

model = xgb.train(
    params,
    dtrain,
    num_rounds,
    watchlist,
    early_stopping_rounds=10,
    verbose_eval=50
)

# Display the best iteration and corresponding validation logloss
best_iteration = model.best_iteration
best_val_logloss = model.best_score
print(f"Best Iteration: {best_iteration}, Best Validation Logloss: {best_val_logloss:.4f}")

# Calculate the test accuracy
y_test_pred = model.predict(dtest)
y_test_pred_rounded = np.round(y_test_pred)
test_accuracy = np.sum(y_test == y_test_pred_rounded) / len(y_test)
print(f"Test Accuracy: {test_accuracy:.4f}")

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(200, 200))
xgb.plot_tree(model, num_trees=10, ax=ax)
plt.show()