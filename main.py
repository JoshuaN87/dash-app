from dash import Dash
from dash_bootstrap_components.themes import LUX
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, use_pages=True, external_stylesheets=[LUX])

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Pages",
    ),
    brand="Lightopia",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container
    ], 
        fluid=True, 
        className="dbc",
)

if __name__ == "__main__":
    app.run_server(debug=True)