import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

pic_link = 'https://images.unsplash.com/photo-1606768666853-403c90a981ad?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8ZmxpZ2h0fGVufDB8fDB8fA%3D%3D&w=1000&q=80'

layout = html.Div(children=[
    html.Div(style={"background-image": "/assets/background.jpeg"}, children=[
        html.H1('Homepage', style={'textAlign': 'center'}),
        html.Br(),
        html.H3("Data is the backbone of modern air traffic control, but it's up to YOU to interpret and use it effectively to ensure safe and efficient operations in the skies."),
        html.Br(),
        html.H5("You need fast and clear data visualizations to make informed decisions in real-time. We have built this resource to provide YOU the essential tools to enhance your situational awareness and manage the complexities of modern air traffic control with confidence."),
        html.Br(),
        html.Img(src=pic_link, style={'width': '70vw', 'padding':'15px 5px 15px 5px'}),
    ])])