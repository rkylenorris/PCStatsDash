from dash import html, dcc
from utils.system_info import get_system_info
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

def bootstrap_badge(text_class):
    mapping = {
        "text-danger": "bg-danger",
        "text-warning": "bg-warning",
        "text-success": "bg-success",
        "text-light": "bg-info"
    }
    return mapping.get(text_class, "bg-secondary")



def serve_layout():
    sys_info = get_system_info()
    
    info_content = html.Ul([
        html.Li([
        html.Span(f"{label}:", style={"width": "120px", "display": "inline-block", "color": "#bbb"}),
        html.Span(info["value"], className=f"badge {bootstrap_badge(info['class'])}")
    ], style={"marginBottom": "0.5rem"}, className="list-group-item")
        for label, info in sys_info.items()
    ], style={"listStyle": "none", "padding": 0, "margin": 0}, className="list-group")

    card = dbc.Card([
        dbc.CardHeader([
            html.Span("System Info", className="text-white"),
            dbc.Button("▼", id="collapse-toggle", size="sm", color="secondary",
                       className="ms-auto", n_clicks=0)
        ], className="d-flex justify-content-between align-items-center bg-secondary"),
        dbc.Collapse(
            dbc.CardBody(info_content),
            id="collapse-body",
            is_open=True
        )
    ], className="mb-4", color="dark", inverse=True)



    return html.Div([
        html.H1("PC Stats Dashboard", className="text-warning"),
        card,
        dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
        dcc.Graph(id='system-gauges')
    ], className="bg-dark p-4")

