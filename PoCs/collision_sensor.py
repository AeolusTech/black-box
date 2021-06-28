#!/usr/bin/env python3
import sys
import time
import grovepi




VIBRATION_OCCURED = 0
port = 14

grovepi.pinMode(port, "INPUT")


while True:
    val = grovepi.digitalRead(port)
    if val == VIBRATION_OCCURED:
        print(f'collision detected!')
    time.sleep(0.1)
