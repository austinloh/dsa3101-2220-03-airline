from flask import Flask, request, jsonify, send_file, render_template
from pickle import load
import pandas as pd
import lime

app = Flask(__name__)

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

@app.route('/api/lime_fi', methods = ['GET'])
def lime_output():
  x = request.args.get('inputs')
  X = pd.DataFrame([x], columns = columns)
  X[transforming] = oe.transform(X[transforming])
  res = hgb.predict(X)
  X = X.to_numpy()
  exp = explainer.explain_instance(X[0], hgb.predict_proba)
  return jsonify(exp.as_list())

@app.route('/api/lime_plot', methods = ['GET'])
def fn():
   x = request.args.get('inputs')
   X = pd.DataFrame([x], columns = columns)
   X[transforming] = oe.transform(X[transforming])
   res = hgb.predict(X)
   X = X.to_numpy()
   exp = explainer.explain_instance(X[0], hgb.predict_proba)
   return send_file(exp.as_html())

#@app.route('/upload', methods = ['POST'])
#def fn():
#    return render_template('uploaded.html', fname = f.filename)
