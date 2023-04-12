FROM python:3.10.6-slim-buster

## Add Python script, requirements file and templates folder to /app 
## directory on the image:

WORKDIR /app/apps

COPY app.py app.py
COPY no_onehot_encoder_dictionary.pkl no_onehot_encoder_dictionary.pkl
COPY XGBoost_model_no_onehot.pkl XGBoost_model_no_onehot.pkl 
COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
