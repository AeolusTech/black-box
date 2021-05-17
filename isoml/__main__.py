#!/usr/bin/env python3
from zeroless import Client
from IMU import IMU
from collision_sensor import CollisionSensor
from waveshare import Waveshare
from threading import Thread


topics_to_listen = [
    b'master_acc_x',
    b'master_acc_y',
    b'master_acc_z',
    b'master_gyro_x',
    b'master_gyro_y',
    b'master_gyro_z',
    b'mag_x',
    b'mag_y',
    b'mag_z',
    b'master_temp',
    b'collision_sensor',
    b'gps_lat',
    b'gps_long',
]

imu = IMU()
thread_imu = Thread(target=imu.run)

collision_sensor = CollisionSensor()
thread_collision_sensor = Thread(target=collision_sensor.run)

waveshare = Waveshare()
thread_waveshare = Thread(target=waveshare.run)


def get_initialized_client():
    client = Client()
    for i in range(len(topics_to_listen)):
        client.connect_local(port=12345 + i)

    return client


def run_devices_threads():
    try:
        thread_imu.start()
        thread_collision_sensor.start()
        thread_waveshare.start()
    except:
        print("Error: unable to start some of the threads")


def main():
    client = get_initialized_client()

    listen_for_pub = client.sub(topics=topics_to_listen)
    run_devices_threads()

    for topic, msg in listen_for_pub:
        print(topic, ': ', msg)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        imu.stop()
        collision_sensor.stop()
        waveshare.stop()

        thread_imu.join()
        thread_collision_sensor.join()
        thread_waveshare.join()
