import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Output, Input

# call 
# from apps import navigation
# for every page

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
    "top": 30,
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
        # html.Img(src="assets/plane_icon.png", height="30px"),
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
        )#,
        #dbc.Nav(
        #    [
        #        dbc.NavLink("Home", href="/", active="exact"),
        #        dbc.NavLink("Average Arrival Delays per Month", href=dash.page_registry['pages.arr_delay']['path'], active="exact"),
        #        dbc.NavLink("Page 1", href="/page-1", active="exact"),
        #        dbc.NavLink("Page 2", href="/page-2", active="exact"),
        #    ],
        #    vertical=True,
        #    pills=True,
        #),
    ],
    style=SIDEBAR_STYLE,
)

