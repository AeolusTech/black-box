#!/usr/bin/env python3
import csv
import collision_sensor
import IMU
import gps
import time
import vibration_module
from helpers import *

imu = IMU.IMU()
gps_thread = gps.GPS()

data_header = [
    "timestamp",
    "vibration1",
    "vibration2",
    "vibration3",
    "collision"
    
] + imu.get_labels() + gps_thread.get_labels()




def main():
    gps_thread.start()
    frequency = Config.instance().get_isoml_frequency()
    filename = Config.instance().get_new_output_filename_with_timestamp()

    print(f"Starting to log flight data to: {filename}")

    with open(filename, 'w', newline='') as csvfile:
        logger = csv.writer(csvfile, delimiter=',')

        logger.writerow(data_header)
        print(f"Column data is: {data_header}")
        
        while True:
            timestamp_utc = [get_utc_time_iso()]
            vibrations = vibration_module.read_sensors()
            collision = [collision_sensor.read_sensor()]
            imu_data = imu.get_data()
            gps_data = gps_thread.get_data()

            data = timestamp_utc + vibrations + collision + imu_data + gps_data
            logger.writerow(data)
            time.sleep(1.0 / frequency)


if __name__ == '__main__':
    main()
