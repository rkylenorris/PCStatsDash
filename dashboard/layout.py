from dash import html, dcc

def serve_layout():
    return html.Div([
        html.H1("PC Stats Dashboard"),
        dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
        dcc.Graph(id='cpu-usage'),
        dcc.Graph(id='ram-usage'),
        dcc.Graph(id='gpu-usage'),
        dcc.Graph(id='network-traffic'),
    ])
