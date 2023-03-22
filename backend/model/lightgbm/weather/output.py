from pickle import load
import pandas as pd
import lime

#Ordinal Encoder
with open('encoder.pkl', 'rb') as f:
   oe = load(f)
#hgb model
with open('model.pkl' ,'rb') as f:
    hgb = load(f)
#LIME explainer
with open('lime.pkl' ,'rb') as f:
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

#sample input. Actual label: 1
testing = [2, 24, 7, 1545, 1802, 'XE', 'N17108', 137.0, 'EWR', 'LEX', 588, \
           3.3, -6.8, -1.4, 2.0, -10.0, -3.9, -8.2, 60.8, 0.642, 100.0, 20.83, \
            0.0, 0.6, 13.1, 276.2, 1020.0, 0.8, 15.9, 'Snow, Rain']

def lime_output(x):
  X = pd.DataFrame([x], columns = columns)
  X[transforming] = oe.transform(X[transforming])
  res = hgb.predict(X)
  X = X.to_numpy()
  exp = explainer.explain_instance(X[0], hgb.predict_proba)
  return res, exp

res, exp = lime_output(testing)
print(res)
print(exp.as_list())

#output as html page
#html = exp.as_html()