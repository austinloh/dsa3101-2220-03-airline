import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

pic_link = 'https://images.unsplash.com/photo-1606768666853-403c90a981ad?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8ZmxpZ2h0fGVufDB8fDB8fA%3D%3D&w=1000&q=80'


layout = html.Div(children=[
    html.Div(children=[
        html.H1('Homepage', style={'textAlign': 'center'}),
        html.Br(), 
        html.Img(src=pic_link, style={'height':'50%', 'width':'50%'}),
        html.Br(),
        html.H3("Welcome to Flight Models! This is a webpage to help you predict plane delays."),
                #Use it effectively to ensure safe and efficient operations in the skies.
        html.Br(),
        html.H5("As an Air Traffic Controller like yourself, you need fast and clear data visualizations to make informed decisions in real-time. Hence, we have built this resource to provide you with the essential tools to enhance your situational awareness and manage the complexities of modern air traffic control with confidence."),
        html.Br(), 
        html.H5("To navigate this page, use the 'Menu' button on the top left corner of the page to display the side navigation bar."),
        html.Br(),
        html.H5("The side bar consists of different pages that focuses on different features to help you anticipate a delay."),
        html.Br()
    ])])