# Flight Delay Prediction API

This API uses an XGBoost model to predict flight delays based on various features such as date, time, carrier, origin, destination, weather conditions, and more. The model has been trained on historical flight and weather data.

## Setup

1. Install the required Python packages:

```bash
pip install flask xgboost pandas scikit-learn

2.Run the API server:

python app.py

The API will be available at http://127.0.0.1:5000/.

Usage

Send a POST request to the /xgb_predict endpoint with a JSON payload containing the input data. The input data should include the following fields:

Year (int64)
Month (int64)
DayofMonth (int64)
DayOfWeek (int64)
CRSDepTime (int64)
CRSArrTime (int64)
UniqueCarrier (string)
TailNum (string)
CRSElapsedTime (float64)
Origin (string)
Dest (string)
Distance (int64)
origin_state (string)
tempmax (float64)
tempmin (float64)
temp (float64)
feelslikemax (float64)
feelslikemin (float64)
feelslike (float64)
dew (float64)
humidity (float64)
precip (float64)
precipcover (float64)
snow (float64)
snowdepth (float64)
windgust (float64)
windspeed (float64)
winddir (float64)
sealevelpressure (float64)
cloudcover (float64)
visibility (float64)
moonphase (float64)
conditions (string)
description (string)

It takes extremely long time to run, maybe because of one-hot encode.

