''' --------------------------------
AM2302 DHT22
Humidity & Temperature Sensor Logger
by hgstyler on python
-------------------------------- '''

import sys
import Adafruit_DHT as dht
from os import path
import time
import csv

now = time.localtime()
today = ("%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday))
fpath = '/home/pi/dev/DHT22_/Log/'
location = 'Tr_Room'
fname = fpath + location + '_' + today + '.csv'

if path.exists(fname)==False:
    with open(fname, "w") as f:
        wr = csv.writer(f, delimiter=",", lineterminator='\n')
        wr.writerow(['Time', 'Temp(*C)', 'Humid(%)'])

while True:
    humidity, temperature = dht.read_retry(dht.DHT22, 4)
    
    if humidity is not None and temperature is not None: # read failure check
        if humidity < 100.1: # out of range in humidity check
            humid = round(humidity, 1)
            temp = round(temperature, 1)
            
            now = time.localtime()
            nowdate = ("%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)) 
            nowtime = ("%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec)) 

            print('Temp: {0:}*C  Humid: {1:}%  {2:} {3:}'.format(temp, humid, nowdate, nowtime))

            #print('Temp: {0:0.1f}*C Humid: {1:0.1f}% {2:}-{3:}-{4:} {5:}:{6:}:{7:}'.\
                    #format(temp, humid, \
                    #time.strftime("%Y"), time.strftime("%m"), time.strftime("%d"), \
                    #time.strftime("%H"), time.strftime("%M"), time.strftime("%S")))

            data = []
            data.append(nowtime)
            data.append(temp)
            data.append(humid)
            
            with open(fname, "a") as f:
                wr = csv.writer(f, delimiter=",", lineterminator='\n')
                wr.writerow(data)
            
    time.sleep(5) # time interval

