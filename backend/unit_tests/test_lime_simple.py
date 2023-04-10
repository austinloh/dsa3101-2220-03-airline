#from model.lightgbm.simple import output
from pickle import load
import pandas as pd
import pytest

#Ordinal Encoder
with open('../model/lightgbm/simple/encoder.pkl', 'rb') as f:
   oe = load(f)
#hgb model
with open('../model/lightgbm/simple/model.pkl' ,'rb') as f:
    hgb = load(f)
#LIME explainer
with open('../model/lightgbm/simple/lime.pkl' ,'rb') as f:
    explainer = load(f)    

#Encoded features
transforming = ['Month','DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest']
#features used
columns = ['Month','DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime', 'UniqueCarrier',
       'TailNum', 'CRSElapsedTime', 'Origin', 'Dest', 'Distance']

@pytest.fixture
def sample_input():
    testing = [3,28,5,635,912,'YV','N956LR', 97.0,'MEM','CLT',512]
    return testing

def test_lime_output_simple(sample_input):
  X = pd.DataFrame([sample_input], columns = columns)
  X[transforming] = oe.transform(X[transforming])
  res = hgb.predict(X)
  X = X.to_numpy()
  exp = explainer.explain_instance(X[0], hgb.predict_proba)
  assert res in [0,1]
  assert len(exp.as_list()) == 10
