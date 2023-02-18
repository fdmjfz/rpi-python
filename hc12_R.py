import time
import serial

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
)

try:
    while True:
        x=ser.read_until(bytes('>', encoding='utf-8'))
        message = x.decode('utf-8')
        message = message.replace('>', '')

        items_list = message.split('~')
        device_id = items_list[0]
        text = items_list[1]

        output = f'{device_id}: {text}'
        print(output)

except KeyboardInterrupt:
    print("Exiting")
