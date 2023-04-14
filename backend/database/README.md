## Database

### Setting up

In database directory, check the following are present:
- data folder (all data obtained from [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/HG7NV7))
    - flights data csv files compressed using bz2 
    - any other data csv files
- sql-scripts folder
    - CreateTable.sql 
- Dockerfile
- docker-compose-yml
- startup.py
- connectingDB.py
- requirements.txt
- weather2008.py


To create sql data file from csv in data folder, in database directory, run 
```
python3 startup.py
```


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

### Augmenting dataset with weather data
Would have to decompress *2008.csv.bz2* first. <br>
Run
```
python3 weather2008.py
```
This creates a file which contain flights from 2008 and weather data. <br>
To prevent duplicating of tables, remove *2008.csv.bz2* and *States Climate weather data 2008.csv* <br>
Note, this would take very long for docker compose up to run due to the large dataset.

### Current state of database
![](schema.png)