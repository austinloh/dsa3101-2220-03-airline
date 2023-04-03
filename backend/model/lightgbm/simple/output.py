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
transforming = ['Month','DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest']
#features used
columns = ['Month','DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime', 'UniqueCarrier',
       'TailNum', 'CRSElapsedTime', 'Origin', 'Dest', 'Distance']





#sample input. Actual label: 1
testing = [3,28,5,635,912,'YV','N956LR', 97.0,'MEM','CLT',512]


# accept input as list, transform and predict output using lime model
def lime_output(x):
  X = pd.DataFrame([x], columns = columns)
  X[transforming] = oe.transform(X[transforming])
  res = hgb.predict(X)
  X = X.to_numpy()
  exp = explainer.explain_instance(X[0], hgb.predict_proba)
  return res, exp

prediction, exp = lime_output(testing)
print(prediction)
print(exp.as_list())

#output as html page
#html = exp.as_html()