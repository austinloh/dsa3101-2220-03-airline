import pickle
import numpy as np
from flask import Flask, request, jsonify
import xgboost as xgb
import pandas as pd

app = Flask(__name__)

# Load the XGBoost model
with open("XGBoost_model_no_onehot.pkl", "rb") as f:
    model = pickle.load(f)

# Load the label encodings
with open("no_onehot_encoder_dictionary.pkl", "rb") as f:
    encoding_dict = pickle.load(f)

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
    print("Input data:")
    print(input_data)
    preprocessed_data = preprocess_input(input_data)
    print("Preprocessed data:")
    print(preprocessed_data)
    prediction = model.predict(preprocessed_data.reshape(1, -1))
    print("Model prediction:")
    print(prediction)
    response = {'prediction': int(prediction[0])}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
