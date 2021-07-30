#!/bin/sh

set -x

services=$(ls etc/systemd/system/)

for service in $services
do
    sudo systemctl disable $service
done

for service in $services
do
    sudo systemctl stop $service
done

files=$(find etc/ -type f)

for file in $files
do
    sudo rm /$file
done
