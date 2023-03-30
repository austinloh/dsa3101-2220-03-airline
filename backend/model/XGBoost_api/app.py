import pickle
import numpy as np
from flask import Flask, request, jsonify
import xgboost as xgb
import pandas as pd

app = Flask(__name__)

# Load the XGBoost model
with open("XGBoost_model_better.pkl", "rb") as f:
    model = pickle.load(f)

# Load the label encodings
with open("label_encodings.pkl", "rb") as f:
    encodings = pickle.load(f)

# Define a function to preprocess the input data
def preprocess_input(input_data):
    input_df = pd.DataFrame(input_data, index=[0])

    # Apply label encodings
    input_df['TailNum'] = encodings['TailNum'].transform(input_df['TailNum'])
    input_df['Origin'] = encodings['Origin'].transform(input_df['Origin'])
    input_df['Dest'] = encodings['Dest'].transform(input_df['Dest'])
    input_df['origin_state'] = encodings['origin_state'].transform(input_df['origin_state'])

    # Apply one-hot encodings
    unique_carrier_ohe = encodings['UniqueCarrier'].transform(input_df[['UniqueCarrier']])
    conditions_ohe = encodings['conditions'].transform(input_df[['conditions']])
    description_ohe = encodings['description'].transform(input_df[['description']])

    # Convert the one-hot encoded arrays to dataframes
    unique_carrier_df = pd.DataFrame(unique_carrier_ohe.toarray(), columns=encodings['UniqueCarrier'].get_feature_names_out(['UniqueCarrier']))
    conditions_df = pd.DataFrame(conditions_ohe.toarray(), columns=encodings['conditions'].get_feature_names_out(['conditions']))
    description_df = pd.DataFrame(description_ohe.toarray(), columns=encodings['description'].get_feature_names_out(['description']))

    # Concatenate the one-hot encoded dataframes with the original dataframe
    input_df = pd.concat([input_df.drop(columns=['UniqueCarrier', 'conditions', 'description']), unique_carrier_df, conditions_df, description_df], axis=1)

    return input_df.values[0]


@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    # input_data_dict = json.loads(input_data)  # Remove this line
    preprocessed_data = preprocess_input(input_data)  # Use input_data directly
    prediction = model.predict(preprocessed_data)
    response = {'prediction': int(prediction[0])}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
