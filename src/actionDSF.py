#!/usr/bin/env python3
import queue
import threading
import time
from time import sleep
import os

import parse

from dsf.connections import CommandConnection


class PortException(BaseException):
    pass


class ActionsDSF(threading.Thread):

    def dsf_connect(self):
        while True:
            try:
                self.conn.connect()
            except Exception as err:
                print(err)
                time.sleep(1)
                continue

            break

    def __init__(self, input_queue: queue.Queue):
        self.conn = CommandConnection(debug=True)
        self.queue = input_queue
        self.interrupt = False
        self.dsf_connect()
        threading.Thread.__init__(self, name="XHC_Action")

    def start(self) -> None:
        super().start()

    def reset_serial(self):
        pass
        # self.serial.reset_output_buffer()
        # self.serial.reset_input_buffer()
        # self.serial.close()
        # self.init_serial()

    def run(self):
        while not self.interrupt:
            try:
                action_struct = self.queue.get(block=True, timeout=1)

                # print(action_struct)
                action = action_struct.get('action')

                filename = 'nc_commands/' + action + '.nc'

                if os.path.exists(filename):
                    with open(filename, 'r') as command:
                        content = command.read()
                        if action == 'mpg':
                            axis = action_struct['sel_axis']
                            inc = action_struct['inc']
                            content = content.format(axis, inc)

                        if content:
                            # print('Sending command \'{}\''.format(content))
                            self.conn.perform_simple_code(content)
                            # print('Done {}'.format(res))
                else:
                    pass
                # print('skip: action {} not defined'.format(action))
            except queue.Empty:
                pass
            except Exception as err:
                print("error: %s".format(err))
                self.dsf_connect()

    def quit(self):
        self.conn.close()
        self.interrupt = True
