#!/usr/bin/env python
import os
import serial

device_id = os.getenv('LOGNAME')

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
)

try:
    while 1:
        message = input("Mensaje: ")
        message = f'{device_id}~' + message
        message = message + '>'
        ser.write( bytes( message, encoding='utf8'))

except KeyboardInterrupt:
    print("Exiting")
