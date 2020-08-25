#!/usr/bin/env python3
import queue
import sys
from actions import Actions
from receiver import Receiver
import hid

vendor_id = 0x10CE
product_id = 0xEB93
queue = queue.Queue(0)

if __name__ == "__main__":
    device_info = hid.enumerate(vendor_id, product_id)
    if not device_info:
        print('No device found')
        exit(1)
    device_info = device_info.__getitem__(0)    # Always use first match
    print('Device found!')
    device = hid.Device
    try:
        device = hid.Device(path=device_info.__getitem__('path'))
    except OSError as e:
        print(e, file=sys.stderr)
        exit(2)
    receiver = Receiver(queue, device)
    actions = Actions(queue)
    receiver.start()
    actions.start()
    while True:
        inp = input("").lower()
        if inp == 'quit' or inp == 'exit' or inp == 'q':
            break
    receiver.quit()
    actions.quit()
    receiver.join()
    actions.join()
    exit(0)
