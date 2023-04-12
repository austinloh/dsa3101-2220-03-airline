# 2012 AVERAGE DELAYS

# Import required packages
import zipfile

import dash
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

dtypes = {
    "YEAR": np.int16,
    "MONTH": np.int16,
    "DAY_OF_MONTH": np.int16,
    "DAY_OF_WEEK": np.int16,
    "FL_NUM": np.int16,
    "ORIGIN_AIRPORT_ID": np.int16,
    "DEST_AIRPORT_ID": np.int16,
    "CRS_DEP_TIME": np.int16,
    "DEP_TIME": np.float16,
    "DEP_DELAY": np.float16,
    "DEP_DELAY_NEW": np.float16,
    "DEP_DEL15": np.float16,
    "DEP_DELAY_GROUP": np.float16,
    "TAXI_OUT": np.float16,
    "WHEELS_OFF": np.float16,
    "WHEELS_ON": np.float16,
    "TAXI_IN": np.float16,
    "CRS_ARR_TIME": np.int16,
    "ARR_TIME": np.float16,
    "ARR_DELAY": np.float16,
    "ARR_DELAY_NEW": np.float16,
    "ARR_DEL15": np.float16,
    "ARR_DELAY_GROUP": np.float16,
    "CANCELLED": np.float16,
    "DIVERTED": np.float16,
    "CRS_ELAPSED_TIME": np.float16,
    "ACTUAL_ELAPSED_TIME": np.float16,
    "AIR_TIME": np.float16,
    "FLIGHTS": np.float16,
    "DISTANCE": np.float16,
    "DISTANCE_GROUP": np.int16,
    "CARRIER_DELAY": np.float16,
    "WEATHER_DELAY": np.float16,
    "NAS_DELAY": np.float16,
    "SECURITY_DELAY": np.float16,
    "LATE_AIRCRAFT_DELAY": np.float16,
}

data = pd.read_csv("data/airOT201201.csv", dtype=dtypes)

plt.plot(data["FL_DATE"], data["LATE_AIRCRAFT_DELAY"])

by_date = data.groupby("FL_DATE").count().reset_index()

plt.figure(figsize=(16, 10))
plt.plot(by_date["FL_DATE"], by_date["LATE_AIRCRAFT_DELAY"])

coordinates = pd.read_csv("data/2011_february_us_airport_traffic.csv")

data2 = data[["FL_DATE", "DEST", "LATE_AIRCRAFT_DELAY"]]
data2.head()

specified = data[
    (data["ORIGIN"] == "JFK")
    & (data["FL_DATE"] == "2012-01-21")
    & (data["CRS_DEP_TIME"] <= 1200)
    & (data["CRS_DEP_TIME"] >= 900)
]

px.box(specified["DEP_DELAY"].tolist(), points="all").update_layout(
    xaxis_title="Departure Delays"
)

departure = pd.merge(
    specified[["FL_DATE", "CRS_DEP_TIME", "DEP_DELAY", "DEST"]],
    coordinates,
    left_on="DEST",
    right_on="iata",
)

px.scatter(
    x=pd.to_datetime(
        departure["FL_DATE"] + departure["CRS_DEP_TIME"].astype(str),
        format="%Y-%m-%d%H%M",
    ),
    y=departure["DEP_DELAY"].tolist(),
    color=departure["DEP_DELAY"] > 0,
    color_discrete_sequence=["red", "green"],
    labels={
        "color": "Delay",
        "x": "Scheduled Departure Time",
        "y": "Delay in Departure Time",
    },
    hover_name=departure["airport"],
).update_layout(
    xaxis_title="Scheduled Departure Time",
    yaxis_title="Delay in Departure Time",
    showlegend=False,
)


# Breakdown of delay cause for arrival
px.bar(
    (
        specified[
            [
                "CARRIER_DELAY",
                "WEATHER_DELAY",
                "NAS_DELAY",
                "SECURITY_DELAY",
                "LATE_AIRCRAFT_DELAY",
            ]
        ]
        > 0
    ).sum()
).update_layout(
    xaxis_title="Cause of delay", yaxis_title="Number of delay", showlegend=False
)

arrival = (
    specified.groupby("DEST")["ARR_DELAY"]
    .aggregate(["count", "mean"])
    .reset_index()
    .fillna(0)
)

full = pd.merge(arrival, coordinates, left_on="DEST", right_on="iata")

fig = go.Figure()

# Flight path
for i in range(len(arrival)):
    fig.add_trace(
        go.Scattergeo(
            locationmode="USA-states",
            lon=[
                coordinates[coordinates["iata"] == "JFK"]["long"].iloc[0],
                full["long"][i],
            ],
            lat=[
                coordinates[coordinates["iata"] == "JFK"]["lat"].iloc[0],
                full["lat"][i],
            ],
            mode="lines",
            line=dict(width=1, color="red"),
            opacity=float(full["count"][i]) / float(full["count"].max()),
        )
    )
# Marker for dest airport
fig.add_trace(
    go.Scattergeo(
        locationmode="USA-states",
        lon=full["long"],
        lat=full["lat"],
        # fillcolor = full['mean'],
        hoverinfo="text",
        text=full["airport"],
        mode="markers",
        marker=dict(
            size=2,
            color="lightblue",
            line=dict(
                # width = 5,
                width=full["count"] * 2,
                color=full["mean"].tolist(),
                # color = 'blue'
            ),
        ),
    )
)
# Marker for origin airport
fig.add_trace(
    go.Scattergeo(
        locationmode="USA-states",
        lon=coordinates[coordinates["iata"] == "JFK"]["long"],
        lat=coordinates[coordinates["iata"] == "JFK"]["lat"],
        hoverinfo="text",
        text=coordinates[coordinates["iata"] == "JFK"]["airport"],
        mode="markers",
        marker=dict(size=2, color="lightblue", line=dict(width=5, color="blue")),
    )
)
fig.update_layout(
    title_text="Arrival Delays in Airport",
    showlegend=False,
    geo=dict(
        scope="north america",
        projection_type="azimuthal equal area",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        countrycolor="rgb(204, 204, 204)",
    ),
    margin=dict(l=20, r=20, t=30, b=20),
)

# ------- App layout ----------

layout = html.Div(
    [
        html.H1(
            "Map of Flights with Arrival Delays to JFK Airport",
            style={"text-align": "center"},
        ),
        html.Br(),
        html.H5(
            "Gain a bird's-eye view of JFK airport's flight traffic on a busy day in January 2012 with this flight map visualization - an invaluable tool for optimizing flight patterns and ensuring safe and efficient operations:"
        ),
        html.Br(),
        dcc.Graph(figure=fig),
        html.Br(),
        html.Br(),
        html.H6(
            [("Data taken from: "), html.Em("21 January 2012")],
            style={"fontSize": "70%", "textAlign": "center"},
        ),
    ]
)
