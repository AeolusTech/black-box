#!/bin/sh

set -x

services=$(ls etc/systemd/system/)

for service in $services
do
    sudo systemctl --now disable $service
done


files=$(find etc/ -type f)

for file in $files
do
    sudo rm /$file
done
