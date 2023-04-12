# Visualizing delays with CRSDepTime
import pandas as pd
import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import zipfile

dash.register_page(__name__)
# line = Dash(__name__)

# df_zip = zipfile.ZipFile("data/2008_data.csv.zip")
df_zip = zipfile.ZipFile("data/2008_data.csv.zip")
df = pd.read_csv(df_zip.open("2008_data.csv"))

#-------- Importing and pre processing of data ---------
# Get all non-cancelled flights
df = df.loc[df['Cancelled']==0, ["CRSDepTime", "ArrDelay", "DepDelay"]]
df["ArrDelay"] = df["ArrDelay"].fillna(0)
df["DepDelay"] = df["DepDelay"].fillna(0)

arr_df = df[["CRSDepTime","ArrDelay"]]
arr_df = arr_df.groupby(["CRSDepTime"])["ArrDelay"].mean().to_frame().reset_index()
arr_df = arr_df.drop_duplicates()

dep_df = df[["CRSDepTime","DepDelay"]]
dep_df = dep_df.groupby(["CRSDepTime"])["DepDelay"].mean().to_frame().reset_index()
dep_df = dep_df.drop_duplicates()

#--------- App layout ---------------
layout = html.Div([

    html.H1("Average Delays With Scheduled Departure Timings (24 hour format)"),

    html.Br(),

    html.P("Hover over the visualization to see the CRSDepTime and corresponding average delay for that timing"),
    html.P("Example 1: (440, 76) means at 4:40 am, the average delay is 76 minutes."),
    html.P("Example 2: (1645, 25) means at 4:45 pm, the average delay is 25 minutes."),
    html.P("You may notice some flat lines that occur over regular intervals, that is due to time not having minutes \
           between 60 and 99, as 24 hour time jumps from XX59 to XX00."),

    html.Br(),

    html.Label(['Select Delay Type'], style={'font-weight': 'bold', "text-align": "center"}),

    dcc.Dropdown(id='delay_type',
                 options=[
                    {"label": "Arrival", "value":"arrival"},
                    {"label": "Departure", "value":"departure"},
                    {"label": "Both Arrival And Departure", "value":"both"}],
                multi=False,
                placeholder="Select delay type",
                value = "arrival",
                className="dropdown"
                ),

    html.Br(),

    dcc.Graph(id='line_plot', figure={})
])

@callback(
    [Output(component_id='line_plot',component_property='figure')],
    [Input(component_id='delay_type',component_property='value')])

def update_graph(option_selected):
    temp_arr_df = arr_df.copy()
    temp_dep_df = dep_df.copy()

    if option_selected == "arrival":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=temp_arr_df["CRSDepTime"], y=temp_arr_df["ArrDelay"], name='Arrival Delay',
                         line=dict(color='firebrick', width=3)))
        fig.update_layout(title='Average Arrival Delays With CRSDepTime (Scheduled Departure Time)',
                   xaxis_title='CRSDepTime (in 24 hour Format)',
                   yaxis_title='Delay (in minutes)')

    elif option_selected == "departure":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=temp_dep_df["CRSDepTime"], y=temp_dep_df["DepDelay"], name='Departure Delay',
                         line=dict(color='royalblue', width=3)))
        fig.update_layout(title='Average Departure Delays With CRSDepTime (Scheduled Departure Time)',
                   xaxis_title='CRSDepTime (in 24 hour Format)',
                   yaxis_title='Delay (in minutes)')

    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=temp_arr_df["CRSDepTime"], y=temp_arr_df["ArrDelay"], name='Arrival Delay',
                         line=dict(color='firebrick', width=3)))
        fig.add_trace(go.Scatter(x=temp_dep_df["CRSDepTime"], y=temp_dep_df["DepDelay"], name='Departure Delay',
                         line=dict(color='royalblue', width=3)))
        fig.update_layout(title='Arrival & Departure Delays With CRSDepTime (Scheduled Departure Time)',
                   xaxis_title='CRSDepTime (in 24 hour Format)',
                   yaxis_title='Delay (in minutes)')
    return [fig] 

# if __name__ == '__main__':
#     line.run_server(debug=True)