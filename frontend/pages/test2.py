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
from apps import navigation

dash.register_page(__name__)

flights08 = pd.read_csv("2008_data.csv")

layout = html.Div(children=[
    navigation.navbar,
    html.Div([
        html.H1('Homepage'),
        html.P('Flights in the US'),
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