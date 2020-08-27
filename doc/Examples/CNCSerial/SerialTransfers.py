"""
============
Send byte through serial port
============

Sends a specific byte to a serial port
"""

import serial
import time
import os

filePath = './Programs'
ser = None




def OpenPort( port, baudrate):
    global ser
    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port=port,
        baudrate=baudrate,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS,
        xonxoff=True,              # software flow control
        rtscts=False,               # RTS/CTS flow control
        dsrdtr=False,
        timeout=None                # set a timeout value, None for waiting fore
    )
    ser.isOpen()


def SendX0():
    SendFile('x0.nc')
def SendY0():
    SendFile('y0.nc')
def SendZ0():
    SendFile('z0.nc')
def SendXC():
    SendFile('x_cent_g54.nc')
def SendYC():
    SendFile('y_cent_g54.nc')
def SendZ0_5():
    SendFile('z0.5.nc')
def SendZerFerr():
    SendFile('zero_ferr_mes.nc')
def SendProgram():
    SendFile('Program.nc')

def SendFile(fileName):
    global filePath
    global ser
    for file in os.listdir(filePath):
        if file == fileName:
            print('Found program:' + fileName)
            if ser.isOpen():
                print ("Sending to port: " + str(ser.port) + " Baudrate: " + str(ser.baudrate))
                savedFile = open(filePath + '/' + fileName, 'rb')
                byte = savedFile.read(1)
                while byte:
                    print(byte)
                    ser.write(byte)       
                    byte = savedFile.read(1)           
                savedFile.close
                #ser.close()
            else:
                 print("Port is not open")   



