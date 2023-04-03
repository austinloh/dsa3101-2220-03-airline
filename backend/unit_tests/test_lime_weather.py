#from model.lightgbm.simple import output
from pickle import load
import pandas as pd
import pytest

#Ordinal Encoder
with open('../model/lightgbm/weather/encoder.pkl', 'rb') as f:
   oe = load(f)
#hgb model
with open('../model/lightgbm/weather/model.pkl' ,'rb') as f:
    hgb = load(f)
#LIME explainer
with open('../model/lightgbm/weather/lime.pkl' ,'rb') as f:
    explainer = load(f)    

#Encoded features
transforming = ['Month','DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'conditions']
#features used
columns = ['Month', 'DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime', \
           'UniqueCarrier', 'TailNum', 'CRSElapsedTime', 'Origin', 'Dest', \
           'Distance', 'tempmax', 'tempmin', 'temp', 'feelslikemax', \
           'feelslikemin', 'feelslike', 'dew', 'humidity', 'precip', \
           'precipprob', 'precipcover', 'snow', 'snowdepth', 'windspeed', \
           'winddir', 'sealevelpressure', 'cloudcover', 'visibility', 'conditions']

@pytest.fixture
def sample_input():
    testing = [2, 24, 7, 1545, 1802, 'XE', 'N17108', 137.0, 'EWR', 'LEX', 588, \
           3.3, -6.8, -1.4, 2.0, -10.0, -3.9, -8.2, 60.8, 0.642, 100.0, 20.83, \
            0.0, 0.6, 13.1, 276.2, 1020.0, 0.8, 15.9, 'Snow, Rain']
    return testing

def test_lime_output_simple(sample_input):
  X = pd.DataFrame([sample_input], columns = columns)
  X[transforming] = oe.transform(X[transforming])
  res = hgb.predict(X)
  X = X.to_numpy()
  exp = explainer.explain_instance(X[0], hgb.predict_proba)
  assert res in [0,1]
  assert len(exp.as_list()) == 10
