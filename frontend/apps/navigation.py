import dash_bootstrap_components as dbc
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

