import random
import simpy
import math
import copy

class Application(object):
    def __init__(self, env, host, start_time, stop_time, send_interval):
        self.env = env
        self.host = host
        self.start_time = start_time
        self.stop_time = stop_time
        self.send_interval = send_interval
        self.seq_no = 0

        self.seen_seq_nos = []
        self.packets_to_forward = []

        if send_interval > 0:
            self.send_action = env.process(self.send())

        self.forward_action = None

        self.lower_layer = None

        self.num_packet_rcvd = 0
        self.num_packet_sent = 0
        self.transmission_dist_from_sender = []

    def dist(self, p1, p2):
        d = math.sqrt((p1[0] - p2[0])**2 + (p1[1] -p2[1])**2)
        return d

    def send(self):
        while True:
            t = self.start_time - self.env.now if self.env.now < self.start_time else self.send_interval

            if(self.env.now + t > self.stop_time):
                return
            yield self.env.timeout(t)
            pkt = {
                'seq_no': f'{self.host.transceiver.id}-{self.seq_no}',
                'size': 10,
                'created_at': self.env.now,
                'dest': 'BROADCAST',
                'sender_pos': self.host.pos,
                'last_pos': self.host.pos
            }
            self.transmission_dist_from_sender.append(0)
            self.seen_seq_nos.append(pkt['seq_no'])
            self.seq_no += 1
            self.lower_layer.receive_from_upper(pkt)
            self.num_packet_sent += 1

    def forward(self):
        try:
            while True:
                # print(self.packets_to_forward)
                if(len(self.packets_to_forward) == 0):
                    self.forward_action = None
                    return
                (t, pkt) = self.packets_to_forward[0]
                yield self.env.timeout(t - self.env.now)
                self.packets_to_forward.pop(0)
                cpy = copy.copy(pkt)
                cpy['last_pos'] = self.host.pos
                self.lower_layer.receive_from_upper(cpy)
                tx_dist = self.dist(self.host.pos, cpy['sender_pos'])
                self.transmission_dist_from_sender.append(tx_dist)
        except simpy.Interrupt:
            return

    def set_lower_layer(self, layer):
        self.lower_layer = layer

    def receive_from_lower(self, packet):
        self.num_packet_rcvd += 1
        seq_no = packet['seq_no']

        if seq_no in self.seen_seq_nos:
            l1 = len(self.packets_to_forward)
            self.packets_to_forward = [x for x in self.packets_to_forward if x[1]['seq_no'] != seq_no]
            if self.forward_action:
                self.forward_action.interrupt()
                self.forward_action = self.env.process(self.forward())
            return

        self.seen_seq_nos.append(seq_no)
        delay = 1 - self.dist(self.host.pos, packet['last_pos']) / 100 
        self.packets_to_forward.append((self.env.now + delay, packet))
        self.packets_to_forward.sort(key=lambda tup: tup[0])

        if self.forward_action:
            self.forward_action.interrupt()
        self.forward_action = self.env.process(self.forward())

