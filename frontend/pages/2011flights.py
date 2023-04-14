# 2011 FLIGHTS BY STATE AND CITY

# Import required packages
import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

dash.register_page(__name__)

# ------ importing of data -------------

flights = pd.read_csv("data/2011_february_us_airport_traffic.csv")

# ------- App layout ----------

layout = html.Div(
    children=[
        html.H1("All US Flights by State and City", style={"text-align": "center"}),
        html.Br(),
        html.H5(
            "Get a comprehensive overview of flight traffic across the United States with this interactive bargraph showcasing the breakdown of flight counts by city for every state in February 2011 - a powerful tool for optimizing flight routes, managing resources, and ensuring smooth operations:"
        ),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="state_dd",
                            placeholder="Select state...",
                            options=[
                                {"label": state, "value": state}
                                for state in sorted(
                                    list(flights.state.dropna().unique())
                                )
                            ],
                            style={
                                "color": "black",
                                "width": "200px",
                                "margin": "0px auto",
                            },
                        )
                    ],
                    style={"width": "350px", "height": "90px", "margin": "0px auto",},
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id="bar_graph",
                            style={"height": "1000px", "margin": "0px auto"},
                        ),
                    ],
                    style={"width": "700px", "margin": "0px auto"},
                ),
            ],
            style={"text-align": "center", "display": "inline-block", "width": "100%"},
        ),
        html.Br(),
        html.Br(),
        html.H6(
            [("Data taken from: "), html.Em("February 2011")],
            style={"fontSize": "70%", "textAlign": "center"},
        ),
    ]
)

# ----- Interactivity between Dash Components -----


@callback(
    Output(component_id="bar_graph", component_property="figure"),
    Input(component_id="state_dd", component_property="value"),
)
def update_plot(selection):
    filter = "All States"
    flights2 = flights.copy(deep=True)
    if selection:
        filter = selection
        flights2 = flights2[flights2["state"] == filter]
    flights2 = (
        flights2.groupby(["city"])["cnt"]
        .agg("sum")
        .reset_index(name="Total Flight Count")
        #.sort_values(by=["cnt"])
    )
    flights_bar = px.bar(
        title=f"Flights in {filter} in Feb 2011",
        data_frame=flights2,
        x="Total Flight Count",
        y="city",
        orientation="h",
        color="city",
    ).update_yaxes(categoryorder='total ascending')
    return flights_bar
