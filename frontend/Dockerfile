FROM python:3.10.6-slim-buster

## Add Python script, requirements file and templates folder to /app 
## directory on the image:

WORKDIR /app

COPY app.py app.py
COPY requirements.txt requirements.txt
COPY data data
COPY assets assets
COPY pages pages

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
