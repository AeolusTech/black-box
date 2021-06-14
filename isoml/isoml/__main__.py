#!/usr/bin/env python3
from zeroless import Client


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


def get_initialized_client():
    client = Client()
    for i in range(len(topics_to_listen)):
        client.connect_local(port=12345 + i)

    return client


def main():
    client = get_initialized_client()

    listen_for_pub = client.sub(topics=topics_to_listen)

    for topic, msg in listen_for_pub:
        print(topic, ': ', msg)


if __name__ == '__main__':
    main()
