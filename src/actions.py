#!/usr/bin/env python3
import socket
import threading
import queue


class Actions(threading.Thread):
    def __init__(self, input_queue: queue.Queue):
        self.queue = input_queue
        self.interrupt = False
        threading.Thread.__init__(self, name="XHC_Action")

    def start(self) -> None:
        threading.Thread.start(self)

    def run(self):
        while not self.interrupt:
            try:
                action = self.queue.get(block=True, timeout=1)
                if action != 'noop':
                    with open('nc_commands/' + action + '.nc', 'r') as command:
                        content = command.read()
                        print(content)
            except queue.Empty:
                pass

    def quit(self):
        self.interrupt = True


if __name__ == "__main__":
    srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        srv.bind(('localhost', 61111))  # Allocate random port
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
