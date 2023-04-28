import pandas as pd
import plotly.express as px
from dash import dcc, html, callback
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids

def render(data: pd.DataFrame) -> html.Div:

    @callback(
        Output(ids.LINE_CHART,'children'),
        [
            Input(ids.STUDIO_YEAR_DROPDOWN, "value"),
            Input(ids.REP_DROPDOWN, 'value'),
        ], prevent_initial_call=True
    )
    
    def update_chart(years: list[str], reps: list[str]) -> html.Div:
        filtered_data = data.query(
            "fiscal_year == @years and sales_rep == @reps"
        )
        if filtered_data.shape[0] == 0:        
            return html.Div("No Data Selected", id=ids.LINE_CHART)

        def grouped_data() -> pd.DataFrame:
            dff = filtered_data.groupby([DataSchema.WEEK, DataSchema.FISCAL_YEAR], as_index=False)[DataSchema.AMOUNT].sum(numeric_only=True)
            return dff  
        try:
            fig = px.line(
                grouped_data(),
                x=DataSchema.WEEK,
                y=DataSchema.AMOUNT,
                color=DataSchema.FISCAL_YEAR,
                line_shape='spline',
                render_mode='svg',
                title='Studio Sales YOY',
                template='plotly_white',
                color_discrete_sequence=['Orange', 'Blue', 'Green']
            )
            fig.update_traces(mode="lines", hovertemplate='%{y:$,.0f}')
            fig.update_layout(hovermode="x unified")
        except Exception:
            fig = px.line(
                grouped_data(),
                x=DataSchema.WEEK,
                y=DataSchema.AMOUNT,
                color=DataSchema.FISCAL_YEAR,
                line_shape='spline',
                render_mode='svg',
                title='Studio Sales YOY',
                template='plotly_white',
                color_discrete_sequence=['Orange', 'Blue', 'Green']
            )
            fig.update_traces(mode="lines", hovertemplate='%{y:$,.0f}')
            fig.update_layout(hovermode="x unified")        
        
        return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART)

    return html.Div(id=ids.LINE_CHART)