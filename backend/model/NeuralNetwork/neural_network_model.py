import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Softmax
from sklearn.model_selection import train_test_split

df = pd.read_csv('../../database/data/2008_data_with_weather.csv')

df.drop(['Year', 'DepTime', 'ArrTime', 'FlightNum', 'ActualElapsedTime', 'DepDelay', 'AirTime', 'TailNum', \
         'TaxiIn', 'TaxiOut', 'Cancelled', 'CancellationCode', 'Diverted','CarrierDelay', 'WeatherDelay', \
         'NASDelay', 'SecurityDelay', 'LateAircraftDelay', \
         'datetime', 'origin_state', 'solarradiation', 'solarenergy', 'severerisk', 'sunrise', 'sunset', \
         'moonphase', 'description', 'icon', 'stations', 'windgust', 'preciptype','uvindex'], axis=1, inplace=True)

# Convert ArrDelayed into categorical variable
df['ArrDelayed'] = (df['ArrDelay'] > 0).astype(int)
df.drop('ArrDelay', axis=1, inplace=True)

# Transform the time CRSDepTime and CRSArrTime columns into hour only
df["CRSDepHour"] = df["CRSDepTime"] // 100
df["CRSArrHour"] = df["CRSArrTime"] // 100
df.drop(['CRSDepTime', 'CRSArrTime'], axis=1, inplace=True)

# Convert Month, DayofMonth, DayOfWeek into categorical variables
df[["Month", "DayofMonth", "DayOfWeek"]] = df[["Month", "DayofMonth", "DayOfWeek"]].astype(str)

# Split CRSDepHour and CRSArrHour into 8 classes
hour_map = {1: "1TO3", 2: "1TO3", 3: "1TO3",
            4: "4TO6", 5: "4TO6", 6: "4TO6",
            7: "7TO9", 8: "7TO9", 9: "7TO9",
            10: "10TO12", 11: "10TO12", 12: "10TO12",
            13: "13TO15", 14: "13TO15", 15: "13TO15",
            16: "16TO18", 17: "16TO18", 18: "16TO18",
            19: "19TO21", 20: "19TO21", 21: "19TO21",
            22: "22TO0", 23: "22TO0", 24: "22TO0", 0: "22TO0"}
df = df.replace({'CRSDepHour': hour_map, 'CRSArrHour': hour_map})

df.dropna(inplace = True)

# Encode categorical variables using one-hot encoding
df = pd.get_dummies(df)

# Neural Network Model
# Due to RAM issue, drop ArrDelayed column in df instead of creating new table X
y = df[["ArrDelayed"]]
df = df.drop(labels=["ArrDelayed"], axis=1)

# Due to RAM issue, use only 10% of data
df, _, y, _ = train_test_split(df, y, train_size=0.1, random_state=42)

# Split into training dataset and test dataset
train, test, labels_enc_train, labels_test = train_test_split(df, y, train_size=0.8, random_state=42)

# Convert ArrDelayed column into one-hot encoded version
labels_enc_train["ONTIME"] = 1-labels_enc_train["ArrDelayed"]
labels_enc_train["DELAY"] = labels_enc_train["ArrDelayed"]

# Keep the original labels
labels_train = labels_enc_train["ArrDelayed"]
labels_test = labels_test["ArrDelayed"]

labels_enc_train = labels_enc_train.drop(labels=["ArrDelayed"], axis=1)

n_inputs, n_outputs = train.shape[1], labels_enc_train.shape[1]

# Using three linear transformation layers
# 1st layer: input size = n_inputs (579)    output size = 64
# 2nd layer: input size = 64                output size = 32
# 3rd layer: input size = 32                output size = n_outputs (2)
def get_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(64, input_dim=n_inputs, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(n_outputs))
    model.add(Softmax())
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Fitting model
model = get_model(n_inputs, n_outputs)
model.fit(train,labels_enc_train,epochs=50,verbose=0)

# Output model
import pickle
pickle.dump(model, open('neural_network_model.pkl', 'wb'))

# Output average mean of each column in train set
mean_df = pd.DataFrame(train.mean()).transpose()
mean_df.to_csv('train_mean.csv', index=False)