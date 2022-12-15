from matplotlib import pyplot as plt
import matplotlib.animation as animation
from gpiozero import CPUTemperature
import datetime as dt
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--freq', type=int, default=2, help='Frecuencia en segundos. Default 2 sec.')
parser.add_argument('--hist_lenght', type=int, default=10, help='Longitud del histórico.')
args = parser.parse_args()

history = []
counter = []

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

def animate(i, counter, history):
    cpu_temp = CPUTemperature().temperature
    
    counter.append(dt.datetime.now().strftime('%S'))
    history.append(cpu_temp)

    counter = counter[-args.hist_lenght:]
    history = history[-args.hist_lenght:]

    ax.clear()
    ax.plot(counter, history)

    plt.subplots_adjust(bottom=0.30)
    plt.title('Cpu Temperature {}'.format(cpu_temp))
    plt.ylim(30,80)


try:
    ani = animation.FuncAnimation(fig, animate, fargs=(counter, history), interval=1000)
    plt.show()

except KeyboardInterrupt:
    print("Stopping")