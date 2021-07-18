#!/bin/sh

services=$(ls etc/systemd/system/)

for service in $services
do
    systemctl status $service
done