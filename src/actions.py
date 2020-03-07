#!/usr/bin/env python3
import socket
	
def key1_action(x):
	return {
		1 : reset,
		2 : stop,
		3 : start_pause,
		4 : feed_plus,
		5 : feed_minus,
		6 : spindle_plus,
		7 : spindle_minus,
		8 : machine_home,
		9 : safe_z,
		10 : work_home,
		11 : spindle_on_off,
		12 : noop,
		13 : probe_z,
		14 : continuous,
		15 : step,
		16 : noop
	}[x]

def reset():
	print("Reset")

def stop():
	print("Stop")
	
def start_pause():
	print("Start/Pause")
	
def feed_plus():
	print("Feed+")
	
def feed_minus():
	print("Feed-")
	
def spindle_plus():
	print("Spindle+")
	
def spindle_minus():
	print("Spindle-")
	
def machine_home(): 
	# G28
	print("Machine Home")
	
def safe_z():
	print("Safe Z")
	
def work_home():
	# Set work home on selected axis
	print("Work Home")
	
def spindle_on_off():
	print("Spindle On/Off")
	
def probe_z():
	# Set tool offset
	print("Probe Z")
	
def continuous():
	print("Continuous")
	
def step():
	print("Step")
	
def noop():
	pass


if __name__ == "__main__":
	srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		srv.bind(('localhost', 61111)) # Allocate random port
	except socket.error as e:
		print("Socket bind failed with error code {0}: {0}".format(e.errno, e.getMessage()))
	print(srv.getsockname())
	try:
		while True:
			data, addr = srv.recvfrom(1024)
			if not data:
				continue
			print("From {0}: {1}".format(addr, data))
			
	except KeyboardInterrupt:
		pass
	srv.close()
	print('')
	exit(0)
