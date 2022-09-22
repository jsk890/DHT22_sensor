''' --------------------------------
AM2302 DHT22 (Old Module ver.)
Humidity & Temperature Sensor Logger
by hgstyler on Python
-------------------------------- '''

import sys
import Adafruit_DHT as dht
from os import path
import time
import csv

# current time
now = time.localtime()
today = ("%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday))

# csv file path
fpath = '/home/pi/dev/DHT22_sensor/log/'
location = 'Tr_Room'
fname = fpath + location + '_' + today + '.csv'

# csv file: first row generation
# label: Date | Time | Temp(*C) | Humid(%) | dTemp(*C) | dHumid(%) | Cal. Temp(*C) | Cal. Humid (%) | Cal. Msg
if path.exists(fname)==False:
    with open(fname, "w") as f:
        wr = csv.writer(f, delimiter=",", lineterminator='\n')
        wr.writerow(['Date', 'Time', 'Temp(*C)', 'Humid(%)', 'dTemp(*C)', 'dHumid(%)', 'Cal. Temp(*C)', 'Cal. Humid(%)', 'Cal. Msg'])

# sensor read loop
while True:
    # raw humid, temp data (GPIO 4)
    humidity, temperature = dht.read_retry(dht.DHT22, 4)
    
    # data list generation for csv
    if humidity is not None and temperature is not None: # read failure check
        if humidity < 100.1: # out of range in humidity check
            # humid & temp for data list
            humid = round(humidity, 1)
            temp = round(temperature, 1)

            dt = 0; dh = 0
            calibrated_temp = temp + dt; calibrated_humid = humid + dh

            # calibration msg for data list
            if dt == 0 and dh == 0:
                calibration_msg = 0 # 0: no calibration
            elif dt != 0 and dh == 0:
                calibration_msg = 1 # 1: temp calibration
            elif dt == 0 and dh != 0:
                caliabration_msg = 2 # 2: humid calibration
            else:
                calibration_msg = 3 # 3: temp & humid calibration
            
            # time & data for data list
            now = time.localtime()
            nowdate = ("%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)) 
            nowtime = ("%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec)) 

            # print on screen
            print('Temp: {0:}*C  Humid: {1:}%  {2:} {3:}'.format(temp, humid, nowdate, nowtime))

            # data list
            data = []
            data.append(nowdate)
            data.append(nowtime)
            data.append(temp)
            data.append(humid)
            data.append(dt)
            data.append(dh)
            data.append(calibrated_temp)
            data.append(calibrated_humid)
            data.append(calibration_msg)
            
            # write csv
            with open(fname, "a") as f:
                wr = csv.writer(f, delimiter=",", lineterminator='\n')
                wr.writerow(data)
            
    # wait 5 sec for next loop
    time.sleep(5)

