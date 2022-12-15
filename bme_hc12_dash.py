from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import psutil, datetime, plotly
from gpiozero import CPUTemperature
import pandas as pd
import datetime
import os
import serial

temp=[]
hum=[]
press=[]
time_instant=[]
hist = 20

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2)

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(["Temperatura", "Humedad", "Presión"], "Temperatura", id="monitorizacion_dropdown"),
    html.Div(id="debug_div"),
    dcc.Graph(id='live_graph_monitoring'),
    dcc.Interval(
        id='interval-component',
        interval=3*1000,
        n_intervals=0
    )])



@app.callback(
    Output('live_graph_monitoring', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('monitorizacion_dropdown', 'value')
    )
def update_output(n, dropdown_option):
	global temp, hum, press, time_instant

	x=ser.readline()
	message = x.decode("utf8").split(',')
	row_dict = {}
	try:
		for i in message:
			row_dict[ i.split(':')[0] ]=  i.split(':')[1]
		print(row_dict)
		
		time_instant.append( datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		temp.append( float( row_dict["T"]) )
		hum.append( float( row_dict["H"]) )
		press.append( float( row_dict["P"]) )

		temp = temp[-hist:]
		hum = hum[-hist:]
		press = press[-hist:]
		time_instant = time_instant[-hist:]



	except:
		print("Sin datos")


	data_to_plot = None
	if dropdown_option == "Temperatura":
		data_to_plot = temp
		ran = [-10,40]
	elif dropdown_option == "Humedad":
		data_to_plot = hum
		ran = [0,100]
	elif dropdown_option == "Presión":
		data_to_plot = press
		ran = [800,1200]

	fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
	fig['layout']['margin'] = {
		'l': 30, 'r': 300, 'b': 30, 't': 10
	}
	fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
	fig.update_layout(yaxis_range=ran )
	fig.append_trace({
		'x': time_instant,
		'y': data_to_plot,
		'name': dropdown_option,
		'mode': 'lines+markers',
		'type': 'scatter'
	}, 1, 1)

	return fig


if __name__ == '__main__':
	app.run_server( host = '127.0.0.1', port = 5000, debug=True)