from flask import Flask, request, jsonify, send_file, render_template
from pickle import load
import pandas as pd
import lime
import numpy as np

app = Flask(__name__)

#Ordinal Encoder
with open('lightgbm/simple/encoder.pkl', 'rb') as f:
    hgb_oe = load(f)
#hgb model
with open('lightgbm/simple/model.pkl' ,'rb') as f:
    hgb = load(f)
#LIME explainer
with open('lightgbm/simple/lime.pkl' ,'rb') as f:
    hgb_explainer = load(f)    

#Encoded features
transforming = ['Month','DayofMonth', 'DayOfWeek', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest']
#features used
columns = ['Month','DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime', 'UniqueCarrier',
       'TailNum', 'CRSElapsedTime', 'Origin', 'Dest', 'Distance']

@app.route('/api/lime_fi', methods = ['GET'])
def lime_output():
  #print('ok')
  x = request.get_json()['inputs']
  #print(x)
  X = pd.DataFrame([x], columns = columns)
  X[transforming] = hgb_oe.transform(X[transforming])
  res = hgb.predict(X)
  X = X.to_numpy()
  exp = hgb_explainer.explain_instance(X[0], hgb.predict_proba)
  return jsonify(exp.as_list())

@app.route('/api/lime_plot', methods = ['GET'])
def fn():
   x = request.get_json()['inputs']
   X = pd.DataFrame([x], columns = columns)
   X[transforming] = hgb_oe.transform(X[transforming])
   res = hgb.predict(X)
   X = X.to_numpy()
   exp = hgb_explainer.explain_instance(X[0], hgb.predict_proba)
   return jsonify(exp.as_html())

#@app.route('/upload', methods = ['POST'])
#def fn():
#    return render_template('uploaded.html', fname = f.filename)

# Load the XGBoost model
with open("XGBoost_api_no_onehot/XGBoost_model_no_onehot.pkl", "rb") as f:
    model = load(f)

# Load the label encodings
with open("XGBoost_api_no_onehot/no_onehot_encoder_dictionary.pkl", "rb") as f:
    encoding_dict = load(f)

def transform_with_fallback(encoder, column_data):
    try:
        return encoder.transform(column_data)
    except ValueError as e:
        print(f"Warning: {str(e)}")
        return -1

# Define a function to preprocess the input data
def preprocess_input(input_data):
    input_df = pd.DataFrame(input_data, index=[0])

    # Convert categorical columns to category data type
    cat_cols = ['UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'origin_state', 'conditions', 'description']
    for col in cat_cols:
        input_df[col] = input_df[col].astype('category')

    # Replace missing categorical values with 'unknown'
    for col in input_df.select_dtypes(include=['category']):
        input_df[col] = input_df[col].cat.add_categories(['unknown'])
        input_df[col].fillna('unknown', inplace=True)

    # Replace missing numeric values with mean of that column
    for col in input_df.select_dtypes(include=[np.number]):
        mean_val = input_df[col].mean()
        input_df[col].fillna(mean_val, inplace=True)

    # Apply label encodings using the encoding dictionary
    for column in cat_cols:
        if column in encoding_dict:
            input_df[column] = input_df[column].map(encoding_dict[column])
        else:
            input_df[column] = -1  # Assign a default value to unseen labels

    return input_df.values[0]


@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    #print("Input data:")
    #print(input_data)
    preprocessed_data = preprocess_input(input_data)
    #print("Preprocessed data:")
    #print(preprocessed_data)
    prediction = model.predict(preprocessed_data.reshape(1, -1))
    #print("Model prediction:")
    #print(prediction)
    response = {'prediction': int(prediction[0])}
    return jsonify(response)

import mysql.connector
from sshtunnel import SSHTunnelForwarder
tunnel = SSHTunnelForwarder(('50.19.153.183', 22), ssh_username='ubuntu', 
                            ssh_pkey='./pem/dsa3101-03.pem', remote_bind_address=('127.0.0.1', 3306))
tunnel.start()
conn = mysql.connector.connect(host='127.0.0.1', user='root', password='rootpw', 
                               port=tunnel.local_bind_port, use_pure=True, database='mydb')
@app.route('/api/database', methods = ['GET'])
def db():
    x = request.get_json()['inputs']
    cursor = conn.cursor()
    #change SQL command
    #change SQL command
    cursor.execute(x) 
    result = cursor.fetchall()
    return jsonify(result)