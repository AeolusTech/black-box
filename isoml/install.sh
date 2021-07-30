#!/bin/sh

set -x

sudo cp etc/* /etc/ -R

services=$(ls etc/systemd/system/)

for service in $services
do
    sudo systemctl enable $service
done


for service in $services
do
    sudo systemctl start $service
done
