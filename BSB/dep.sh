#!/bin/sh


#LIST_LIBRARIES = "pip socket psutil time subprocess PIL smbus math"

sudo apt-get update #get latest update
#apt-get install -y python3-psutil python3-smbus python3-pillow


python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
#sudo apt-get install -y pillow
python3 -m pip install smbus
python3 -m pip install psutil



