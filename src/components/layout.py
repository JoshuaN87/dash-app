from dash import  Dash, html
import dash_bootstrap_components as dbc
from src.components import (
    line_chart,
    year_dropdown,
    rep_dropdown,
    line_chart_web,
    blended_chart,
)

def create_layout(app: Dash, data=None, data_ad=None, merged=None) -> dbc.Container:

    return dbc.Container([
        dbc.Row(
            dbc.Col(html.H1(
                app.title, 
                className='text-center text-primary py-4'),
                width =12)
        ),
        dbc.Row([
            dbc.Col([
                year_dropdown.render(app,data),
                line_chart_web.render_web(app, data_ad),
            ],xs=12,sm=12,md=12,lg=6,xl=6
            ),
            dbc.Col([
                rep_dropdown.render(app, data),
                line_chart.render(app, data),
            ],xs=12,sm=12,md=12,lg=6,xl=6
            ),
        ], justify='start'),    
        dbc.Row([
            dbc.Col([
                blended_chart.render_blend(app, merged),
            ],xs=12,sm=12,md=12,lg=12,xl=12
            ),
        ], justify='start')        
    ])