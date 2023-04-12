# main.py

import dash
from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
server = app.server

navbar = dbc.NavbarSimple(
     children=[
        # Adding a button for side bar
        dbc.Button("Menu", outline=True, color="light", className="me-1", id="btn_sidebar")
     ],
     brand="Flight Models",
     brand_href="/",
     color="#212529",
     dark=True,
     fluid=True,
     links_left=True,
     sticky="top"  
 )

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 71,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "position": "fixed",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "1rem 1rem",
    "background-color": "#343a40",
}

SIDEBAR_HIDDEN = {
    "position": "fixed",
    "top": 71,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "1rem 1rem",
}

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "0rem",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        dbc.Row([
            dbc.Col(html.A([html.Img(src="assets/plane_icon.png", height="50px")], href="/")), 
            # Clicking on icon returns to homepage too
            dbc.Col(html.H1("Menu"))],
        align="center",     
        style={'color':"#fff"}
        ),
        html.Hr(),
        html.H6(
            "Data is the artist, but interpretation is the brushstroke that creates a masterpiece.",
            style={'fontSize':'80%', 'padding':'1px 1px 1px 1px', 'color':"#fff"}
        ),
        dbc.Nav(
           [
               dbc.NavLink("Home", href="/", active="exact"),
               dbc.NavLink("Line Graph Of Delays", href=dash.page_registry['pages.line']['path'], active="exact"),
               dbc.NavLink("Arrival Delay Times", href=dash.page_registry['pages.avgdelays']['path'], active="exact"),
               dbc.NavLink("Heatmap of Daily Delays", href=dash.page_registry['pages.heatmap']['path'], active="exact"),
            #    dbc.NavLink("Flight Map", href=dash.page_registry['pages.2012delays']['path'], active="exact"),
               dbc.NavLink("Breakdown by State", href=dash.page_registry['pages.2011flights']['path'], active="exact"),
               dbc.NavLink("Tinker With Data", href=dash.page_registry['pages.model']['path'], active="exact"),

           ],
           vertical=True,
           pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE, children=[dash.page_container])

app.layout = html.Div([
     dcc.Store(id='side_click'),
     dcc.Location(id="url"), 
     sidebar,
     navbar, 
     content
     ])


@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [State("side_click", "data")]
)

def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])

def render_page_content(pathname):
   if pathname == "/":
        return dash.page_registry['pages.home']['layout']
   elif pathname == dash.page_registry['pages.avgdelays']['path']:
       return dash.page_registry['pages.avgdelays']['layout']
   elif pathname == dash.page_registry['pages.heatmap']['path']:
       return dash.page_registry['pages.heatmap']['layout']

   elif pathname == dash.page_registry['pages.line']['path']:
       return dash.page_registry['pages.line']['layout']

#    elif pathname == dash.page_registry['pages.2012delays']['path']:
#        return dash.page_registry['pages.2012delays']['layout']

   elif pathname == dash.page_registry['pages.2011flights']['path']:
       return dash.page_registry['pages.2011flights']['layout']
   elif pathname == dash.page_registry['pages.model']['path']:
       return dash.page_registry['pages.model']['layout']
   
   # If the user tries to reach a different page, return a 404 message
   return html.Div(
       [
           html.H1("404: Not found", className="text-danger"),
           html.Hr(),
           html.P(f"The pathname {pathname} was not recognised..."),
       ]
   )

if __name__ == '__main__':
	app.run_server(debug=True)