# Visualizing 2008 delays in heatmap

# Import required packages
import zipfile

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from plotly_calplot import calplot

dash.register_page(__name__)

# ------ Importing and pre processing of data -------------

df_zip = zipfile.ZipFile("data/2008_data.csv.zip")
df = pd.read_csv(df_zip.open("2008_data.csv"))

df = df.loc[
    df["Cancelled"] == 0, ["Year", "Month", "DayofMonth", "ArrDelay", "DepDelay"]
]
df = df.rename(columns={"DayofMonth": "Day"})
df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])

arr_df = df[["Date", "ArrDelay"]]
arr_df = arr_df.groupby(["Date"])["ArrDelay"].sum().to_frame().reset_index()

dep_df = df[["Date", "DepDelay"]]
dep_df = dep_df.groupby(["Date"])["DepDelay"].sum().to_frame().reset_index()

arr_fig = calplot(
    arr_df,
    x="Date",
    y="ArrDelay",
    years_title=True,
    end_month=4,
    title="2008 Daily Arrival Delays (mins)",
    name="Total arrival delay(mins)",
    colorscale="amp",
    showscale=True,
    month_lines_width=3,
    month_lines_color="#fff",
)

dep_fig = calplot(
    dep_df,
    x="Date",
    y="DepDelay",
    end_month=4,
    years_title=True,
    title="2008 Daily Departure Delays (mins)",
    name="Total departure delay(mins)",
    colorscale="amp",
    showscale=True,
    month_lines_width=3,
    month_lines_color="#fff",
)

# ------- App layout -------------

layout = html.Div(
    children=[
        html.H1("Heatmap of US Flight Delays by Day", style={"text-align": "center"}),
        html.Br(),
        html.H5(
            "Stay ahead of the curve and proactively manage flight delays with this insightful Heatmap visualization showcasing flight delays over days in 2008 - an essential tool for predicting potential delays and improving overall flight scheduling:"
        ),
        html.Br(),
        dcc.Dropdown(
            id="delay_type",
            options=[
                {"label": "Arrival", "value": "arrival"},
                {"label": "Departure", "value": "delay"},
            ],
            multi=False,
            placeholder="Select delay type...",
            # value = "arrival",
            style={"color": "black", "width": "300px", "margin": "0px auto"},
            # className="dropdown"
        ),
        html.Br(),
        dcc.Graph(id="my_heatmap", figure={}, style={"backgroundColor": "transparent"}),
        html.Br(),
        html.Br(),
        html.P(
            "Observe how regardless of arrival or departure delay, the Friday rows in general have higher delays, \
           indicated by darker red pixels!"
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H6(
            [("Data taken from: "), html.Em("January - April 2008")],
            style={"fontSize": "70%", "textAlign": "center"},
        ),
    ]
)


@callback(
    [Output(component_id="my_heatmap", component_property="figure")],
    [Input(component_id="delay_type", component_property="value")],
)
def update_graph(option_selected):
    if option_selected == "arrival":
        return [arr_fig]
    else:
        return [dep_fig]
