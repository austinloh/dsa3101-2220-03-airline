FROM python:3.10.6-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
COPY app.py app.py
COPY no_onehot_encoder_dictionary.pkl no_onehot_encoder_dictionary.pkl
COPY XGBoost_model_no_onehot.pkl XGBoost_model_no_onehot.pkl
# ADD XGBoost_api_no_onehot XGBoost_api_no_onehot
# COPY lightgbm lightgbm
# COPY NeuralNetwork NeuralNetwork
# COPY StatisticalTest StatisticalTest
# COPY XGBoost_api XGBoost_api
# COPY Time_Series_Analysis Time_Series_Analysis

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
#RUN python fit_model.py

ENV FLASK_APP app

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]