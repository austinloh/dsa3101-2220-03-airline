import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.model_selection import train_test_split


data = pd.read_csv('../../database/data/2008_data_with_weather.csv')
data = data[["Month", "DayofMonth", "DayOfWeek", "CRSDepTime", "CRSArrTime", "UniqueCarrier", "Origin", "Dest", "Distance", "ArrDelay"]]
data.dropna(inplace = True)
data['ArrDelayed'] = (data['ArrDelay'] > 0).astype(int)
data["CRSDepHour"] = data["CRSDepTime"] // 100
data["CRSArrHour"] = data["CRSArrTime"] // 100
data.drop(['CRSDepTime', 'CRSArrTime'], axis=1, inplace=True)
data.drop('ArrDelay', axis=1, inplace=True)
# Convert Month, DayofMonth, DayOfWeek into categorical variables
data[["Month", "DayofMonth", "DayOfWeek"]] = data[["Month", "DayofMonth", "DayOfWeek"]].astype(str)
# Split CRSDepHour and CRSArrHour into 8 classes
hour_map = {1: "1TO3", 2: "1TO3", 3: "1TO3",
            4: "4TO6", 5: "4TO6", 6: "4TO6",
            7: "7TO9", 8: "7TO9", 9: "7TO9",
            10: "10TO12", 11: "10TO12", 12: "10TO12",
            13: "13TO15", 14: "13TO15", 15: "13TO15",
            16: "16TO18", 17: "16TO18", 18: "16TO18",
            19: "19TO21", 20: "19TO21", 21: "19TO21",
            22: "22TO0", 23: "22TO0", 24: "22TO0", 0: "22TO0"}
data = data.replace({'CRSDepHour': hour_map, 'CRSArrHour': hour_map})
data = pd.get_dummies(data)

y = data.pop('ArrDelayed')
# Split into training dataset and test dataset
data, _, y, _ = train_test_split(data, y, train_size=0.1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(data, y, train_size=0.8, random_state=42)
predictors = list(X_train.columns.values)


rf = RandomForestClassifier(n_estimators=round(len(predictors)/3), criterion="entropy", max_depth = 4)
rf.fit(X_train, y_train)


pickle.dump(rf, open('random_forest_model.pkl', 'wb'))
pickle.dump(predictors, open('predictors.pkl', 'wb'))