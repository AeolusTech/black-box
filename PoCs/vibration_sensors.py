#!/usr/bin/env python3
import sys
import time
import grovepi

ports = [15, 16, 3]
collision = [False, False, False]

VIBRATION_OCCURED = 0

for port in ports:
    grovepi.pinMode(port, "INPUT")

while True:
    for port in ports:
        val = grovepi.digitalRead(port)
        if val == VIBRATION_OCCURED:
            print(f'collision on sensor: {port} and {val}')
    time.sleep(0.1)
