# TINKER WITH DATA

# Import required packages
import dash
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import requests
import json

dash.register_page(__name__)

# Import of images from assets folder
delay_yes = '../assets/delay_yes.png'
delay_no = '../assets/delay_no.png'
delay_or_not = '../assets/delay_or_not.png'

# Default values for remaining non-customizable feature columns
input_data = {
    'Year': 2006,
    'Month': 1,
    'DayofMonth': 11,
    'DayOfWeek': 3,
    'CRSDepTime': 1053,
    'CRSArrTime': 1318,
    'UniqueCarrier': 'US',
    'TailNum': 'N834AW',
    'CRSElapsedTime': 265.0,
    'Origin': 'ATL',
    'Dest': 'PHX',
    'Distance': 1587,
    'origin_state': 'GA',
    'tempmax': 2.1,
    'tempmin': -4.6,
    'temp': -0.1,
    'feelslikemax': 1.3,
    'feelslikemin': -4.6,
    'feelslike': -0.6,
    'dew': -0.9,
    'humidity': 94.6, # 94.6
    'precip': 1.573,
    'precipcover': 8.33,
    'snow': 0.0,
    'snowdepth': 0.6,
    'windgust': 57.685756,
    'windspeed': 25.6, # 10.5
    'winddir': 90.0,
    'sealevelpressure': 1030.7,
    'cloudcover': 98.5,
    'visibility': 6.6,
    'moonphase': 0.39,
    'conditions': 'Snow, Rain, Overcast',
    'description': 'Cloudy skies throughout the day with rain or snow.'
}
headers = {"Content-Type": "application/json"}

def generate_pred(DayOfWeek, CRSDepTime, origin_state):
    input_dict = input_data.copy()
    if DayOfWeek and CRSDepTime and origin_state:
        input_dict['DayOfWeek'] = DayOfWeek
        input_dict['CRSDepTime'] = CRSDepTime
        input_dict['origin_state'] = origin_state
        # '0' for no delay, '1' for delay
        # if running locally instead of in dockerised: use http://127.0.0.1:5001/predict
        return str(requests.post('http://model:5000/predict', data=json.dumps(input_dict), headers=headers).json()['prediction'])
    # '2' for no full user input yet
    return '2'


#------- App Layout ----------

layout = html.Div(children=[
    html.Br(),

    html.H1(id='prediction_text', style={'textAlign': 'center'}),

    html.Br(),
    html.Br(),

    html.H3([html.Strong("Data: where knowledge meets opportunity.")]),
    html.H5(" We looked at data from over a million flights and built a simple model from it, so YOU don't have to. Among the top factors that determine if a flight will be delayed, we handpicked these 3 for YOU to customize. Try our tool to take a look at how these 3 factors affect a flight's delay:"),
    
    html.Br(),
    html.Br(),

    dbc.Row([
        html.H6("Flight Origin:", style={'textAlign': 'center'}),
        html.Br(),
        dcc.Dropdown(
            id='origin_state',
            options = ['AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'FL', 'GA', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY'],
            placeholder="Select state...",
            style={'color': 'black', 'width':'300px', 'margin':'0px auto'}
        )
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.H6("Day of Week:", style={'textAlign': 'center'}),
            dcc.Slider(
                id='DayOfWeek',
                min=1,
                max=7,
                marks={1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat', 7:'Sun'},
                value=3,
                vertical=True,
            )
        ]),
        dbc.Col([
            html.H6("Scheduled Departure Hour:", style={'textAlign': 'center'}),
            dcc.Slider(
                id='CRSDepTime',
                min=0,
                max=23,
                marks={i: f"{('0'+str(i))[-2:]}:00" for i in range(24)},
                value=11,
                vertical=True
            )
        ])
    ]),

    html.Div([
        html.Img(id='prediction_img', style={"width": "70vw", "margin": "0 auto"})
    ]),

    html.Br(),
    html.Br(),

    html.H6([('Data taken from: '), html.Em('2006 - 2008')], style={'fontSize':'70%', 'textAlign': 'center'})

])

# ----- Interactivity between Dash Components -----

@callback(
    [Output(component_id='prediction_text', component_property='children'),
    Output(component_id='prediction_img', component_property='src')],
    [Input(component_id='DayOfWeek', component_property='value'),
    Input(component_id='CRSDepTime', component_property='value'),
    Input(component_id='origin_state', component_property='value')]
)

def update_output(DayOfWeek, CRSDepTime, origin_state):
    pred = generate_pred(DayOfWeek, CRSDepTime, origin_state)
    if pred=='0':
        # return delay_no
        return "No delay!", delay_no
    elif pred=='1':
        # return delay_yes
        return "DELAY", delay_yes
    else:
        # return delay_or_not
        return "Will the flight be delayed?", delay_or_not
