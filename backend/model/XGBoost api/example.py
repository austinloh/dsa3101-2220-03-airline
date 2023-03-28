import requests
import json

url = "http://127.0.0.1:5000/predict"

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

response = requests.post(url, data=json.dumps(sample_input), headers=headers)

print(response.json())
#Will take extremely long time to run since the model is complexed.