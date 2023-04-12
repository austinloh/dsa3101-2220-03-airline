# pip install dash
import zipfile

import dash
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # or plotly.express as px

# from dash.dependencies.import Input, Output
# import dash_html_components as html
# import dash_core_components as dcc
from dash import Input, Output, callback, dcc, html

# fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

# dash.register_page(__name__, path='/2008flights_2')

# df_zip = zipfile.ZipFile("data/2008_data.csv.zip")
# df = pd.read_csv(df_zip.open("2008_data.csv"))
# airports_df = pd.read_csv("data/airports.csv")

# layout = html.Div(children=[
#
#    html.Div([
#        html.H1('Homepage'),
#        html.P('2008 Flights in the US'),
#        html.Img(),
#        html.Label(),
#        dcc.Dropdown(),
#        html.Br(),
#        html.Label(),
#        dcc.Dropdown(),
#        html.Button()
#    ]),
#    html.Div([
#    ]),
# ])


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

data = pd.read_csv("./airOT201201.csv", dtype=dtypes)  # , parse_dates=parse_dates)

plt.plot(data["FL_DATE"], data["LATE_AIRCRAFT_DELAY"])

by_date = data.groupby("FL_DATE").count().reset_index()

plt.figure(figsize=(16, 10))
plt.plot(by_date["FL_DATE"], by_date["LATE_AIRCRAFT_DELAY"])

coordinates = pd.read_csv("./2011_february_us_airport_traffic.csv")

data2 = data[["FL_DATE", "DEST", "LATE_AIRCRAFT_DELAY"]]
data2.head()

specified = data[
    (data["ORIGIN"] == "JFK")
    & (data["FL_DATE"] == "2012-01-21")
    & (data["CRS_DEP_TIME"] <= 1200)
    & (data["CRS_DEP_TIME"] >= 900)
]

# Possible to group by DATE, CARRIER, AIRCRAFT, ORIGIN, DEST?
# choose origin airport and time, date to consider (e.g. JFK, 2012-01-21)
# show flight from origin airport and departing in time specified to dest airport
# show delays in departure time at origin airport
# show delay in arrival time at dest airport
# show cascading flight from dest airport to new dest airport
# show delay in departure time at dest airport
# show delay in arrival time at new dest airport
# show further breakdown of delay due to weather, NAS, security,... (not available for all)

# departure delay at origin
# origin_d = specified[['FL_DATE', 'UNIQUE_CARRIER', 'TAIL_NUM', 'FL_NUM', 'ORIGIN', 'CRS_DEP_TIME', 'DEP_TIME', 'DEP_DELAY',\
#                      'DEP_DELAY_NEW', 'DEP_DEL15', 'DEP_DELAY_GROUP']]
# arrival delay at dest
# dest_a = specified[['FL_DATE', 'UNIQUE_CARRIER', 'TAIL_NUM', 'FL_NUM',]]
# departure delay at dest

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
#    dtick="M48",
#    tickformat="%H%M")

# breakdown of delay cause for arrival
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

# fig = px.scatter_geo(full, locationmode="USA-states", lat = 'lat', lon = 'long', scope='usa',
#               color=full["mean"].tolist(), size="count", hover_name = 'airport',
#              title = "Arrival Delays at each Airport", labels={'color':'Average delay (min)', 'count':'Number of delays'}, hover_data={'lat':False, 'long':False})

fig = go.Figure()

# flight path
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
# marker for dest airport
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
# marker for origin airport
fig.add_trace(
    go.Scattergeo(
        locationmode="USA-states",
        lon=coordinates[coordinates["iata"] == "JFK"]["long"],
        lat=coordinates[coordinates["iata"] == "JFK"]["lat"],
        # hoverlabel = full['airport'],
        # color = full['mean'].tolist(),
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
        # scope = 'usa',
        scope="north america",
        projection_type="azimuthal equal area",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        countrycolor="rgb(204, 204, 204)",
    ),
    margin=dict(l=20, r=20, t=30, b=20),
)
# fig.show()
# fig.update_layout(legend_title = "Average delay in arrival")

# data3 = data2.groupby('DEST').count().reset_index()

# combine = pd.merge(data3, coordinates, left_on='DEST', right_on='iata')

# import plotly.graph_objects as go

# fig = go.Figure(data=go.Scattergeo(
#        lon = combine['long'],
#        lat = combine['lat'],
#        text = combine['airport'] + ". Total delay time: " + combine['LATE_AIRCRAFT_DELAY'].astype('str'),
#        mode = 'markers',
#        marker_color = combine['cnt'],
#        ))

# fig.update_layout(
#        title = 'Total delay time in 2012 January<br>(Hover for airport names)',
#        geo_scope='usa',
#   )
# fig.show()

layout = html.Div([dcc.Graph(figure=fig)])
