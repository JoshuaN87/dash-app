from dash import Dash
from dash_bootstrap_components.themes import LUX

from src.components.layout import create_layout
from src.data.loader import load_transaction_data, load_additional_data, merge

#DATA_PATH = "https://raw.githubusercontent.com/JoshuaN87/dash-app/main/data/studiosalesdataResults.csv"
#DATA_PATH_2 = "https://raw.githubusercontent.com/JoshuaN87/dash-app/main/data/web_sales_combined.csv"

#loading data and creating the data manager
data = load_transaction_data(DATA_PATH)
data_ad = load_additional_data(DATA_PATH_2)
merged = merge(data, data_ad)

app = Dash(external_stylesheets=[LUX])

app.title = 'Sales Dashboard'
app.layout = create_layout(app, data, data_ad, merged)

if __name__ == "__main__":
    app.run_server(debug=False)

