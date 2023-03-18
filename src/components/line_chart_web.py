import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids

def render_web(app: Dash, data_ad: pd.DataFrame) -> html.Div:
  
    @app.callback(
        Output(ids.LINE_CHART_WEB,'children'),
        [
            Input(ids.YEAR_DROPDOWN, "value"),

        ])
    def update_chart_web(years: list[str]) -> html.Div:
        filtered_data = data_ad.query(
            "fiscal_year == @years"
        )
        if filtered_data.shape[0] == 0:        
            return html.Div('No Data Selected', id=ids.LINE_CHART_WEB)
        def grouped_web() -> pd.DataFrame:
            dfw = filtered_data.groupby([DataSchema.WEEK, DataSchema.FISCAL_YEAR], as_index=False)[DataSchema.AMOUNT].sum(numeric_only=True)
            return dfw

        fig = px.line(
            grouped_web(),
            x=DataSchema.WEEK,
            y=DataSchema.AMOUNT,
            color=DataSchema.FISCAL_YEAR,
            title='Web Sales YOY',
            line_shape='spline',
            render_mode='svg',
            template='plotly_white',
            color_discrete_sequence=['Orange', 'Blue']
        )
        fig.update_traces(mode="lines", hovertemplate='%{y:$,.0f}')
        fig.update_layout(hovermode="x unified")        
        
        return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART_WEB)

    return html.Div(id=ids.LINE_CHART_WEB)