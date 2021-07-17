#!/usr/bin/env python3
import grovepi
from helpers import Config

port = int(Config.instance().config['collision_sensor']['PORT_0'])
COLLISION_OCCURRED = 0
grovepi.pinMode(port, "INPUT")

def read_sensor():        
    val = grovepi.digitalRead(port)
    if val == COLLISION_OCCURRED:
        return True
    return False