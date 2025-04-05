import dash_bootstrap_components as dbc
from dash import Dash
from dashboard.layout import serve_layout
from dashboard.callbacks import register_callbacks

# Use a dark Bootstrap theme (e.g., "CYBORG")
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.title = "PC Stats Dashboard"

app.layout = serve_layout()
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
