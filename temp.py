from gpiozero import CPUTemperature
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--freq', type=int, default=2, help='Frecuencia en segundos. Default 2 sec.')
args = parser.parse_args()

try:
	while True:
		cpu_temp = CPUTemperature().temperature
		print( f'Temperatura del cpu: {cpu_temp}')
		time.sleep(args.freq)
except KeyboardInterrupt:
	print("Stop")
