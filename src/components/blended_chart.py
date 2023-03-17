import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema

from . import ids

def render_blend(app: Dash, merged: pd.DataFrame) -> html.Div:
    
    @app.callback(
        Output(ids.BLENDED_LINE_CHART,'children'),
        [
            Input(ids.YEAR_DROPDOWN, "value"),

        ])

    def update_blend_chart(years: list[str]) -> html.Div:
        filtered_data = merged.query(
            "fiscal_year in @years"
        )
        if filtered_data.shape[0] == 0:
            return html.Div("No Data Selected.", id=ids.BLENDED_LINE_CHART)  
        
        def create_chart() ->pd.DataFrame:
            dfm = filtered_data.groupby([DataSchema.WEEK, DataSchema.FISCAL_YEAR], as_index=False)[DataSchema.AMOUNT].sum(numeric_only=True)
            return dfm   

        fig = px.line(
            create_chart(),
            x=DataSchema.WEEK,
            y=DataSchema.AMOUNT,
            color=DataSchema.FISCAL_YEAR,
            line_shape='spline',
            render_mode='svg',
            title='Blended Sales YOY',
            template='plotly_white',
            color_discrete_sequence=['Orange', 'Blue']
        )
        fig.update_traces(mode="markers+lines", hovertemplate='%{y:$,.0f}')
        fig.update_layout(hovermode="x unified")
        
        return html.Div(dcc.Graph(figure=fig), id=ids.BLENDED_LINE_CHART)

    return html.Div(id=ids.BLENDED_LINE_CHART)
