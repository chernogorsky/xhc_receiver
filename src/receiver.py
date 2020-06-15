import threading
import struct
import queue

fields = ['key1', 'key2', 'sel_incr', 'sel_axis', 'mpg_incr']
q = queue.Queue(100)


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
        12: 'noop',
        13: 'probe_z',
        14: 'continuous',
        15: 'step',
        16: 'noop'
    }[x]


class Receiver(threading.Thread):
    def __init__(self, input_queue: queue.Queue, device):
        self.queue = input_queue
        self.device = device
        self.interrupt = False
        threading.Thread.__init__(self, name="XHC_Receiver")
        self.receiverThread = threading.Thread(target=self.receive, name="USB_Reader")

    def receive(self):
        while not self.interrupt:
            frame = self.device.read(8, timeout=1)
            if len(frame) > 0:
                q.put_nowait(frame)

    def run(self):
        while not self.interrupt:
            try:
                frame = q.get(block=True, timeout=1)
                values = struct.unpack("xxBBBBbx", frame)
                vals = dict(zip(fields, values))
                k1 = vals.get('key1')
                self.queue.put(key1_action(k1))
            except queue.Empty:
                pass

    def start(self) -> None:
        threading.Thread.start(self)
        self.receiverThread.start()

    def quit(self) -> None:
        self.interrupt = True


