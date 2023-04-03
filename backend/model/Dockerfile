FROM python:3.10.6-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py 
COPY lightgbm lightgbm
COPY NeuralNetwork NeuralNetwork
COPY StatisticalTest StatisticalTest
COPY XGBoost_api XGBoost_api
COPY Time_Series_Analysis Time_Series_Analysis

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
#RUN python fit_model.py

ENV FLASK_APP main

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]