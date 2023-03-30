from dash import Dash, html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SIMPLEX])

# PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app.layout = html.Div([
	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)