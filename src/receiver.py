import queue
import struct
import threading

fields = ['key1', 'key2', 'sel_inc', 'sel_axis', 'mpg_inc']
q = queue.Queue(100)


class Receiver(threading.Thread):
    def __init__(self, input_queue: queue.Queue, device):
        self.queue = input_queue
        self.device = device
        self.interrupt = False
        threading.Thread.__init__(self, name="XHC_Receiver")
        self.receiverThread = threading.Thread(target=self.receive, name="USB_Reader")

    def receive(self):
        while not self.interrupt:
            frame = self.device.read(8, timeout=1000)
            if len(frame) > 0:
                q.put(frame)
        self.device.close()

    def run(self):
        while not self.interrupt:
            try:
                frame = q.get(block=True, timeout=1)
                values = struct.unpack("xxBBBBbx", frame)
                vals = dict(zip(fields, values))
                k1 = vals.get('key1')
                key1 = key1_action(k1)
                if key1 != 'fn' and key1 != 'noop':
                    self.queue.put(key1)
                elif key1 == 'fn':
                    k2 = vals.get('key2')
                    key2 = key2_action(k2)
                    if key2 != 'noop':
                        self.queue.put(key2)
                else:
                    pulses = vals.get('mpg_incr')
                    axis = axis_selection(vals.get('sel_axis'))
                    inc = axis_incr_denominator(vals.get('sel_incr'))
                    if inc is not None and pulses != 0:
                        if pulses < 0:
                            inc = 0 - inc
                        if inc != 0.0:
                            self.queue.put('mpg({},{})'.format(axis, inc))

            except queue.Empty:
                pass

    def start(self) -> None:
        threading.Thread.start(self)
        self.receiverThread.start()

    def quit(self) -> None:
        self.interrupt = True


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
        0: 'noop',
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
        6: None,
        17: 'X',
        18: 'Y',
        19: 'Z',
        20: 'A',
        21: 'B',
        22: 'C',
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
    }[x]
