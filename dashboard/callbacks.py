import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collectors.system_stats import get_system_stats

stats_log = []

def register_callbacks(app):
    @app.callback(
        [Output('cpu-usage', 'figure'),
         Output('ram-usage', 'figure'),
         Output('gpu-usage', 'figure'),
         Output('network-traffic', 'figure')],
        Input('interval-component', 'n_intervals')
    )
    def update_metrics(n):
        global stats_log
        stats = get_system_stats()
        stats_log.append(stats)
        df = pd.DataFrame(stats_log[-20:])

        # CPU
        fig_cpu = go.Figure(go.Scatter(x=df['time'], y=df['cpu'], mode='lines+markers'))
        fig_cpu.update_layout(title='CPU Usage (%)', yaxis=dict(range=[0, 100]))

        # RAM
        fig_ram = go.Figure(go.Scatter(x=df['time'], y=df['ram'], mode='lines+markers'))
        fig_ram.update_layout(title='RAM Usage (%)', yaxis=dict(range=[0, 100]))

        # GPU
        fig_gpu = go.Figure()
        if df['gpu_load'].notna().any():
            fig_gpu.add_trace(go.Scatter(x=df['time'], y=df['gpu_load'], mode='lines+markers', name='GPU Load'))
            fig_gpu.add_trace(go.Scatter(x=df['time'], y=df['gpu_mem'], mode='lines+markers', name='GPU Memory'))
        fig_gpu.update_layout(title='GPU Stats (%)', yaxis=dict(range=[0, 100]))

        # Network
        fig_net = go.Figure()
        fig_net.add_trace(go.Scatter(x=df['time'], y=df['bytes_sent'], mode='lines+markers', name='Bytes Sent'))
        fig_net.add_trace(go.Scatter(x=df['time'], y=df['bytes_recv'], mode='lines+markers', name='Bytes Received'))
        fig_net.update_layout(title='Network Traffic (Bytes)')

        return fig_cpu, fig_ram, fig_gpu, fig_net
