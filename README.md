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
1. Setting up frontend & backend
```
docker compose up -f docker-compose-full.yml
```
Note that database itself takes > 24 hours to set up. <br>
So it is recommended to use the pre-populated database on AWS and use the 2nd method of setting up.

2. Setting Up frontend & backend without database
```
docker compose up
```

## Setting up database by itself
Navigate to *backend/model/* and follow instructions in *README.md*