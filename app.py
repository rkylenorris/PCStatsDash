from dash import Dash
from dashboard.layout import serve_layout
from dashboard.callbacks import register_callbacks

app = Dash(__name__)
app.title = "PC Stats Dashboard"

app.layout = serve_layout()
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
