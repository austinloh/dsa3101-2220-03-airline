CREATE TABLE flights (
    Year SMALLINT,
    Month SMALLINT,
    DayofMonth SMALLINT,
    DayOfWeek SMALLINT,
    DepTime SMALLINT,
    CRSDepTime SMALLINT,
    ArrTime SMALLINT,
    CRSArrTime SMALLINT,
    UniqueCarrier VARCHAR(7) REFERENCES carriers(Code),
    FlightNum SMALLINT,
    TailNum VARCHAR(10) REFERENCES planes(tailnum),
    ActualElapsedTime SMALLINT,
    CRSElapsedTime SMALLINT,
    AirTime SMALLINT,
    ArrDelay SMALLINT,
    DepDelay SMALLINT,
    Origin VARCHAR(3) REFERENCES airports(iata),
    Dest VARCHAR(3) REFERENCES airports(iata),
    Distance INT,
    TaxiIn SMALLINT,
    TaxiOut SMALLINT,
    Cancelled SMALLINT,
    Cancellation VARCHAR(1),
    Diverted SMALLINT,
    CarrierDelay SMALLINT,
    WeatherDelay SMALLINT,
    NASDelay SMALLINT,
    SecurityDelay SMALLINT,
    LateAircraftDelay SMALLINT,
    PRIMARY KEY(Year, Month, DayofMonth, CRSDepTime, CRSArrTime, FlightNum, TailNum)
);

CREATE TABLE carriers (
    Code VARCHAR(7) PRIMARY KEY,
    Description VARCHAR(150)
);

CREATE TABLE airports (
    iata VARCHAR(3) PRIMARY KEY,
    airport VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    latitude DECIMAL(7,4),
    longitude DECIMAL(7,4)
);

CREATE TABLE planes (
    tailnum VARCHAR(10) PRIMARY KEY,
    type VARCHAR(50),
    manufacturer VARCHAR(100),
    issue_date VARCHAR(10),
    model VARCHAR(30),
    status VARCHAR(10),
    aircraft_type VARCHAR(100),
    engine_type VARCHAR(100),
    year YEAR
);