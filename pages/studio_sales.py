from dash import html
import dash
import dash_bootstrap_components as dbc

from src.components import (
    year_dropdown,
    rep_dropdown,
    line_chart,
    studio_bar_chart,
    studio_pie
)
from src.data.loader import load_transaction_data

dash.register_page(__name__, top_nav=True)

DATA_PATH = "/Users/joshuaniewiadomski/data_app/data/blended_sales.csv"
data = load_transaction_data(DATA_PATH)


layout = dbc.Container(
        [
            dbc.Row(
                dbc.Col(html.H1(
                    "Studio Sales Dashboard",
                    className='text-center text-primary py-4'),
                    width =12)
            ),
            dbc.Row([
                dbc.Col([
                    year_dropdown.render(data)
                ]),
                dbc.Col([
                    rep_dropdown.render(data)
                        ])

            ], justify='start'),   

            dbc.Row([
                dbc.Col(
                    children=[
                    line_chart.render(data)
                ],xs=12,sm=12,md=12,lg=12,xl=12
                ),
            ], justify='start'),

            dbc.Row([
                dbc.Col(
                    children=[
                    studio_bar_chart.render_bar(data)
                ],xs=12,sm=12,md=12,lg=8,xl=8
                ),
                dbc.Col(
                    children=[
                    studio_pie.render_pie(data)
                ],xs=12,sm=12,md=12,lg=4,xl=4
                ),
            ], justify='start'),      
    
        ],
    )