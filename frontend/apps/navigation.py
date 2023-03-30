import dash_bootstrap_components as dbc
#import dash_html_components as html
from dash import html
#from app import app
from dash.dependencies import Input, Output, State
import dash

navbar = dbc.NavbarSimple(
     children=[
         dbc.NavItem(dbc.NavLink("Home", href="/")),
         dbc.NavItem(dbc.NavLink("Test", href="/test")),
	     dbc.NavItem(dbc.NavLink("Test2", href="/test2")),
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
