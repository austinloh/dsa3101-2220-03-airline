# Visualizing arrival delays in 2008
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import zipfile

app = Dash(__name__)

df_zip = zipfile.ZipFile("data/2008_data.csv.zip")
df = pd.read_csv(df_zip.open("2008_data.csv"))
iata_df = pd.read_csv("data/iata-icao.csv")

#------ importing and pre processing of data -------------

# Obtain US iata airport codes
us_iata = iata_df.loc[iata_df["country_code"]=="US", 
                      ["iata","airport","longitude","latitude"]].sort_values(by="iata")

# Using only non-cancelled flights data
month_delay_df = df.loc[df["Cancelled"] == 0, ["Month","ArrDelay","Dest"]]
month_delay_df = month_delay_df.rename(columns={"Dest":"iata"})
# Average arrival delay (mins) for each arrival destination each month
month_delay_df["AvgArrDelay"] = month_delay_df.groupby(["iata","Month"])["ArrDelay"].transform("mean")
month_delay_df = month_delay_df.loc[:, ["iata","Month","AvgArrDelay"]].drop_duplicates().sort_values(by=["iata","Month"])

month_iata_df = pd.merge(month_delay_df, us_iata, on="iata") 
#After merging, 9 rows were lost, not sure why, could be no record of iata code

#------- App layout ----------

app.layout = html.Div(style={'backgroundColor': 'lightpurple'}, children=[

    html.H1("Average Arrival Delay In Destination Airports", style={'text-align':'center'}),

    dcc.Dropdown(id="select_month",
                 options=[
                    {"label": "January", "value":1},
                    {"label": "February", "value":2},
                    {"label": "March", "value":3},
                    {"label": "April", "value":4}],
                multi=False,
                value=1,
                #style={'width': "40%"},
                className="dropdown"
                ),
    
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_map', figure={})

], className="container")

# ----- Connect Plotly graphs with Dash Components -----
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='my_map', component_property='figure')],
    [Input(component_id='select_month', component_property='value')]
)

def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))

    month_dict = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
                  7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
    
    container = "The month chosen was: {}".format(month_dict[option_selected])

    temp_df = month_iata_df.copy()
    temp_df = temp_df[temp_df["Month"]==option_selected]

    # Plotly Express (PX)
    fig = px.scatter_geo(data_frame = temp_df, 
                         lat = temp_df["latitude"], 
                         lon = temp_df["longitude"], 
                        #  locationmode = 'USA-states',
                         hover_name = temp_df["airport"],
                         scope = "usa",
                         color = temp_df["AvgArrDelay"],
                         hover_data = ["AvgArrDelay"],
                         color_continuous_scale = px.colors.sequential.Agsunset,
                         template = 'plotly_dark'
                         )

    return container, fig

# ---------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
