import shap
import pickle
import pandas as pd

model = pickle.load(open('neural_network_model.pkl', 'rb'))
mean_df = pd.read_csv('train_mean.csv')

explainer = shap.KernelExplainer(model = model.predict, data = mean_df, link = "identity")


# Input must contains:
# ['Month', 'DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime',
#        'UniqueCarrier', 'CRSElapsedTime', 'ArrDelay', 'Origin', 'Dest',
#        'Distance', 'tempmax', 'tempmin', 'temp', 'feelslikemax',
#        'feelslikemin', 'feelslike', 'dew', 'humidity', 'precip', 'precipprob',
#        'precipcover', 'snow', 'snowdepth', 'windspeed', 'winddir',
#        'sealevelpressure', 'cloudcover', 'visibility', 'conditions']

def calculate_shap_values(input):
    # Preprocess input
    df = pd.read_csv('../../database/data/2008_data_with_weather.csv')
    df.drop(['Year', 'DepTime', 'ArrTime', 'FlightNum', 'ActualElapsedTime', 'DepDelay', 'AirTime', 'TailNum', \
            'TaxiIn', 'TaxiOut', 'Cancelled', 'CancellationCode', 'Diverted','CarrierDelay', 'WeatherDelay', \
            'NASDelay', 'SecurityDelay', 'LateAircraftDelay', \
            'datetime', 'origin_state', 'solarradiation', 'solarenergy', 'severerisk', 'sunrise', 'sunset', \
            'moonphase', 'description', 'icon', 'stations', 'windgust', 'preciptype','uvindex'], axis=1, inplace=True)

    df = pd.concat([input, df])
    df['ArrDelayed'] = (df['ArrDelay'] > 0).astype(int)
    df.drop('ArrDelay', axis=1, inplace=True)
    df["CRSDepHour"] = df["CRSDepTime"] // 100
    df["CRSArrHour"] = df["CRSArrTime"] // 100
    df.drop(['CRSDepTime', 'CRSArrTime'], axis=1, inplace=True)
    df[["Month", "DayofMonth", "DayOfWeek"]] = df[["Month", "DayofMonth", "DayOfWeek"]].astype(str)
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
    df = pd.get_dummies(df)
    df = df.drop(labels=["ArrDelayed"], axis=1)


    # Calculate shap values
    shap_values = explainer.shap_values(X = df.iloc[0:1,:], nsamples = 500)

    return shap_values, df.iloc[0:1,:]


def generate_plot(shap_values, preprocessed_data):
    shap.summary_plot(shap_values = shap_values[0],
            features = preprocessed_data,
            plot_size = (12,6)
            )