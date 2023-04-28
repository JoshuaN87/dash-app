from dash import html
import dash_bootstrap_components as dbc
import dash

from src.components import (
    web_year_dropdown,
    line_chart_web,
)

from src.data.loader import (
    load_additional_data,
    load_blended_data,
)

dash.register_page(__name__, path='/', top_nav=True)

DATA_PATH_2 = "/Users/joshuaniewiadomski/data_app/data/blended_sales.csv"
data_ad = load_additional_data(DATA_PATH_2)
data_blend = load_blended_data(DATA_PATH_2)


layout = dbc.Container(
        [
            dbc.Row(
                dbc.Col(html.H1(
                    "Web Sales Dashboard",
                    className='text-center text-primary py-4'),
                    width =12)
            ),
            dbc.Row([
                dbc.Col([
                    web_year_dropdown.render(data_blend)
                ]),


            ], justify='start'),   

            dbc.Row([
                dbc.Col(
                    children=[
                    line_chart_web.render_web(data_ad)
                ],xs=12,sm=12,md=12,lg=12,xl=12
                ),
            ], justify='start'),

            dbc.Row([
                dbc.Col(
                    children=[
                    line_chart_web.render_blend(data_blend)
                ],xs=12,sm=12,md=12,lg=12,xl=12
                ),

            ], justify='start'),      
    
        ],
    )