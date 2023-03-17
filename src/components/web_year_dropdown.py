import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids

def render_web(app: Dash, data_ad: pd.DataFrame) -> html.Div:
    all_years: list[str] = data_ad[DataSchema.FISCAL_YEAR].tolist()
    unique_years = sorted(set(all_years), key=int)

    @app.callback(
        Output(ids.YEAR_DROPDOWN, 'value'),
        Input(ids.SELECT_ALL_YEARS_BUTTON, 'n_clicks'), 
    )
    def select_all_web_years(_: int) -> list[str]:
        return unique_years

    return html.Div(
        className='col',
        children=[
            html.H6('Fiscal Year', className='m-2'),
            
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{"label": year, "value": year} for year in unique_years],
                value=unique_years,
                multi=True,
                className='col-sm'
            ),
            html.Button(
                className='btn btn-primary btn-sm m-2',
                children=['Select All'],
                id=ids.SELECT_ALL_YEARS_BUTTON,
                n_clicks=0
            ),
        ]
    )