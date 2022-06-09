import time
import queue
import struct
import threading
import math
import typing


import hid

fields = ['key1', 'key2', 'sel_inc', 'sel_axis', 'mpg_inc']

def key1_action(x):
    return {
        0: 'noop',
        1: 'reset',
        2: 'stop',
        3: 'start_pause',
        4: 'feed_plus',
        5: 'feed_minus',
        6: 'spindle_plus',
        7: 'spindle_minus',
        8: 'machine_home',
        9: 'safe_z',
        10: 'work_home',
        11: 'spindle_on_off',
        12: 'fn',
        13: 'probe_z',
        14: 'continuous',
        15: 'step',
        16: 'noop'
    }[x]


def key2_action(x):
    return {
        0: 'fn_reset',
        1: 'noop',
        2: 'noop',
        3: 'noop',
        4: 'macro_1',
        5: 'macro_2',
        6: 'macro_3',
        7: 'macro_4',
        8: 'macro_5',
        9: 'macro_6',
        10: 'macro_7',
        11: 'macro_8',
        12: 'noop',
        13: 'macro_9',
        14: 'noop',
        15: 'noop',
        16: 'macro_10'
    }[x]


def axis_selection(x):
    return {
        0: None,
        6: 'N',
        16: 'noop',
        17: 'X',
        18: 'Y',
        19: 'Z',
        20: 'A',
        21: 'B',
        22: 'C',
        23: 'noop',
    }[x]


def axis_incr_denominator(x):
    return {
        0: None,
        13: 0.001,  # 2%
        14: 0.01,  # 5%
        15: 0.1,  # 10%
        16: 1.0,  # 30%
        26: 5.0,  # 60%
        27: 10.0,  # 100%
        155: 20.0  # Lead
    }.get(x, None)

class Xhb04b_6_DisplayStatus:
	X: float = 0
	Y: float = 0
	Z: float = 0
	A: float = 0
	B: float = 0
	C: float = 0

	displayPage: int = 0

	

	def IntToHex4bR(self, input: int, minus: bool = False) -> str:

		result = input

		# print(input, hex(input))
		if minus:
			result = result | 0x8000


		result = hex(result)[2:]

		# print(input, result)



		result = '0'*(4-len(result))+result


		# print('' + result[2:] + result[:2])
		return '' + result[2:] + result[:2]

	def FloatToSplit(self, f: float) -> (int, int, bool):
		frac, whole = math.modf(abs(f))

		return (int(whole), round(frac * 10000), f < 0)

	def FloatToHex4bR(self, input: float) -> str:
		whole, frac, minus = self.FloatToSplit(input)
		return self.IntToHex4bR(whole) +  self.IntToHex4bR(frac,minus)


	


	def DisplayUpdateUSBData(self):
		baseNume = 3*self.displayPage
		# print(baseNume)
		result = [ self.FloatToHex4bR(val) for val in [self.X, self.Y, self.Z, self.A, self.B, self.C]] 
			
		return ["06fefdfe02{}".format(result[baseNume][:6]),"06{}{}{}".format(result[baseNume][6:],result[baseNume+1],result[2][:4]),"06{}00d0010300".format(result[baseNume+2][4:])]


class Xhb04b_6_Receiver(threading.Thread):
    def __init__(self, input_queue: queue.Queue, output_queue: queue.Queue, device, callback, callback_obj):
        self.q = input_queue
        self.queue = output_queue
        self.device = device
        self.interrupt = False
        self.callback = callback
        self.callback_obj = callback_obj
        threading.Thread.__init__(self, name="XHC_Receiver")
        self.receiverThread = threading.Thread(target=self.receive, name="USB_Reader")

    def receive(self):
        while not self.interrupt:
            frame = self.device.read(8, timeout=1000)
            # print(frame)
            if len(frame) > 0:
                self.q.put(frame)
        self.device.close()

    def run(self):
        while not self.interrupt:
            try:
            	frame = self.q.get(block=True, timeout=1)
            	self.callback(self.callback_obj,usb_frame=frame)
            except queue.Empty:
            	pass

    def start(self) -> None:
        threading.Thread.start(self)
        self.receiverThread.start()

    def quit(self) -> None:
        self.interrupt = True



