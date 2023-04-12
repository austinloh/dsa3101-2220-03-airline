FROM python:3.10.6-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
COPY app.py app.py
COPY no_onehot_encoder_dictionary.pkl no_onehot_encoder_dictionary.pkl
COPY XGBoost_model_no_onehot.pkl XGBoost_model_no_onehot.pkl

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP app

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]