#pip install dash
import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import pandas as pd
import plotly.express as px
#from dash.dependencies.import Input, Output
from dash import Input, Output, callback
#from apps import navigation
import zipfile

dash.register_page(__name__)

df_zip = zipfile.ZipFile("data/2008_data.csv.zip")
df = pd.read_csv(df_zip.open("2008_data.csv"))
airports_df = pd.read_csv("data/airports.csv")

layout = html.Div(children=[
    # navigation.navbar,
    # navigation.sidebar,
    html.Div([
        html.H1('Homepage'),
        html.P('2008 Flights in the US'),
        html.Img(),
        html.Label(), 
        dcc.Dropdown(),
        html.Br(),
        html.Label(), 
        dcc.Dropdown(),
        html.Button()
    ]),

    html.Div([
    

    ]),
])