from flask import Flask, request, jsonify, send_file, render_template
from pickle import load
import pandas as pd
import lime

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
with open("XGBoost_api/XGBoost_model_better.pkl", "rb") as f:
    xgb = load(f)

# Load the label encodings
with open("XGBoost_api/label_encodings.pkl", "rb") as f:
    xgb_encodings = load(f)

# Define a function to preprocess the input data
def preprocess_input(input_data):
    input_df = pd.DataFrame(input_data, index=[0])

    # Apply label encodings
    input_df['TailNum'] = xgb_encodings['TailNum'].transform(input_df['TailNum'])
    input_df['Origin'] = xgb_encodings['Origin'].transform(input_df['Origin'])
    input_df['Dest'] = xgb_encodings['Dest'].transform(input_df['Dest'])
    input_df['origin_state'] = xgb_encodings['origin_state'].transform(input_df['origin_state'])

    # Apply one-hot encodings
    unique_carrier_ohe = xgb_encodings['UniqueCarrier'].transform(input_df[['UniqueCarrier']])
    conditions_ohe = xgb_encodings['conditions'].transform(input_df[['conditions']])
    description_ohe = xgb_encodings['description'].transform(input_df[['description']])

    # Convert the one-hot encoded arrays to dataframes
    unique_carrier_df = pd.DataFrame(unique_carrier_ohe.toarray(), columns=xgb_encodings['UniqueCarrier'].get_feature_names_out(['UniqueCarrier']))
    conditions_df = pd.DataFrame(conditions_ohe.toarray(), columns=xgb_encodings['conditions'].get_feature_names_out(['conditions']))
    description_df = pd.DataFrame(description_ohe.toarray(), columns=xgb_encodings['description'].get_feature_names_out(['description']))

    # Concatenate the one-hot encoded dataframes with the original dataframe
    input_df = pd.concat([input_df.drop(columns=['UniqueCarrier', 'conditions', 'description']), unique_carrier_df, conditions_df, description_df], axis=1)

    return input_df.values[0]


@app.route('/xgb_predict', methods=['POST'])
def predict():
    input_data = request.json
    # input_data_dict = json.loads(input_data)  # Remove this line
    preprocessed_data = preprocess_input(input_data)  # Use input_data directly
    prediction = xgb.predict(preprocessed_data)
    response = {'prediction': int(prediction[0])}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)