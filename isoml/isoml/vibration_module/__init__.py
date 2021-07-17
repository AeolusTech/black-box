#!/usr/bin/env python3
import grovepi
from helpers import Config

ports = [
    int(Config.instance().config['vibration_module']['PORT_0']),
    int(Config.instance().config['vibration_module']['PORT_1']),
    int(Config.instance().config['vibration_module']['PORT_2'])
]
VIBRATION_OCCURRED = 0


for port in ports:
    grovepi.pinMode(port, "INPUT")

def read_sensors():
    collision_occured = [False, False, False]

    for idx, port in enumerate(ports):
        val = grovepi.digitalRead(port)
        if val == VIBRATION_OCCURRED:
            collision_occured[idx] = True

    return collision_occured
