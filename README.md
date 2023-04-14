# dsa3101-2220-03-airline

## Installation
```
.
├── backend
│   ├── database 
│   └── model      
├── frontend
├── docker-compose-full.yml
├── docker-compose.yml
└── README.md
```

## Running
Using **Docker** <br>
1. Setting up frontend & backend without database
```
docker compose up -f docker-compose-full.yml
```

2. Setting Up frontend & backend without database
```
docker compose -f docker-compose-full.yml up
```
Note that database itself takes > 24 hours to set up. <br>
So it is recommended to use the pre-populated database on AWS and use the 1st method of setting up.

## Setting up database by itself
Navigate to *backend/model/* and follow instructions in *README.md*