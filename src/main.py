#!/usr/bin/env python3
import sys
import struct
import hidapi
import threading
import queue
import json
import socket

fields = ['key1', 'key2', 'sel_incr', 'sel_axis', 'mpg_incr']
queue = queue.Queue(0)
previous = dict.fromkeys(fields)


def receiver():
	while True:
		#time.sleep(0.001)
		frame = device.read(8)
		if frame:
			queue.put_nowait(frame)


if __name__ == "__main__":
	vendor_id = 0x10CE
	product_id = 0xEB93
	device_info = list(hidapi.enumerate(vendor_id, product_id))
	if not device_info:
		print('No device found')
		exit(1)
	device_info = device_info[0]
	print('Device found!')
	print('Device parameters:')
	for attr in device_info.__slots__:
		print('\t', attr, ':', device_info.__getattribute__(attr))
	device = hidapi.Device
	try:
		device = hidapi.Device(device_info, blocking=True)
	except OSError as e:
		print(e, file=sys.stderr)
		exit(2)
	print("Manufacturer: ", device.get_manufacturer_string())
	print("Product: ", device.get_product_string())
	try:
		t1 = threading.Thread(target=receiver)
		t1.daemon = True
		t1.start()
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind(('localhost', 61101))
		print(s.getsockname())
		i = 0
		while True:
			# FIXME: Lots of MPG counts are dropping, need to check if it's a
			#  problem with this program or with the actual controller
			values = struct.unpack("xxBBBBbx", queue.get(block=True))
			vals = dict(zip(fields, values))
			#decoder.DecoderThread(vals.copy())
			#for item, value in vals.items():
				#print("{0}: {1}".format(item, value))
			if vals.items() != previous.items():
				s.sendto(json.dumps({'contents' : vals, 'index': i}).encode('UTF-8'), ('localhost', 61111))
				i += 1
			previous = vals
	except KeyboardInterrupt:
		print('')
	device.close()
	s.close()
	exit(0)
