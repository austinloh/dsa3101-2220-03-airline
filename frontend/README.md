## **README for frontend**
Before running `docker compose up` you should have at least these in your current directory:
```
.
├── assets
|   ├── plane_icon.png
│   └── style.css
├── data
|   ├── 2008_data_csv.zip
|   └── airports.csv
├── pages
|   ├── home.py
|   ├── 2008flights.py
|   ├── 2011flights.py
|   └── arr_delay.py
├── app.py
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```
### **To run**
```
docker compose up
```
You should now have the container running and access the webpage on localhost:8000. 

