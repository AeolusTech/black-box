#!/bin/sh

sudo apt-get update && sudo apt-get upgrade -y -q
sudo apt-get install -y -q build-essential git libsystemd-dev vim lz4
ssh-keygen -t rsa -b 4096
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
sudo apt update
sudo apt install python3-mraa python3-upm python-rpi.gpio python3-rpi.gpio libatlas-base-dev
sudo pip install -r requirements.txt
curl -kL dexterindustries.com/update_grovepi | bash
cd /home/pi/Dexter/GrovePi/Firmware
bash firmware_update.sh

cd /home/pi
git clone https://github.com/xorbit/LiFePO4wered-Pi.git
cd /home/pi/LiFePO4wered-Pi/
make all
sudo make user-install

cd /home/pi/BlackBox
