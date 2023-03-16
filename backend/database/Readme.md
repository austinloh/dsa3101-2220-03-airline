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
How to connect to database?