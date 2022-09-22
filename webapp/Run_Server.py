import sys
import time
# communication gpio
import board
import csv
# import json
from os import path
# need to install 'pip3 install adafruit-circuitpython-dht'
import adafruit_dht
#need to install 'flask'
from flask import Flask, request, jsonify, render_template
import copy

humid = 60.0
temp = 24.0
prevHumid = 60.0
prevTemp = 24.0
prevTime = ''

app = Flask(__name__)  

# rendering main page
@app.route('/')
def home():
    return render_template('main.html')  

@app.route("/callHT")
def callHT():
    
    try:# normal case to read temp & humid sucessfully
        # raw humid, temp data (GPIO 4)
        global humid,temp,prevHumid,prevTemp,prevTime
        dht22 = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        temperature = dht22.temperature
        humidity = dht22.humidity
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
                nowdate = ("%04d - %02d - %02d" % (now.tm_year, now.tm_mon, now.tm_mday)) 
                nowtime = ("%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec)) 
                
                
                prevTime = nowtime
                prevHumid = humid
                prevTemp = temp

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
                
                # return to html
                return jsonify(hum=humid, tem=temp, date=nowdate, time=nowtime)
    
    except RuntimeError as error: # runtime error case
        humid = prevHumid
        temp = prevTemp
        tmptime = prevTime
        # return to html
        return jsonify(hum=humid, tem=temp, time=tmptime)
    except Exception as error: # reading sensor error case
        humid = prevHumid
        temp = prevTemp
        tmptime = prevTime
        # return to html
        return jsonify(hum=humid, tem=temp, time=tmptime)


# connecting port
if __name__ == "__main__":
	app.run(port = "8080", debug=True)
