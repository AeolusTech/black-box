#!/bin/sh

sudo cp ./collision_sensor/collision_sensor.service /etc/systemd/system/
sudo cp ./IMU/imu.service /etc/systemd/system/
sudo cp ./isoml/isoml.service /etc/systemd/system/
sudo cp ./waveshare/waveshare.service /etc/systemd/system/
