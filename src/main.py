#!/usr/bin/env python3
import json
import queue
import socket
import struct
import sys
import threading

import hid

fields = ['key1', 'key2', 'sel_incr', 'sel_axis', 'mpg_incr']
queue = queue.Queue(0)


def receiver():
    while True:
        frame = device.read(8, timeout=None)
        if frame is not None:
            queue.put_nowait(frame)


if __name__ == "__main__":
    vendor_id = 0x10CE
    product_id = 0xEB93
    device_info = hid.enumerate(vendor_id, product_id)
    if not device_info:
        print('No device found')
        exit(1)
    device_info = device_info.__getitem__(0)
    print('Device found!')
    device = hid.Device
    try:
        device = hid.Device(path=device_info.__getitem__('path'))
    except OSError as e:
        print(e, file=sys.stderr)
        exit(2)
    try:
        t1 = threading.Thread(target=receiver)
        t1.daemon = True
        t1.start()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('localhost', 61101))
        print(s.getsockname())
        i = 0
        while True:
            values = struct.unpack("xxBBBBbx", queue.get(block=True))
            vals = dict(zip(fields, values))
            s.sendto(json.dumps({'contents': vals, 'index': i}).encode('UTF-8'), ('localhost', 61111))
            i += 1
    except KeyboardInterrupt:
        print('')
    device.close()
    s.close()
    exit(0)
