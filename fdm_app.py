from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import psutil, datetime, plotly
from gpiozero import CPUTemperature


cpu_use = []
ram_use = []
timetime = []
cpu_temperature = []
hist = 60

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(["CPU", "RAM"], "CPU", id="monitorizacion_dropdown"),
    html.Div(id="debug_div"),
    dcc.Graph(id='live_graph_monitoring'),
    dcc.Interval(
        id='interval-component',
        interval=2*1000, # in milliseconds
        n_intervals=0
    )
    ])

@app.callback(
    Output('live_graph_monitoring', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('monitorizacion_dropdown', 'value')
    )
def update_output(n, dropdown_option):
    cpu_use.append( psutil.cpu_percent())
    ram_use.append( psutil.virtual_memory()[2])
    cpu_temperature.append( CPUTemperature().temperature)
    timetime.append(datetime.datetime.now().strftime('%H:%M:%S'))  
    
    if dropdown_option == "CPU":
        fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
            'l': 30, 'r': 300, 'b': 30, 't': 10
        }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
        fig.update_yaxes( range=[0,100])
        fig.append_trace({
            'x': timetime[-hist:],
            'y': cpu_use[-hist:],
            'name': 'Cpu use',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)
        fig.append_trace({
            'x': timetime[-hist:],
            'y': cpu_temperature[-hist:],
            'name': 'Cpu temperature',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)

        return fig

    
    elif dropdown_option == "RAM":
        fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
            'l': 30, 'r': 300, 'b': 30, 't': 10
        }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
        fig.update_yaxes( range=[20,90])
        fig.append_trace({
            'x': timetime[-hist:],
            'y': ram_use[-hist:],
            'name': 'Cpu use',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)
    
    return fig

if __name__ == '__main__':
    app.run_server( host = '127.0.0.1', port = 5000, debug=True)