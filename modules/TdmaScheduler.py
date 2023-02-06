import numpy as np
import random

class TdmaScheduler(object):
    radio_idx = 0
    def __init__(self, env, slot_duration, frame_length):
        self.env = env
        self.slot_duration = slot_duration
        self.frame_length = frame_length
        self.radios = []
        self.buffer_status = dict()

        self.action = env.process(self.run())

        self.utilization = []

    def run(self):
        while True:
            yield self.env.timeout(self.slot_duration * self.frame_length)
            #print('Scheduler', self.env.now)
            self.compute_schedule()

    def compute_schedule(self):
        if(len(self.radios) == 0):
            return

        schedule = [-1 for x in np.zeros(self.frame_length)]
        schedule_idx = 0
        node_idx = random.randint(0, len(self.radios)-1)
        total_buffer_status = sum(self.buffer_status.values())
        slots_to_schedule = min(total_buffer_status, self.frame_length)

        u = slots_to_schedule / self.frame_length
        t = self.env.now
        self.utilization.append((t,u))

        while schedule_idx < slots_to_schedule:
            node_buffer_status = self.buffer_status[node_idx]
            if node_buffer_status > 0:
                schedule[schedule_idx] = node_idx
                self.buffer_status[node_idx] -=1
                schedule_idx += 1
                node_idx = (node_idx + 1) % (len(self.radios))
            else:
                node_idx = (node_idx + 1) % (len(self.radios))

        for r in self.radios:
            r.set_schedule(schedule)

    def register(self, radio):
        self.radios.append(radio)
        idx = TdmaScheduler.radio_idx
        TdmaScheduler.radio_idx += 1
        self.buffer_status[idx] = 0
        return idx

    def report_buffer_status(self, id, buffer_status):
        self.buffer_status[id] = buffer_status

