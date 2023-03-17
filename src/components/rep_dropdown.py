import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_reps: list[str] = data[DataSchema.REPS].tolist()
    unique_reps: list[str] = sorted(set(all_reps), key=str)

    @app.callback(
        Output(ids.REP_DROPDOWN, 'value'),
        [
            Input(ids.YEAR_DROPDOWN, 'value'),
            Input(ids.SELECT_ALL_REPS_BUTTON, 'n_clicks'),   
        ],

    )
    def select_all_reps(years: list[str], _: int) -> list[str]:
        filtered_data = data.query("fiscal_year in @years")
        return sorted(set(filtered_data[DataSchema.REPS].tolist()))

    return html.Div(
        children=[
            html.H6('Sales Rep', className='m-2'),      
            dcc.Dropdown(
                id=ids.REP_DROPDOWN,
                options=[{"label": sales_rep, "value": sales_rep} for sales_rep in unique_reps],                
                placeholder='Select a Sales Rep',
                value=unique_reps
            ),

            html.Button(
                className="btn btn-primary btn-sm m-2",
                children=["Select All"],
                id=ids.SELECT_ALL_REPS_BUTTON,
                n_clicks=0,
            ),

        ]
    )