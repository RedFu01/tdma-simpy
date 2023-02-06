from modules.Application import Application
from modules.TdmaTransceiver import TdmaTransceiver


class Node(object):
    def __init__(self, env, pos, scheduler, radio_medium, slot_duration, is_sender=False):
        self.pos = pos

        self.application = Application(env, self, 0, 1.5, 1 if is_sender else 0)
        self.transceiver = TdmaTransceiver(env, self, scheduler, radio_medium, slot_duration)

        # Wire up
        self.application.set_lower_layer(self.transceiver)
        self.transceiver.set_upper_layer(self.application)
