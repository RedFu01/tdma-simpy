import simpy
import random
import math

from modules.Node import Node
from modules.TdmaScheduler import TdmaScheduler
from modules.RadioMedium import RadioMedium
from utils.Plotter import Plotter


def monitor(env, simtime):
    idx = 1
    steps = 10
    while True:
        yield env.timeout(simtime / steps)
        print(f'{idx * 100/ steps:.2f}%')
        idx+=1


def main(run_id):
    # random.seed(run_id)
    TdmaScheduler.radio_idx = 0
    sim_time = 10

    # Parameters
    slot_duration = 0.002
    R = 2000

    # Setup:
    env = simpy.Environment()
    env.process(monitor(env, sim_time))
    radio_medium = RadioMedium(env, 100)
    scheduler = TdmaScheduler(env, slot_duration, 100)

    nodes = []
    n = Node(env, (0,0), scheduler, radio_medium, slot_duration, is_sender=True)
    nodes.append(n)

    for i in range(1000):
        r = math.sqrt(random.random()) * R
        phi = random.random() * math.pi * 2
        x = math.sin(phi) * r
        y = math.cos(phi) * r
        n = Node(env, (x, y), scheduler, radio_medium, slot_duration, is_sender=True)
        nodes.append(n)

    # Run:
    env.run(until=sim_time)

    # Eval:
    plotter = Plotter()
    dist = []
    print('Eval', env.now)

    for n in nodes:
        print(f'{n.transceiver.id} {n.pos} | Sent: {n.application.num_packet_sent} / Rcvd: {len(n.application.seen_seq_nos)}')
        dist += n.application.transmission_dist_from_sender

    # plotter.plot_histogram(dist, f'tx_dist_{run_id}')
    plotter.plot_time_series([t[0] for t in scheduler.utilization], [t[1] for t in scheduler.utilization], 'Utilization', f'utilization_{run_id}')
    return dist


if __name__ == '__main__':
    main(0)
        
    
        
