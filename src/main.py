#!/usr/bin/env python3
import queue
import sys

import json
import time

from dsf.connections import SubscribeConnection
from dsf.initmessages.clientinitmessages import SubscriptionMode

import hid
from actionDSF import ActionsDSF
from receiver import Receiver

from xhc_whb04b_6 import Xhb04b_6

# vendor_id = 0x10CE
# product_id = 0xEB93
# vendor_id = 0x2109
# product_id = 0x3431
queue = queue.Queue(0)


def dsf_connect(conn):
    while True:
        try:
            conn.connect()
        except Exception as err:
            print(err)
            time.sleep(1)
            continue

        break


if __name__ == "__main__":
    # try:
    #     port = sys.argv[1]
    #     print('Using port %s' % port)
    # except NameError:
    #     print('Serial port needed')
    #     exit(1)
    # device_info = hid.enumerate(vendor_id, product_id)
    # if not device_info:
    #     print('No device found')
    #     exit(1)
    # device_info = device_info.__getitem__(0)    # Always use first match
    # print('Device found!')
    # device = hid.Device
    # try:
    #     device = hid.Device(path=device_info.__getitem__('path'))
    # except OSError as e:
    #     print(e, file=sys.stderr)
    #     exit(2)

    cncPendant = Xhb04b_6(output_queue=queue)
    device = cncPendant.device

    subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH, "", ['move/axes/**'])
    # subscribe_connection.connect()
    dsf_connect(subscribe_connection)

    # try:
    # Get the complete model once
    machine_model = subscribe_connection.get_machine_model()
    machX = float(machine_model["move"]["axes"][0]["machinePosition"])
    machY = float(machine_model["move"]["axes"][1]["machinePosition"])
    machZ = float(machine_model["move"]["axes"][2]["machinePosition"])

    cncPendant.displayStatus.X = machX
    cncPendant.displayStatus.Y = machY
    cncPendant.displayStatus.Z = machZ
    cncPendant.UpdateDisplay()

    cncPendant.StartUSBReceiver()
    # receiver = Receiver(queue, device)
    # receiver.pendant = cncPendant
    actions = ActionsDSF(queue)
    # receiver.start()
    actions.start()

    while True:
        try:
            upd = subscribe_connection.get_machine_model_patch()
            update = json.loads(upd)
        except Exception as err:
            print(err)
            dsf_connect(subscribe_connection)
            continue

        # print(update)
        if ('move' in update) and ('axes' in update["move"]):
            for ind, val in enumerate(update["move"]["axes"]):
                if val and "machinePosition" in val:
                    # print(val)
                    machVal = float(val["machinePosition"])
                    if ind == 0:
                        cncPendant.displayStatus.X = machVal
                        # print(ind, machVal)
                    elif ind == 1:
                        cncPendant.displayStatus.Y = machVal
                        # print(ind, machVal)
                    elif ind == 2:
                        cncPendant.displayStatus.Z = machVal
                        # print(ind, machVal)
            cncPendant.UpdateDisplay()

        # time.sleep(0.1)
        # if inp == 's':
        #     # led_state = bytearray("06fdfe0000001000".replace(" ", "").decode("hex"))
        #     # led_state =  
        #     # hidapi.hid_write(device, led_state)
        #     # hid.Device.write(bytes.([0x00,0xf1]))
        #     device.write(bytes.fromhex("06fefdfe0201000d")) 
        #     device.write(bytes.fromhex("06030200d0010300")) 
        #     device.write(bytes.fromhex("0663106300640000")) 

        #     # data=[0x00, 0x04, 0x04, 0xFF, 0xFF, 0xFF, 0x00, 0x00]
        #     # result=

        #     # msg = bytes([0x06,0xfe,0xfd,0xfe,0x02,0x01,0x00,0x0d])
        #     # assert device.ctrl_transfer(0x21, 0x9, wValue=0x200, wIndex=0x00, data_or_wLength=msg) == len(msg)    
        #     # msg = bytes([0x06,0x03,0x02,0x00,0xd0,0x01,0x02,0x00])
        #     # assert device.ctrl_transfer(0x21, 0x9, wValue=0x200, wIndex=0x00, data_or_wLength=msg) == len(msg)    
        #     # msg = bytes([0x06,0x63,0x10,0x63,0x00,0x64,0x00,0x00])
        #     # assert device.ctrl_transfer(0x21, 0x9, wValue=0x200, wIndex=0x00, data_or_wLength=msg) == len(msg)    
        #     print("data sent")
        #     # time.sleep(0.1)

        #     # device.open()
        #     # device.write(bytes([0x06,0xfd,0xfe,0x00,0x00,0x00,0x10,0x00]))
        #     # device.write(bytes([0x06,0x11,0x00,0x11,0x00,0x12,0x00,0x12]))
        #     # device.write(bytes([0x06,0x01,0x00,0x01,0x10,0x00,0x00,0x00]))

    # receiver.quit()
    cncPendant.StoptUSBReceiver()
    actions.quit()
    # receiver.join()
    actions.join()

    exit(0)

# https://github.com/rubienr/machinekit/tree/feature-xhc-whb04b-6/src/hal/user_comps/xhc-whb04b-6
# >>> import usb.core
# >>> import usb.util
# >>>
# >>> dev = usb.core.find(idVendor=0x10CE, idProduct=0xEB93)
# https://stackoverflow.com/questions/44290837/how-to-interact-with-usb-device-using-pyusb
# https://github.com/walac/pyusb/blob/master/docs/tutorial.rst
#  COUNTER=0; while true; do ./main.py; echo $COUNTER; let COUNTER=COUNTER+1; done
