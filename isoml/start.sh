#!/bin/sh

services=$(ls etc/systemd/system/)

for service in $services
do
    sudo systemctl start $service
done
