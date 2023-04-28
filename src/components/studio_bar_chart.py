import pandas as pd
import plotly.express as px
from dash import dcc, html, callback
from dash.dependencies import Input, Output

from . import ids

def render_bar(data: pd.DataFrame) -> html.Div:

    @callback(
        Output(ids.STUDIO_BAR,'children'),
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

        fig = px.bar(grouped_data(), x="gross_sales", y="day", color='sales_rep', orientation='h',
                    hover_data={"aov": ":$.2f","number_of_sales":":.0f", "week":":.0f"},
                    height=500,
                    labels={"gross_sales":"Total Sales", "day":"Day"},
                    title='Studio Sales')
        
        #fig.update_traces(hovertemplate='%{y:$,.0f}')
        #fig.update_layout(hovermode="x unified")

        return html.Div(dcc.Graph(figure=fig), id=ids.STUDIO_BAR)

    return html.Div(id=ids.STUDIO_BAR)