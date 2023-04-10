import dash
from dash import html, dcc

# dash.register_page(__name__, path='/home_2')

pic_link = 'https://images.unsplash.com/photo-1606768666853-403c90a981ad?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8ZmxpZ2h0fGVufDB8fDB8fA%3D%3D&w=1000&q=80'

layout = html.Div(children=[
    html.Div( children=[
        html.H1('Homepage'),
        html.P('Flights in the US'),
        html.Img(src=pic_link, style={'padding':'15px 5px 15px 5px'}),
    ])
    ]
)