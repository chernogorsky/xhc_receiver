"""
============
Send byte through serial port
============

Sends a specific byte to a serial port
"""

import serial
import time
import os

filePath = 'Programs'
fileName = 'x0.nc'

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM6',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    xonxoff=False,              # software flow control
    rtscts=False,               # RTS/CTS flow control
    timeout=None                # set a timeout value, None for waiting fore
)

ser.isOpen()

def SendFile():
    global filePath
    global fileName 
    for file in os.listdir(filePath):
        if file == fileName:
            print('Found program:' + fileName)
            savedFile = open(filePath + '/' + fileName, 'rb')
            byte = savedFile.read(1)
            while byte:
                print(byte)
                ser.write(byte)       
                byte = savedFile.read(1)           
            savedFile.close

SendFile()
ser.close()
