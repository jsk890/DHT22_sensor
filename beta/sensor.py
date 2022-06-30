''' --------------------------------
AM2302 DHT22
Humidity & Temperature Sensor Logger
by hgstyler on python
-------------------------------- '''

import sys
import board
import adafruit_dht
from os import path
import time
import csv

now = time.localtime()
today = ("%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday))
fpath = '/home/pi/git/DHT22_sensor/Log/'
location = 'Tr_Room'
fname = fpath + location + '_' + today + '.csv'

if path.exists(fname)==False:
    with open(fname, "w") as f:
        wr = csv.writer(f, delimiter=",", lineterminator='\n')
        wr.writerow(['Time', 'Temp(*C)', 'Humid(%)'])

while True:
    try:
        # AdaFruit old ver.
        '''
        humidity, temperature = dht.read_retry(dht.DHT22, 4)
        '''

        # Adafruit_circuitpython_dht ver.
        #SENSOR_PIN = 4
        #POS = "THOx"

        dht22 = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        temperature1 = dht22.temperature
        humidity1 = dht22.humidity

        if humidity1 is not None and temperature1 is not None: # read failure check
            if humidity1 < 100.1: # out of range in humidity check
                humid = round(humidity1, 1)
                temp = round(temperature1, 1)
            
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
            
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(5)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(5) # time interval

