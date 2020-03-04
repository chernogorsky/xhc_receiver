#!/usr/bin/env python3
import threading

fields = ['key1', 'key2', 'sel_incr', 'sel_axis', 'mpg_incr']


class DecoderThread(threading.Thread):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.data = data
        self.start()

    def run(self):
        for item, value in self.data.items():
            print(f"{item}: {value}")
