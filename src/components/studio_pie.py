import pandas as pd
import plotly.express as px
from dash import dcc, html, callback
from dash.dependencies import Input, Output

from . import ids

def render_pie(data: pd.DataFrame) -> html.Div:

    @callback(
        Output(ids.STUDIO_PIE,'children'),
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
            return html.Div("No Data Selected", id=ids.STUDIO_BAR)

        def grouped_data() -> pd.DataFrame:

            dff = filtered_data.groupby(['sales_rep','day','week', 'fiscal_year'],as_index=False)\
                    [['number_of_sales','gross_sales']].sum()

            dff['aov'] = dff['gross_sales']/dff['number_of_sales']
            return dff  

        fig = px.sunburst(grouped_data(), path=['day', 'sales_rep'], 
                  values='gross_sales', color='day',
                  width=500, height=500)
        
        #fig.update_traces(hovertemplate='%{y:$,.0f}')
        #fig.update_layout(hovermode="x unified")

        return html.Div(dcc.Graph(figure=fig), id=ids.STUDIO_PIE)

    return html.Div(id=ids.STUDIO_PIE)