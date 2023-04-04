import requests
import json

URL = 'http://127.0.0.1:5000/'

# FOR LIME + LIGHTGBM
# Getting feature importance as list
h1 = {'Content-type': 'application/json', 'Accept': 'application/json'}
# Inputs are for columns = ['Month','DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime', 'UniqueCarrier',
#       'TailNum', 'CRSElapsedTime', 'Origin', 'Dest', 'Distance']
params1 = {'inputs': [3, 28, 5, 635, 912, 'YV', 'N956LR', 97.0, 'MEM', 'CLT', 512]}
req = requests.get('http://127.0.0.1:5000/api/lime_fi',headers=h1, json=params1)
#req.json
#output is a list containing feature importance
#e.g. '[["DayOfWeek=5",0.04459373534188866],["CRSDepTime",0.042533720995852516],["Distance",0.022956906602916605],\
# ["DayofMonth=28",-0.02028326218839363],["Dest=CLT",-0.01361981943433478],["Origin=MEM",0.012663409910100145],\
# ["TailNum=N956LR",0.012495320364865902],["Month=3",0.012461212222973975],["UniqueCarrier=YV",-0.01192746105881419],\
# ["CRSArrTime",0.004145908201383367]]\n'

# Getting feature importance with plots as html?
h1 = {'Content-type': 'application/json', 'Accept': 'application/json'}
# Inputs are for columns = ['Month','DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime', 'UniqueCarrier',
#       'TailNum', 'CRSElapsedTime', 'Origin', 'Dest', 'Distance']
params1 = {'inputs': [3, 28, 5, 635, 912, 'YV', 'N956LR', 97.0, 'MEM', 'CLT', 512]}
req = requests.get('http://127.0.0.1:5000/api/lime_plot',headers=h1, json=params1)
#req.json
#output is a html string? Need to figure out how to render if using
#'"<html>\\n  ... ... </html>"\n'

# FOR XGBOOST
sample_input = {
    "Year": 2006,
    "Month": 1,
    "DayofMonth": 11,
    "DayOfWeek": 3,
    "CRSDepTime": 1053,
    "CRSArrTime": 1318,
    "UniqueCarrier": "US",
    "TailNum": "N834AW",
    "CRSElapsedTime": 265.0,
    "Origin": "ATL",
    "Dest": "PHX",
    "Distance": 1587,
    "origin_state": "GA",
    "tempmax": 2.1,
    "tempmin": -4.6,
    "temp": -0.1,
    "feelslikemax": 1.3,
    "feelslikemin": -4.6,
    "feelslike": -0.6,
    "dew": -0.9,
    "humidity": 94.6,
    "precip": 1.573,
    "precipcover": 8.33,
    "snow": 0.0,
    "snowdepth": 0.6,
    "windgust": 0.0,  # NaN values should be replaced with None
    "windspeed": 10.5,
    "winddir": 90.0,
    "sealevelpressure": 1030.7,
    "cloudcover": 98.5,
    "visibility": 6.6,
    "moonphase": 0.39,
    "conditions": "Snow, Rain, Overcast",
    "description": "Cloudy skies throughout the day with rain or snow."
}

headers = {"Content-Type": "application/json"}

response = requests.post('http://127.0.0.1:5000/api/xgb_predict', data=json.dumps(sample_input), headers=headers)

print(response.json())
#Will take extremely long time to run since the model is complexed.