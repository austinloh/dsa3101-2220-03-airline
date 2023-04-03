# Visualizing 2008 delays in heatmap
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import zipfile

#dash.register_page(__name__)
heatmap = Dash(__name__)

# df_zip = zipfile.ZipFile("data/2008_data.csv.zip")
df_zip = zipfile.ZipFile("/Users/wanyan/Documents/DSA3101/dsa3101-2220-03-airline/frontend/data/2008_data.csv.zip")
df = pd.read_csv(df_zip.open("2008_data.csv"))

#------ importing and pre processing of data -------------
df = df.loc[df['cancelled']==0, ["Month", "DayofMonth", "ArrDelay", "DepDelay"]]



#------- App layout -------------
heatmap.layout = html.Div(children=[
    
    html.H1("Heatmap of delays over days in 2008", style={'text-align':'center'}),

])