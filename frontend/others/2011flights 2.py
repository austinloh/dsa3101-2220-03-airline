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

# dash.register_page(__name__, path='/2011flights_2')

flights = pd.read_csv("2011_february_us_airport_traffic.csv")
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

	html.H1('US Flights'),
	html.Div(children = [
		html.Div(
			children = [
				html.H2('Select State'),
				dcc.Dropdown(
					id='state_dd',
					options = [{'label':state, 'value':state}
								for state in sorted(list(flights.state.dropna().unique()))],
					style = {'width':'200px', 'margin':'0px auto'}
				)
			],
			style = {
				'width':'350px', 'height':'150px',
				'vertical-align':'top',
				'border':'1px solid black', 'padding':'20px', 'margin':'0px auto'
			}
		),
		html.Div(
			children = [
				dcc.Graph(id='bar_graph',
	      			style = {'height':'1000px', 'margin':'0px auto'}
	      		),
				html.H3('Testing Site', style = {
					'border':'2px solid black',
					'width':'200px', 'margin':'0px auto'
				})
			],
			style = {'width':'700px', 'margin':'0px auto'}
		)
	])
],
style = {'text-align':'center', 'display':'inline-block', 'width':'100%'}
)

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
