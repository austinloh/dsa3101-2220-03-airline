import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
import lime
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from lime import lime_tabular

df = pd.read_csv('2008_data_with_weather.csv')

#data preprocessing
df.drop(['Year', 'DepTime', 'ArrTime', 'FlightNum', 'ActualElapsedTime', 'DepDelay', 'AirTime', \
         'TaxiIn', 'TaxiOut', 'Cancelled', 'CancellationCode', 'Diverted','CarrierDelay', 'WeatherDelay', \
         'NASDelay', 'SecurityDelay', 'LateAircraftDelay', \
         'datetime', 'origin_state', 'solarradiation', 'solarenergy', 'severerisk', 'sunrise', 'sunset', \
         'moonphase', 'description', 'icon', 'stations', 'windgust', 'preciptype','uvindex'], axis=1, inplace=True)
numerical = ['tempmax', 'tempmin', 'temp', 'feelslikemax' ,'feelslikemin', 'feelslike', 'dew', 'humidity', 'precip', \
             'precipprob', 'precipcover', 'snow', 'snowdepth', 'windspeed', 'winddir', 'sealevelpressure', 'cloudcover', 'visibility']
for col in numerical:
  df[col].fillna(df[col].mean(), inplace = True)
df['conditions'].fillna("unknown", inplace=True)
df.dropna(inplace=True)

df['ArrDelayed'] = (df['ArrDelay'] > 0).astype(int)
X = df.drop(['ArrDelayed'], axis=1)
y = df['ArrDelayed']
feature_names = list(X.columns)

le= LabelEncoder()
le.fit(y)
y = le.transform(y)
class_names = le.classes_

categorical_features = [0,1,2,5,6,8,9,29]

oe = OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1)
oe.fit(X[['Month', 'DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'conditions']])
X[['Month','DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'conditions']] = \
oe.transform(X[['Month', 'DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'conditions']])

categorical_names = {}
i = 0
for feature in categorical_features:
  categorical_names[feature] = oe.categories_[i]
  i+=1

train, test, labels_train, labels_test = train_test_split(X, y, train_size=0.8, random_state=42)
hgb2 = HistGradientBoostingClassifier(random_state = 42)
hgb2.fit(train, labels_train)

pred = hgb2.predict(test)
#print(confusion_matrix(labels_test, pred))
#print(classification_report(labels_test, pred))

train_num = train.to_numpy()
test_num = test.to_numpy()

explainer = lime_tabular.LimeTabularExplainer(train_num, feature_names = feature_names,class_names=class_names,
                                                   categorical_features=categorical_features, 
                                                   categorical_names=categorical_names, discretize_continuous=False)

i = 19000
#print(test.iloc[i])
#print(labels_test[i])

exp = explainer.explain_instance(test_num[i], hgb2.predict_proba)
exp.show_in_notebook()

testing = [2, 24, 7, 1545, 1802, 'XE', 'N17108', 137.0, 'EWR', 'LEX', 588,
       3.3, -6.8, -1.4, 2.0, -10.0, -3.9, -8.2, 60.8, 0.642, 100.0, 20.83,
       0.0, 0.6, 13.1, 276.2, 1020.0, 0.8, 15.9, 'Snow, Rain']
columns = feature_names
transforming = ['Month','DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'conditions']

#explainer
def lime_output(x):
  X = pd.DataFrame([x], columns = columns)
  X[transforming] = oe.transform(X[transforming])
  X = X.to_numpy()
  exp = explainer.explain_instance(X[0], hgb2.predict_proba)
  return exp
l = lime_output(testing)
l.as_list()

from pickle import dump
dump(hgb2, open('model.pkl', 'wb'))
dump(oe, open('encoder.pkl', 'wb'))

from dill import dump
dump(explainer, open('lime.pkl', 'wb'))