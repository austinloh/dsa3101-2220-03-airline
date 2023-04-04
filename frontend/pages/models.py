# Visualizing models
import dash
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go

import requests
import json
from IPython.core.display import HTML

# app = dash.Dash(__name__)
dash.register_page(__name__)


#------ importing and pre processing of data -------------

# h1 = {'Content-type': 'application/json', 'Accept': 'application/json'}
#['Month','DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime', 'UniqueCarrier',
#       'TailNum', 'CRSElapsedTime', 'Origin', 'Dest', 'Distance']
# params1 = {'inputs': [3, 28, 5, 635, 912, 'YV', 'N956LR', 97.0, 'MEM', 'CLT', 512]}
# feature_importance = str(requests.get('http://127.0.0.1:5000/api/lime_fi',headers=h1, json=params1).json())

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
# prediction = str(requests.post('http://127.0.0.1:5000/predict', data=json.dumps(input_data), headers=headers).json()['prediction'])



def generate_pred(DayOfWeek, CRSDepTime, origin_state):
    input_dict = input_data.copy()
    if DayOfWeek:
        input_dict['DayOfWeek'] = DayOfWeek
    if CRSDepTime:
        input_dict['CRSDepTime'] = CRSDepTime
    if origin_state:
        input_dict['origin_state'] = origin_state
    return str(requests.post('http://127.0.0.1:5000/predict', data=json.dumps(input_dict), headers=headers).json()['prediction'])


#------- App layout ----------

layout = html.Div(children=[
    # html.H2(feature_importance),
    html.Br(),
    # html.H2(prediction),
    # dcc.DatePickerSingle(
    #     id='year_month_date',
    #     date=date(2006, 1, 11),
    #     min_date_allowed=date(2006, 1, 1),
    #     max_date_allowed=date(2008, 12, 31)
    # ),
    html.H1(id='prediction_text'),
    dcc.Slider(
        id='DayOfWeek',
        min=1,
        max=7,
        marks={1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat', 7:'Sun'},
        value=3,
        # vertical=False
    ),
    dcc.Slider(
        id='CRSDepTime',
        min=0,
        max=47,
        marks={i: f"{i//2}{'30' if i%2 else '00'}" for i in range(48)},
        value=22,
        # vertical=False
    ),
    dcc.Dropdown(
        id='origin_state',
        options = ['AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'FL', 'GA', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY'],
        style={'color': 'black'},
    ) 
])

# ----- Connect Plotly graphs with Dash Components -----

@callback(
    Output(component_id='prediction_text', component_property='children'),
    [Input(component_id='DayOfWeek', component_property='value'),
    Input(component_id='CRSDepTime', component_property='value'),
    Input(component_id='origin_state', component_property='value')]
)

def update_output(DayOfWeek, CRSDepTime, origin_state):
    pred = generate_pred(DayOfWeek, CRSDepTime, origin_state)
    if pred=='0':
        return "No delay :)"
    else:
        return "DELAY"


# ---------------------------------------
# if __name__ == '__main__':
#     app.run_server(debug=True)
