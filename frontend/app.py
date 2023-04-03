# app.py
import dash
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
server = app.server

navbar = dbc.NavbarSimple(
     children=[
        # below are establishing the links and how to establish them
         dbc.NavItem(dbc.NavLink("Home", href="/")),
         dbc.NavItem(dbc.NavLink("2011 Flights", href="/2011flights")),
	     dbc.NavItem(dbc.NavLink("2008 Flights", href="/2008flights")),
         dbc.DropdownMenu(
             children=[
                 dbc.DropdownMenuItem("More pages", header=True),
                 dbc.DropdownMenuItem("Model Showcase", href="/showcase")
             ],
             nav=True,
             in_navbar=True,
             label="More",
         ),
     ],
     brand="Flight Models",
     brand_href="/",
     color="primary",
     dark=True,
     fluid=True,
     links_left=True,
     sticky='Top'  
 )

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "4rem 2rem 1rem",
    "background-color": "#66347F",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        #html.Img(src="assets/plane_icon.png", height="30px"),
        dbc.Row(
            [
                dbc.Col(html.A([html.Img(src="assets/plane_icon.png", height="50px")], 
                               href="/")), #clicking on icon returns to homepage too
                dbc.Col(html.H1("Menu")),
            ],
        align="center",     
        ),
        # html.H1("Menu"),
        html.Hr(),
        html.P(
            "Visualize US airline data from between January to April 2008"
        ),
        dbc.Nav(
           [
               dbc.NavLink("Home", href="/", active="exact"),
               dbc.NavLink("Average Arrival Delays per Month", href=dash.page_registry['pages.arr_delay']['path'], active="exact"),
               dbc.NavLink("2008 Flights", href=dash.page_registry['pages.2008flights']['path'], active="exact"),
               dbc.NavLink("2011 Flights", href=dash.page_registry['pages.2011flights']['path'], active="exact"),
               dbc.NavLink("Page 2", href="/page-2", active="exact"),
           ],
           vertical=True,
           pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE, children=[dash.page_container])

app.layout = html.Div([dcc.Location(id="url"), navbar, sidebar, content])

# app.layout = html.Div([
# 	dash.page_container
# ])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])

def render_page_content(pathname):
   if pathname == "/":
        return dash.page_registry['pages.home']['layout']
   elif pathname == dash.page_registry['pages.arr_delay']['path']:
       return dash.page_registry['pages.arr_delay']['layout']
   elif pathname == dash.page_registry['pages.2008flights']['path']:
       return dash.page_registry['pages.2008flights']['layout']
   elif pathname == dash.page_registry['pages.2011flights']['path']:
       return dash.page_registry['pages.2011flights']['layout']
   elif pathname == "/page-1":
       return html.P("This is the content of page 1. Yay!")
   elif pathname == "/page-2":
       return html.P("Oh cool, this is page 2!")
   # If the user tries to reach a different page, return a 404 message
   return html.Div(
       [
           html.H1("404: Not found", className="text-danger"),
           html.Hr(),
           html.P(f"The pathname {pathname} was not recognised..."),
       ],
       className="p-3 bg-light rounded-3",
   )

if __name__ == '__main__':
	app.run_server(debug=True)