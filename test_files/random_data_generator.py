#!/usr/bin/env python

from random import uniform, randint
import csv


three_hours_of_flight_in_seconds = 3 * 60 * 60
IMU_Hz_rate = 10


def get_single_protocol_frame():
    IMU_list = [str(uniform(-9, 9))[:5] for i in range(6)]
    gps_list = [str(uniform(-128, 128))[:10] for i in range(2)]
    collision = [randint(0, 1)]
    return IMU_list + gps_list + collision


with open("protocol_example_3_hours_of_flight.txt", 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(three_hours_of_flight_in_seconds):
        for j in range(10):  # IMU data comes at 10
            spamwriter.writerow(get_single_protocol_frame())
