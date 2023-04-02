## XGBoost Flight Delay Prediction API

This API is used to predict the likelihood of a flight being delayed. It uses an XGBoost model to make the prediction, based on various input features such as the airline carrier, origin and destination airports, and weather conditions.

### Requirements

To use this API, you need the following requirements:

- Python 3.7 or higher
- Flask
- NumPy
- Pandas
- Scikit-learn
- XGBoost

### Usage

1. Clone this repository to your local machine.
2. Install the required libraries by running `pip install -r requirements.txt`.
3. Run the Flask app by executing `python app.py`.
4. Send a POST request to the `/predict` endpoint with a JSON payload containing the input data. An example payload is provided below:

```json
{
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
    "windgust": 57.685756,
    "windspeed": 10.5,
    "winddir": 90.0,
    "sealevelpressure": 1030.7,
    "cloudcover": 98.5,
    "visibility": 6.6,
    "moonphase": 0.39,
    "conditions": "Snow, Rain, Overcast",
    "description": "Cloudy skies throughout the day with rain or snow."
}


5. The API will return a JSON response with the predicted class label as an integer, either 0 or 1:

    {
        'prediction': 0
    }

### Limitations
- The input data must have the same structure as the example payload above.
- The API only works for flights within the United States, as the origin state column is required.
- The model used by the API was trained on flight data from 2006, so it may not be accurate for more recent years.
