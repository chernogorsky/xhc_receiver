#!/usr/bin/env python3
import queue
import threading
from time import sleep

import parse
import serial


class PortException(BaseException):
    pass


class Actions(threading.Thread):
    def __init__(self, input_queue: queue.Queue, port, baudrate):
        self.queue = input_queue
        self.interrupt = False
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial
        try:
            self.init_serial()
        except serial.SerialException as ex:
            print(ex)
            exit(-1)

    def init_serial(self):
        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_TWO,
            timeout=None,
            xonxoff=False,
            dsrdtr=False,
            rtscts=False
        )
        if self.serial.isOpen():
            while self.serial.in_waiting == 0 and not self.interrupt:
                print('Waiting')
                sleep(0.5)
            if self.interrupt:
                return
            print('Connected')
            self.serial.write('%\n'.encode('UTF-8'))
            self.serial.write('G17G40G49G91G53\n'.encode('UTF-8'))
            threading.Thread.__init__(self, name="XHC_Action")

    def start(self) -> None:
        self.start(self)

    def reset_serial(self):
        self.serial.reset_output_buffer()
        self.serial.reset_input_buffer()
        self.serial.close()
        self.init_serial()

    def run(self):
        while not self.interrupt:
            try:
                action = str(self.queue.get(block=True, timeout=1))
                buf = self.serial.in_waiting
                self.serial.flushInput()
                if buf == 0:
                    print('Buffer full, command discarded')
                    if action == 'reset':
                        self.reset_serial()
                else:
                    if action.startswith('mpg'):
                        filename = 'mpg'
                    else:
                        filename = action
                    with open('nc_commands/' + filename + '.nc', 'r') as command:
                        content = command.read()
                        if filename == 'mpg':
                            t = parse.parse('mpg({},{})', action)
                            content = content.format(t[0], t[1])
                        print('Sending command \'{}\''.format(content))
                        content_bytes = content.encode("UTF-8")
                        self.serial.write(content_bytes)
                        print('Done')
                    if filename == 'reset':
                        self.reset_serial()
            except queue.Empty:
                pass
        self.serial.write('%'.encode('UTF-8'))
        self.serial.close()

    def quit(self):
        self.interrupt = True