# class Xhb04b_6_Status:
# 	test: int

class Xhb04b_6:
	# displayStatus: Xhb04b_6_DisplayStatus
	lastDisplayUpdate: float
	vendor_id = 0x10CE
	product_id = 0xEB93

	sel_axis: typing.Union[int, None] = 0

	input_queue: queue.Queue
	output_queue: queue.Queue


	old_inc: int = 0
	old_axis: str = 'noop'



	def usbConnect(self):
		device_info = hid.enumerate(self.vendor_id, self.product_id)
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

		self.device = device

	def UpdateDisplay(self):
		usbData = self.displayStatus.DisplayUpdateUSBData()
		for block in usbData:
			# print("Write to usb: {}".format(block))
			self.device.write(bytes.fromhex(block)) 

	def SetAxisFromUSB(self, usbInput: int):
		if usbInput >= 17 and usbInput <= 23:
			self.sel_axis = usbInput - 17
		else:
			self.sel_axis = None

		if (self.sel_axis is not None and self.sel_axis > 2):
			self.displayStatus.displayPage = 1
		else:
			self.displayStatus.displayPage = 0

		# print(self.sel_axis)

	def StartUSBReceiver(self):
		self.receiver.start()

	def StopUSBReceiver(self):
		self.receiver.quit()
		self.receiver.join()

	def ReceiverCallback(self, usb_frame):
		# print(usb_frame)
		values = struct.unpack("xxBBBBbx", usb_frame)
		
		vals = dict(zip(fields, values))
		# print(vals)

		action = None
		# sel_axis = None
		# sel_inc = None

		s_inc = vals.get("sel_inc")
		s_axis = vals.get("sel_axis")

		k1 = vals.get("key1")
		key1 = key1_action(k1)
		k2 = vals.get('key2')
		key2 = key2_action(k2)
		pulses = vals.get('mpg_inc')
		sel_axis = axis_selection(s_axis)
		sel_inc = axis_incr_denominator(s_inc)
		if sel_inc:
			inc = sel_inc * pulses
		else:
			inc = pulses



		if self.old_inc == 0 and s_inc:
			action = 'enable'
		elif s_inc == 0 and self.old_inc:
			action = 'disable'
		elif s_inc != self.old_inc:
			action = 'change_inc'			
		elif sel_axis != 'noop' and sel_axis != self.old_axis:
			action = 'change_axis'
			self.setSelAxis(sel_axis)


		elif key1 != 'fn' and key1 != 'noop' and key1 != 'continuous':
			action = key1
		elif key1 == 'fn' and key2 != 'noop':
			action = key2
        # else:

		if sel_inc is not None and pulses != 0:
			if key1 != 'continuous':
				inc = min(inc, 1.0)
			if inc != 0.0:
				action = 'mpg'
            

		self.old_inc = s_inc
		self.old_axis = sel_axis

		if action:
			output_struct = {
				"action": action,
				"sel_axis": sel_axis,
				"sel_inc": sel_inc,
				"inc": inc,
				"pulse": pulses,
				"key1": key1,
				"key2": key2
			}
			self.output_queue.put(output_struct)

			# print(output_struct)


	def setSelAxis(self, newSelAxis):
		# print('Axis changed to {}'.format(newSelAxis))

		oldPage = self.displayStatus.displayPage

		if newSelAxis == 'N': 
			return
		elif newSelAxis in ['X', 'Y', 'Z']:
			newPage = 0
		else:
			newPage = 1

		if newPage != oldPage:
			self.displayStatus.displayPage = newPage
			self.UpdateDisplay()
			print("Page changed to {}".format(newPage))



	
	def __init__(self, output_queue):
		# self.queue = queue
		self.displayStatus = Xhb04b_6_DisplayStatus()
		self.usbConnect()
		self.input_queue = queue.Queue(100)
		self.output_queue = output_queue

		self.receiver = Xhb04b_6_Receiver(input_queue=self.input_queue, output_queue=self.output_queue, device=self.device, callback=self.ReceiverCallback.__func__, callback_obj=self)

	
