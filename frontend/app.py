# app.py
import dash
from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
server = app.server

navbar = dbc.NavbarSimple(
     children=[
        # adding a button for side bar
         dbc.Button("Menu", outline=True, color="light", className="me-1", id="btn_sidebar"),
        # below are establishing the links and how to establish them
        # dbc.NavItem(dbc.NavLink("Home", href="/")),
        # dbc.NavItem(dbc.NavLink("2011 Flights", href="/2011flights")),
	    # dbc.NavItem(dbc.NavLink("2008 Flights", href="/2008flights")),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("Model Showcase", href="/showcase")
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        #),
     ],
     brand="Flight Models",
     brand_href="/",
     color="#343a40",
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
    "background-color": "#7b8a8b",
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
    #"background-color": "#66347F",
}


# the styles for the main content position it to the right of the sidebar and
# add some padding.
#CONTENT_STYLE = {
#    "margin-left": "18rem",
#    "margin-right": "2rem",
#    "padding": "2rem 1rem",
#}

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
               dbc.NavLink("2008 Daily Delays Heatmap", href=dash.page_registry['pages.heatmap']['path'], active="exact"),
               dbc.NavLink("Line Graph Of Of Delays", href=dash.page_registry['pages.line']['path'], active="exact"),
               dbc.NavLink("2008 Flights", href=dash.page_registry['pages.2008flights']['path'], active="exact"),
               dbc.NavLink("2011 Flights", href=dash.page_registry['pages.2011flights']['path'], active="exact"),
               dbc.NavLink("Page 2", href="/page-2", active="exact"),
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
     dcc.Store(id='side_click'), # added this line
     dcc.Location(id="url"), 
     sidebar,
     navbar, 
     content])


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
   elif pathname == dash.page_registry['pages.arr_delay']['path']:
       return dash.page_registry['pages.arr_delay']['layout']
   elif pathname == dash.page_registry['pages.heatmap']['path']:
       return dash.page_registry['pages.heatmap']['layout']
   elif pathname == dash.page_registry['pages.line']['path']:
        return dash.page_registry['pages.line']['layout']
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
       ]#,
       #className="p-3 bg-light rounded-3",
   )

if __name__ == '__main__':
	app.run_server(debug=True)