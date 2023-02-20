#!/usr/bin/env python
import os
import serial
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

GPIO.output(12, GPIO.HIGH)

device_id = os.getenv('LOGNAME')
device_type = 'u'

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    timeout=1,
)

while True:
    message = input("Mensaje: ")

    if message == 'HIGH':
        GPIO.output(12, GPIO.HIGH)
    elif message == 'LOW':
        GPIO.output(12, GPIO.LOW)
    ser.write( bytes( message, encoding='utf-8'))

    for i in range(0, 6):
        response = ser.readline()
        response = response.decode('utf-8')
        if len(response) > 1:
            print(response)
