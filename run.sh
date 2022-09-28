#!/bin/bash

# sudo vim /etc/rc.local for startup
# # run.sh for TempHumid py
# /home/pi/dev/DHT22_sensor/run.sh
nohup python -u /home/pi/dev/DHT22_sensor/sensor.py &
nohup python -u /home/pi/dev/DHT22_sensor/Run_Server.py &
