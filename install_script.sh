#!/bin/sh


sudo apt-get update && sudo apt-get upgrade -y -q
sudo apt-get install -y -q build-essential vim
ssh-keygen -t rsa -b 4096
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
curl -kL dexterindustries.com/update_grovepi | bash
echo "deb https://seeed-studio.github.io/pi_repo/ stretch main" | sudo tee /etc/apt/sources.list.d/seeed.list
curl https://seeed-studio.github.io/pi_repo/public.key | sudo apt-key add -
sudo apt update
sudo apt install python3-mraa python3-upm python-rpi.gpio python3-rpi.gpio
cd ..
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo pip install .
cd ../BlackBox
sudo pip install -r requirements.txt
sudo cp waveshare-gsm-gps.rules /etc/udev/rules.d/
