#!/usr/bin/env python3
import csv
import collision_sensor
import IMU
import time
import vibration_module
from helpers import *

imu = IMU.IMU()

data_header = [
    "timestamp",
    "vibration1",
    "vibration2",
    "vibration3",
    
] + imu.get_labels()


def main():
    frequency = Config.instance().get_isoml_frequency()
    filename = Config.instance().get_new_output_filename_with_timestamp()

    with open(filename, 'w', newline='') as csvfile:
        logger = csv.writer(csvfile, delimiter=',')

        logger.writerow(data_header)
        
        while True:
            timestamp_utc = [get_utc_time_iso()]
            vibrations = vibration_module.read_sensors()
            collision = [collision_sensor.read_sensor()]
            imu_data = imu.get_data()

            data = timestamp_utc + vibrations + collision + imu_data
            logger.writerow(data)
            time.sleep(1.0 / frequency)


if __name__ == '__main__':
    main()
