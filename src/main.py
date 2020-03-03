#!/usr/bin/env python3
import sys
import struct
import hidapi

fields = ['key1', 'key2', 'sel_incr', 'sel_axis', 'mpg_incr']
previous = dict.fromkeys(fields)

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
		while True:
			values = struct.unpack('xxBBBBbx', device.read(8))
			vals = dict(zip(fields, values))
			print("Read: ", vals)
			for item in vals:
				if vals[item] != previous[item]:
					print(item)
			previous = vals

	except KeyboardInterrupt:
		pass
	device.close()
	exit(0)
