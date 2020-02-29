#!/usr/bin/env python3
import sys
import os
import hid

if __name__ == "__main__":
	vendor_id = 4302 # 10CE
	product_id = 60307 # EB93
	device_list = hid.enumerate(vendor_id, product_id)
	device_dict = next(dev for dev in device_list if dev['usage'] == 0)
	device = hid.device()
	device.open_path(device_dict['path'])
	print("Manufacturer: ", device.get_manufacturer_string())
	print("Product: ", device.get_product_string())
	print("Features: ", device.get_feature_report(0, 100))
	try:
		while 1:
			print("Read: ", device.read(100))
	except KeyboardInterrupt:
		pass
	device.close()
	exit(0)
