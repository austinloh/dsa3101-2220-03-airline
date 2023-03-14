CREATE TABLE flights (
    Year SMALLINT;
    Month SMALLINT;
    DayofMonth SMALLINT;
    DayOfWeek SMALLINT;
    DepTime SMALLINT;
    CRSDepTime SMALLINT;
    ArrTime SMALLINT;
    CRSArrTime SMALLINT;
    UniqueCarrier VARCHAR(6);
    FlightNum SMALLINT;
    TailNum VARCHAR(10);
    ActualElapsedTime SMALLINT;
    CRSElapsedTime SMALLINT;
    AirTime SMALLINT;
    ArrDelay SMALLINT;
    DepDelay SMALLINT;
    Origin VARCHAR(3);
    Dest VARCHAR(3):
    Distance INT;
    TaxiIn SMALLINT;
    TaxiOut SMALLINT;
    Cancelled BIT;
    Cancellation VARCHAR(1);
    Diverted BIT;
    CarrierDelay SMALLINT;
    WeatherDelay SMALLINT;
    NASDelay SMALLINT;
    SecurityDelay SMALLINT;
    LateAircraftDelay SMALLINT;
    PRIMARY KEY(Year, Month, DayofMonth, CRSDepTime, TailNum);
)

