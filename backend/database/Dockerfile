# Derived from official mysql image (our base image)
FROM mysql:latest
# Add a database
ENV MYSQL_ROOT_PASSWORD supersecret
ENV MYSQL_DATABASE mydb
ENV MYSQL_USER user
ENV MYSQL_PASSWORD pw
# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
#convert data files into sql files
#RUN startup.py

#docker build -t my-mysql .
#docker run -d -p 3306:3306 --name my-mysql -e MYSQL_ROOT_PASSWORD=supersecret my-mysql