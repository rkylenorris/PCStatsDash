import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from data_collection.system_stats import get_system_stats
from utils.formatter import format_bytes

prev_net = {"bytes_sent": 0, "bytes_recv": 0}

stats_log = []

def register_callbacks(app):
    @app.callback(
        [Output('system-gauges', 'figure')],
        Input('interval-component', 'n_intervals')
    )
    def update_metrics(n):
        global stats_log
        stats = get_system_stats()
        stats_log.append(stats)
        df = pd.DataFrame(stats_log[-20:])
        
        global prev_net
        delta_sent = stats['bytes_sent'] - prev_net['bytes_sent']
        delta_recv = stats['bytes_recv'] - prev_net['bytes_recv']
        prev_net['bytes_sent'] = stats['bytes_sent']
        prev_net['bytes_recv'] = stats['bytes_recv']

        # Convert to Megabits per second
        net_mbps = ((delta_sent + delta_recv) * 8) / 1_000_000  # Bytes → bits → megabits

        
        
        cpu = stats['cpu']
        gpu = stats['gpu_load'] or 0
        ram = stats['ram']
        net_sent = stats['bytes_sent']
        net_recv = stats['bytes_recv']
        net_total = (net_sent + net_recv) / (1024 ** 2)  # in MB

        fig = go.Figure()

        # CPU
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=cpu,
            title={'text': "CPU Usage (%)"},
            domain={'row': 0, 'column': 0},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': 'orange'}}
        ))

        # GPU
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=gpu,
            title={'text': "GPU Usage (%)"},
            domain={'row': 0, 'column': 1},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': 'lightgreen'}}
        ))

        # RAM
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=ram,
            title={'text': "RAM Usage (%)"},
            domain={'row': 1, 'column': 0},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': 'lightblue'}}
        ))

        # Network
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=net_mbps,
            title={'text': "Net Speed (Mbps)"},
            domain={'row': 1, 'column': 1},
            gauge={'axis': {'range': [0, 1000]}, 'bar': {'color': 'violet'}}
        ))


        fig.update_layout(
            grid={'rows': 2, 'columns': 2, 'pattern': "independent"},
            paper_bgcolor="rgb(30,30,30)",
            font={'color': "white"}
        )

        return [fig]

        # # Disk usage
        # # Disk usage
        # fig_disk = go.Figure()
        # fig_disk.add_trace(go.Scatter(x=df['time'], y=df['disk_percent'], mode='lines+markers', name='Disk Usage %'))

        # # Convert bytes to MB/GB for tooltip display (leave axis raw for chart scaling)
        # read_labels = [format_bytes(val) for val in df['disk_read']]
        # write_labels = [format_bytes(val) for val in df['disk_write']]

        # fig_disk.add_trace(go.Scatter(
        #     x=df['time'], y=df['disk_read'],
        #     mode='lines+markers', name='Bytes Read',
        #     hovertext=read_labels, hoverinfo='text+name+x'
        # ))
        # fig_disk.add_trace(go.Scatter(
        #     x=df['time'], y=df['disk_write'],
        #     mode='lines+markers', name='Bytes Written',
        #     hovertext=write_labels, hoverinfo='text+name+x'
        # ))
        # fig_disk.update_layout(title='Disk Usage and IO')



        # # CPU
        # fig_cpu = go.Figure(go.Scatter(x=df['time'], y=df['cpu'], mode='lines+markers'))
        # fig_cpu.update_layout(title='CPU Usage (%)', yaxis=dict(range=[0, 100]))
        
        # # Per-core CPU usage (latest only)
        # per_core_usage = stats['cpu_per_core']
        # core_fig = go.Figure()
        # for i, usage in enumerate(per_core_usage):
        #     core_fig.add_trace(go.Bar(x=[f'Core {i}'], y=[usage], name=f'Core {i}'))
        # core_fig.update_layout(title='CPU Usage by Core (%)', yaxis=dict(range=[0, 100]), barmode='group')


        # # RAM
        # fig_ram = go.Figure(go.Scatter(x=df['time'], y=df['ram'], mode='lines+markers'))
        # fig_ram.update_layout(title='RAM Usage (%)', yaxis=dict(range=[0, 100]))

        # # GPU
        # fig_gpu = go.Figure()
        # if df['gpu_load'].notna().any():
        #     fig_gpu.add_trace(go.Scatter(x=df['time'], y=df['gpu_load'], mode='lines+markers', name='GPU Load'))
        #     fig_gpu.add_trace(go.Scatter(x=df['time'], y=df['gpu_mem'], mode='lines+markers', name='GPU Memory'))
        # if 'gpu_temp' in df and df['gpu_temp'].notna().any():
        #     fig_gpu.add_trace(go.Scatter(x=df['time'], y=df['gpu_temp'], mode='lines+markers', name='GPU Temp (°C)'))
        # fig_gpu.update_layout(title='GPU Stats', yaxis=dict(range=[0, 100]))


        # # Network
        # net_sent = [format_bytes(val) for val in df['bytes_sent']]
        # net_recv = [format_bytes(val) for val in df['bytes_recv']]

        # fig_net = go.Figure()
        # fig_net.add_trace(go.Scatter(x=df['time'], y=df['bytes_sent'],
        #                             mode='lines+markers', name='Bytes Sent',
        #                             hovertext=net_sent, hoverinfo='text+name+x'))
        # fig_net.add_trace(go.Scatter(x=df['time'], y=df['bytes_recv'],
        #                             mode='lines+markers', name='Bytes Received',
        #                             hovertext=net_recv, hoverinfo='text+name+x'))
        # fig_net.update_layout(title='Network Traffic')


        # return fig_cpu, core_fig, fig_ram, fig_gpu, fig_net, fig_disk

    @app.callback(
        Output("collapse-body", "is_open"),
        Input("collapse-toggle", "n_clicks"),
        State("collapse-body", "is_open")
    )
    def toggle_collapse(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open
