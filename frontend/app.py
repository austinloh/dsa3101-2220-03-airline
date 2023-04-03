# app.py
import dash
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
server = app.server

# content = html.Div(id="page-content", style=CONTENT_STYLE, children=[dash.page_container])

# app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

app.layout = html.Div([
	dash.page_container
])


# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])

#def render_page_content(pathname):
#    if pathname == "/":
#         return html.P("This is our home page! :D")
#    elif pathname == dash.page_registry['pages.arr_delay']['path']:
#        return dash.page_registry['pages.arr_delay']['layout']
#    elif pathname == "/page-1":
#        return html.P("This is the content of page 1. Yay!")
#    elif pathname == "/page-2":
#        return html.P("Oh cool, this is page 2!")
#    # If the user tries to reach a different page, return a 404 message
#    return html.Div(
#        [
#            html.H1("404: Not found", className="text-danger"),
#            html.Hr(),
#            html.P(f"The pathname {pathname} was not recognised..."),
#        ],
#        className="p-3 bg-light rounded-3",
#    )

if __name__ == '__main__':
	app.run_server(debug=True)