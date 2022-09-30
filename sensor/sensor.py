''' -------------------------------------------------
AM2302 DHT22 (updated module compatible with RasPi 4)
Humidity & Temperature Sensor Logger
by hgstyler on Python
------------------------------------------------- '''

import sys
import board
import adafruit_dht # pip3 install adafruit-circuitpython-dht
from os import path
import time
import csv

# assign initial value for previous temp, humid
prevhumid = -99.9
prevtemp = -99.9

# sensor read loop
while True:
    try: # normal case to read temp & humid sucessfully
        # raw humid, temp data (GPIO 4)
        dht22 = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        temperature = dht22.temperature
        humidity = dht22.humidity

        # current time
        now = time.localtime()
        today = ("%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday))

        # csv file save folder
        # current save folder: '/home/pi/dev/DHT22_sensor_log/'
        # you can change the context of fpath in order to change csv save folder
        fpath = '/home/pi/dev/DHT22_sensor/log/'

        # csv file name
        location = 'Tr_Room'
        fname = fpath + location + '_' + today + '.csv'

        # data list generation for csv
        if humidity is not None and temperature is not None: # read failure check
            if humidity < 100.1: # out of range in humid check
                # humid & temp for data list
                humid = round(humidity, 1)
                temp = round(temperature, 1)

                # out of normal range in temp, humid
                if prevhumid != -99.9 and abs(humid - prevhumid) >= 10.0:
                    continue
                if prevtemp != -99.9 and abs(temp - prevtemp) >= 5.0:
                    continue

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

                # print on screen -> skip for multi py run
                # print('Temp(raw): {0:}*C  Humid(raw): {1:}%  {2:} {3:}'.format(temp, humid, nowdate, nowtime))

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

                # save csv file
                if path.exists(fname)==False:
                    # create new csv when date is changed
                    # header label: Date | Time | Temp(*C) | Humid(%) | dTemp(*C) | dHumid(%) | Cal. Temp(*C) | Cal. Humid (%) | Cal. Msg
                    with open(fname, "w") as f:
                        wr = csv.writer(f, delimiter=",", lineterminator='\n')
                        header_csv = ['Date', 'Time', 'Temp(*C)', 'Humid(%)', 'dTemp(*C)', 'dHumid(%)', 'Cal. Temp(*C)', 'Cal. Humid(%)', 'Cal. Msg']
                        wr.writerow(header_csv)
                        wr.writerow(data)
                
                else:
                    # add new data row
                    with open(fname, "a") as f:
                        wr = csv.writer(f, delimiter=",", lineterminator='\n')
                        wr.writerow(data)

                #previous temp, humid
                prevtemp = temp
                prevhumid = humid

        # wait 5 sec for next loop
        time.sleep(5)

    except RuntimeError as error: # runtime error case
        # print error -> skip for multi py run
        # print(error.args[0])
        time.sleep(5)
        continue
    except Exception as error: # reading sensor error case
        dhtDevice.exit()
        # raise error -> skip for multi py run
        # raise error

