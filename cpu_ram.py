import psutil
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--freq', type=int, default=2, help='Frecuencia en segundos. Default 2 sec.')
args = parser.parse_args()

try:
	while True:
		cpu_use = psutil.cpu_percent()
		ram_use = psutil.virtual_memory().percent

		print('Uso del cpu: {}'.format(cpu_use))
		print('Uso de ram: {}'.format(ram_use))
		print('=========================')
		time.sleep(args.freq)
except KeyboardInterrupt:
	print("Stop")
