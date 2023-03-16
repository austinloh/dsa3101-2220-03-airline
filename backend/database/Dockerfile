# Derived from official mysql image (our base image)
FROM mysql:latest
# Add a database
# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/

#convert data files into sql files
#FROM python:3.10.6-slim-buster
#COPY startup.py startup.py
#ENTRYPOINT ["python3", "startup.py"] 
#RUN python startup.py
#ENTRYPOINT [ "echo", "*" ]

#docker build -t my-mysql .
#docker run -d -p 3306:3306 --name my-mysql -e MYSQL_ROOT_PASSWORD=supersecret my-mysql