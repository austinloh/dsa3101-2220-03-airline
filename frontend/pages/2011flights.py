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

dash.register_page(__name__)

flights = pd.read_csv("data/2011_february_us_airport_traffic.csv")
#flights = flights.groupby(['state'])['cnt'].agg('sum').reset_index(name='Total Flight Count')
#flights_bar = px.bar(data_frame=flights, x='Total Flight Count', y='state', orientation='h', title='Total Flights by State')


# app = dash.Dash(__name__)

#app.layout = html.Div(children = [
#	html.Div(style={'background-color':'lightblue'}),
#	html.H1("2011 Feb US Airport Traffic"),
#	dcc.Graph(id='bar_graph', figure=flights_bar)
#	]
#)
layout = html.Div(children=[
	html.H1("All US Flights by State and City", style={'text-align':'center'}),
    html.Br(),
	html.H5("Get a comprehensive overview of flight traffic across the United States with this interactive bargraph showcasing the breakdown of flight counts by city for every state in February 2011 - a powerful tool for optimizing flight routes, managing resources, and ensuring smooth operations:"),
	html.Br(),
	html.Div(children = [
		html.Div(
			children = [
				# html.H3('Select State'),
				dcc.Dropdown(
					id='state_dd',
					placeholder="Select state...",
					options = [{'label':state, 'value':state}
								for state in sorted(list(flights.state.dropna().unique()))],
					style = {'color': 'black', 'width':'200px', 'margin':'0px auto'}
				)
			],
			style = {
				'width':'350px', 'height':'90px',
				# 'vertical-align':'top',
				# 'border':'1px solid black', 'padding':'20px',
				'margin':'0px auto',
			}
		),
		html.Div(
			children = [
				dcc.Graph(id='bar_graph',
	      			style = {'height':'1000px', 'margin':'0px auto'}
	      		),
				# html.H3('Testing Site', style = {
				# 	'border':'2px solid black',
				# 	'width':'200px', 'margin':'0px auto'
				# })
			],
			style = {'width':'700px', 'margin':'0px auto'}
		)
	], style = {'text-align':'center', 'display':'inline-block', 'width':'100%'}),
	html.Br(),
	html.Br(),
    html.H6([('Data taken from: '), html.Em('February 2011')], style={'fontSize':'70%', 'textAlign': 'center'})
])

@callback(
	Output(component_id='bar_graph', component_property='figure'),
	Input(component_id='state_dd', component_property='value')
)
def update_plot(selection):
	filter = "All States"
	flights2 = flights.copy(deep=True)
	if selection:
		filter = selection
		flights2 = flights2[flights2['state'] == filter]
	flights2 = flights2.groupby(['city'])['cnt'].agg('sum').reset_index(name='Total Flight Count')
	flights_bar = px.bar(title=f'Flights in {filter} in Feb 2011', data_frame=flights2,
		      	x='Total Flight Count', y='city', orientation='h',
				color='city')
	return flights_bar



#if __name__ == '__main__':
#	app.run_server(debug=True)
