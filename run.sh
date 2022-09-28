#!/bin/bash

# sudo vim /etc/rc.local for startup
nohup python -u /home/pi/dev/DHT22_sensor/sensor.py &
nohup python -u /home/pi/dev/DHT22_sensor/Run_Server.py &
