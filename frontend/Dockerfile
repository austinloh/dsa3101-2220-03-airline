FROM python:3.10.6-slim-buster

## Add Python script, requirements file and templates folder to /app 
## directory on the image:

WORKDIR /frontend

COPY main.py main.py
COPY requirements.txt requirements.txt
ADD data data
ADD assets assets
ADD pages pages

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP=main.py

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
