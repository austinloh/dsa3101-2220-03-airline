## Database

### Setting up

In database directory, check the following are present:
- data folder
    - data csv files compressed using bz2 ([data](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/HG7NV7))
- sql-scripts folder
    - CreateTable.sql 
- Dockerfile
- docker-compose-yml
- startup.py
- connectingDB.py
- requirements.txt

In database directory, run 
```
python3 startup.py
```
to create sql data file from csv in data folder

Next, run
```
docker compose up
```
to setup SQL database

### Connecting
Ensure docker container is running on aws
We have provided a test file to showcase querying from SQL database

Run
```
pip install -r requirements.txt
```

In *connectingDB.py*, change aws ip address, path to pem file and SQL query to execute
Run
```
python3 connectingDB.py
```