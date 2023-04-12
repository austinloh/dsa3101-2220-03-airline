# VISUALIZING ARRIVAL DELAYS IN 2008

# Import required packages
import zipfile

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

dash.register_page(__name__)

# ------ importing and pre processing of data -------------

df_zip = zipfile.ZipFile("data/2008_data.csv.zip")
df = pd.read_csv(df_zip.open("2008_data.csv"))
airports_df = pd.read_csv("data/airports.csv")

airports_df = airports_df.loc[:, ["iata", "airport", "lat", "long"]].sort_values(
    by="iata"
)

# Using only non-cancelled flights data
month_delay_df = df.loc[df["Cancelled"] == 0, ["Month", "ArrDelay", "Dest"]]
month_delay_df = month_delay_df.rename(columns={"Dest": "iata"})

# Average arrival delay (mins) for each arrival destination each month
month_delay_df["AvgArrDelay"] = month_delay_df.groupby(["iata", "Month"])[
    "ArrDelay"
].transform("mean")
month_delay_df = (
    month_delay_df.loc[:, ["iata", "Month", "AvgArrDelay"]]
    .drop_duplicates()
    .sort_values(by=["iata", "Month"])
)

month_airports_df = pd.merge(month_delay_df, airports_df, on="iata")

# ------- App layout ----------

layout = html.Div(
    children=[
        html.H1(
            "US Airport Average Arrival Delays By Month", style={"text-align": "center"}
        ),
        html.Br(),
        dcc.Dropdown(
            id="select_month",
            options=[
                {"label": "January", "value": 1},
                {"label": "February", "value": 2},
                {"label": "March", "value": 3},
                {"label": "April", "value": 4},
            ],
            multi=False,
            value=1,
            style={"color": "black", "width": "300px", "margin": "0px auto"},
        ),
        html.Br(),
        html.Div(id="output_container", children=[], style={"text-align": "center"}),
        # html.P("Hover over the map to see the average arrival delay in minutes for the current selected month"),
        html.Br(),
        dcc.Graph(id="my_map", figure={}),
        html.Br(),
        html.Br(),
        html.H6(
            [("Data taken from: "), html.Em("January - April 2008")],
            style={"fontSize": "70%", "textAlign": "center"},
        ),
    ],
    className="container",
    style={"backgroundColor": "lightpurple"},
)

# ----- Interactivity with Dash Components -----


@callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="my_map", component_property="figure"),
    ],
    [Input(component_id="select_month", component_property="value")],
)
def update_graph(option_selected):

    month_dict = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    container = "Hover over the map to see the average arrival delay in minutes for: {}".format(
        month_dict[option_selected]
    )

    temp_df = month_airports_df.copy()
    temp_df = temp_df[temp_df["Month"] == option_selected]

    # Plotly Express (PX)
    fig = px.scatter_geo(
        data_frame=temp_df,
        lat=temp_df["lat"],
        lon=temp_df["long"],
        hover_name=temp_df["airport"],
        scope="usa",
        color=temp_df["AvgArrDelay"],
        hover_data=["AvgArrDelay"],
        color_continuous_scale=px.colors.sequential.Sunsetdark,
    )

    return container, fig
