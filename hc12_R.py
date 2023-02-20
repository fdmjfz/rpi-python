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

        device_info = items_list[0]
        device_type = device_info[0]
        device_id = device_info[1:]

        text = items_list[1]

        if device_type == 'u':
            output = f'{device_id}: {text}'
            print(output)

except KeyboardInterrupt:
    print("Exiting")
