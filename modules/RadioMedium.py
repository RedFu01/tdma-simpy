import math

class RadioMedium(object):
    def __init__(self, env, radio_range):
        self.env = env
        self.radio_range = radio_range
        self.radios = []
        self.radio_propagation = 300000000
        self.transmission_delay = 0.001

    def register(self, radio):
        self.radios.append(radio)

    def dist(self, source, dest):
        p1 = source.host.pos
        p2 = dest.host.pos
        d = math.sqrt((p1[0] - p2[0])**2 + (p1[1] -p2[1])**2)
        return d

    def receive_from_upper(self, source, packet):
        # find all neighbors, 
        # calc reception times
        receivers = []

        for r in self.radios:
            dist = self.dist(source, r)
            if source.id != r.id and dist <= self.radio_range:
                receivers.append((dist, r))

        self.env.process(self.on_transmit(packet, receivers))

    def on_transmit(self, packet, receivers):
        receivers.sort(key=lambda tup: tup[0])
        idx = 0
        while True:
            if idx >= len(receivers):
                return
            delay = self.transmission_delay + (receivers[idx][0] / self.radio_propagation)
            yield self.env.timeout(delay)
            receivers[idx][1].receive_from_lower(packet)
            idx += 1

        
