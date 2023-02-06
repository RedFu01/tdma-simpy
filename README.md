# tdma-simpy
This repository holds a simplistic TDMA simulation built on top of the discrete event simulator framework [simpy](https://simpy.readthedocs.io/en/latest/).

## Modules
To realize a TDMA communication network, several modules are implemented:

- `TdmaScheduler` is a global entity, that divides time into slots and decides which node is allowed to schedule in which slot.
- `TdmaTransceiver` is a simple link-layer implementation that communicates with the `TdmaScheduler` to obtain transmission grants.
- `RadioMedium` is an abstraction RF communication. It realizes a limited transmission range as well as transmission delays.
- `Application` is a simple application-layer implementation, that is able to send and receive packets.
- `Node` is a module representing a node in the simulation. A nodes has an `Application` and a `TdmaTransceiver`. It also has a geographical position.

## Getting Started
A simple simulation setup is put together in `main.py`.
Install all required dependencies with `pip3 -r requirements.txt` and run the simulation by `python3 main.py`