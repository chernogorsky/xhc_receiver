"""
============
Compensation Table Receive
============

Reads compensation tables from eccentric drive and saves to a file.
"""

import serial
import time

filePath = 'Tables'


ThermDriftColumns = 15
ThermDriftLines = 21
ThermDriftTable = [[0 for y in range(ThermDriftColumns)] for x in range(ThermDriftLines)] 
ID =''


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM12',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

def GetID():
    global ID
    ID = SerialSendReceive(0xffff, False, 0)
    if ID != False:
        print('Connected to device: ' + ID)
    else:
        print('no device found on ' + str(ser.port))

def ReceiveTable():
    global ThermDriftColumns
    global ThermDriftLines
    global ThermDriftTable
    for j in range(ThermDriftColumns):
        for i in range(ThermDriftLines):
            iParamAdress = j*21 + i + 0x1492
            sParamValue = SerialSendReceive(iParamAdress, False, 0)
            #print(str(iParamAdress) +' = ' +  sParamValue)
            #print (str(i) + ' ' + str(j))            
            ThermDriftTable[i][j] = sParamValue
    print("Table successfully received")
        
def SaveTable():
    global filePath
    global ThermDriftColumns
    global ThermDriftLines
    global ThermDriftTable
    global ID

    file  = open(filePath + '/' + ID +'.csv', 'w')
    file.write('(########################################################)\n')
    file.write('(#                                                      #)\n')
    file.write('(#  Eccentric Drive - Thermal drift compensation data   #)\n')    
    file.write('(#         Fernando Figueiredo - DaGmaRobotics®         #)\n')
    file.write('(#                                                      #)\n')
    file.write('(########################################################)\n')
    file.write('\n')
    file.write('Ref,Temp,S1Amp,S1Off,S2Amp,S2Off,S3Amp,S3Off,S4Amp,S4Off,S5Amp,S5Off,S6Amp,S6Off,S7Amp,S7Off\n')
    for i in range(ThermDriftLines):
        file.write(str(i))
        for j in range(ThermDriftColumns):
            file.write(','+str(ThermDriftTable[i][j]))
        file.write('\n')
    file.close
    print("Table successfully saved")





def SerialSendReceive(iParameter, xWrite, sNewValue): 
    answer=''
    sParameter = "{0:#0{1}x}".format(iParameter,6)#hex(iParameter)
    iAttempts = 0
    while answer == '' and iAttempts < 3:
        iAttempts += 1
        if xWrite:
            ser.write(('\n' + sParameter + '=' +  sNewValue + '\r').encode("ascii"))
        else:
            ser.write(('\n' + sParameter + '?\r').encode("ascii"))
        timeOut = time.time() + 0.5;
        while (ser.inWaiting() > 0 or len(answer) < 5) and time.time() < timeOut:
            answer += ser.read(1).decode("ascii") #("utf-8")
    if (len(answer) < 5):
        #print('Reading parameter: ' + iParameter + ' failed')
        return False
    else:
        #print (answer)
        answer = answer.split(' = ')
        sReportedParameter = answer[0].split('(')
        sReportedParameter = sReportedParameter[1].split(')')
        sReportedParameter = sReportedParameter[0]
        answer = answer[1].split(' ')
        answer = answer[0].split('\r')
        print(str(sReportedParameter) + ' = ' + str(answer[0]))
        if sParameter == sReportedParameter and (answer[0] == sNewValue or not xWrite):
            return answer[0]
        else:
            return False
    

#time.sleep(0.2)
GetID()
ReceiveTable()
ser.close()
SaveTable()
