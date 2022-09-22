#!/bin/bash

mkdir /home/pi/dev
mkdir /home/pi/dev/DHT22_sensor
mkdir /home/pi/dev/DHT22_sensor/log
cp -r ./* /home/pi/dev/DHT22_sensor
pip3 install adafruit-circuitpython-dht
pip3 install flask
