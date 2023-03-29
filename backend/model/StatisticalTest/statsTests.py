import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2, mutual_info_classif

df = pd.read_csv('../../../database/data/2008_data_with_weather.csv')

#drop features with all NA or irrelevant to training process
df.drop(['Year', 'DepTime', 'ArrTime', 'FlightNum', 'ActualElapsedTime', 'DepDelay', 'AirTime', \
         'TaxiIn', 'TaxiOut', 'Cancelled', 'CancellationCode', 'Diverted','CarrierDelay', 'WeatherDelay', \
         'NASDelay', 'SecurityDelay', 'LateAircraftDelay', \
         'datetime', 'origin_state', 'solarradiation', 'solarenergy', 'severerisk', 'sunrise', 'sunset', \
         'moonphase', 'description', 'icon', 'stations', 'windgust', 'preciptype','uvindex'], axis=1, inplace=True)

numerical = ['tempmax', 'tempmin', 'temp', 'feelslikemax' ,'feelslikemin', 'feelslike', 'dew', 'humidity', 'precip', \
             'precipprob', 'precipcover', 'snow', 'snowdepth', 'windspeed', 'winddir', 'sealevelpressure', 'cloudcover', 'visibility']

#fill continuous variables with mean
for col in numerical:
  df[col].fillna(df[col].mean(), inplace = True)

df['conditions'].fillna("unknown", inplace=True)
df['ArrDelayed'] = (df['ArrDelay'] > 0).astype(int)
df.drop('ArrDelay', axis=1, inplace=True)
df.dropna(inplace = True)

categorical = ['Month', 'DayofMonth', 'DayOfWeek']

X = df.drop(['ArrDelayed'], axis=1)
y = df['ArrDelayed']

feature_names = list(X.columns)

#encode labels
le= LabelEncoder()
le.fit(y)
y = le.transform(y)
class_names = le.classes_

#encode categorical features
categorical_features = [0,1,2,5,6,8,9,29]
oe = OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1)
oe.fit(X[['Month', 'DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'conditions']])
X[['Month','DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'conditions']] = \
oe.transform(X[['Month', 'DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'conditions']])

#obtain categories names
categorical_names = {}
i = 0
for feature in categorical_features:
  categorical_names[feature] = oe.categories_[i]
  i+=1


# Chi-square test
train, test, labels_train, labels_test = train_test_split(X, y, train_size=0.8, random_state=42)

def select_features(X_train, y_train, X_test):
    fs = SelectKBest(score_func=chi2, k='all')
    fs.fit(X_train, y_train)
    X_train_fs = fs.transform(X_train)
    X_test_fs = fs.transform(X_test)
    return X_train_fs, X_test_fs, fs

scaler = MinMaxScaler()
train[['CRSElapsedTime', 'tempmax', 'tempmin', 'temp', 'feelslikemax', 'feelslikemin', 'feelslike', 'dew']] = \
scaler.fit_transform(train[['CRSElapsedTime', 'tempmax', 'tempmin', 'temp', 'feelslikemax', 'feelslikemin', 'feelslike', 'dew']])

X_train_chi_2, X_test_chi_2, chi_2 = select_features(train, labels_train, test)

#for i in range(len(chi_2.scores_)):
#    print('Feature %s: %f' % (feature_names[i], chi_2.scores_[i]))

#output Chi-square feature importance
fig = plt.figure()
plt.figure(figsize=(16,12))
plt.title('Feature importance using Chi-squared test')
plt.barh(feature_names, chi_2.scores_)
fig.savefig('chi2.png', dpi=fig.dpi)


# Information Gain
train, test, labels_train, labels_test = train_test_split(X, y, train_size=0.8, random_state=42)
def select_features(X_train, y_train, X_test):
    fs = SelectKBest(score_func=mutual_info_classif, k='all')
    fs.fit(X_train, y_train)
    X_train_fs = fs.transform(X_train)
    X_test_fs = fs.transform(X_test)
    return X_train_fs, X_test_fs, fs

#output Information Gain feature importance
X_train_fs, X_test_fs, fs = select_features(train, labels_train, test)
fig = plt.figure()
plt.figure(figsize=(16,12))
plt.title('Feature importance using Mutual Information/Information Gain')
plt.barh(feature_names, fs.scores_)
fig.savefig('IG.png', dpi=fig.dpi)


# ANOVA F-score
train, test, labels_train, labels_test = train_test_split(X, y, train_size=0.8, random_state=42)
def select_features(X_train, y_train, X_test):
    fs = SelectKBest(k='all')
    fs.fit(X_train, y_train)
    X_train_fs = fs.transform(X_train)
    X_test_fs = fs.transform(X_test)
    return X_train_fs, X_test_fs, fs

#output ANOVA F-score feature importance
X_train_fs, X_test_fs, fs = select_features(train, labels_train, test)
fig = plt.figure()
plt.figure(figsize=(16,12))
plt.title('Feature importance using ANOVA F-score')
plt.barh(feature_names, fs.scores_)
fig.savefig('Fscore.png', dpi=fig.dpi)