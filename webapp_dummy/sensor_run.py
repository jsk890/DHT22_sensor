import sys
import time
import board
import csv
#import json
from os import path
#need to install 'pip3 install adafruit-circuitpython-dht'
import adafruit_dht
#need to install 'flask'
from flask import Flask, request, jsonify, render_template
import RPi.GPIO as GPIO 

#now = time.localtime()
#today = ("%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday))
#fpath = '/home/pi/dev/DHT22_/Log/'
#location = 'Tr_Room'
#fname = fpath + location + '_' + today + '.csv'

#if path.exists(fname)==False:
#    with open(fname, "w") as f:
#        wr = csv.writer(f, delimiter=",", lineterminator='\n')
#        wr.writerow(['Time', 'Temp(*C)', 'Humid(%)'])

'''
sw_pin_list = [8, 15, 18]  # 스위치로 사용할 핀
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)     


GPIO.setup(sw_pin_list[0], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)   
GPIO.setup(sw_pin_list[1], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(sw_pin_list[2], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

sw_state_list = [0, 0, 0]   # 스위치 눌림 기록
'''
app = Flask(__name__)  

@app.route("/_callHT")
def callHT():
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

                #print('Temp: {0:}*C  Humid: {1:}%  {2:} {3:}'.format(temp, humid, nowdate, nowtime))
                return jsonify(hum=humid, tem=temp)
                #print('Temp: {0:0.1f}*C Humid: {1:0.1f}% {2:}-{3:}-{4:} {5:}:{6:}:{7:}'.\
                    #format(temp, humid, \
                    #time.strftime("%Y"), time.strftime("%m"), time.strftime("%d"), \
                    #time.strftime("%H"), time.strftime("%M"), time.strftime("%S")))
	
    except RuntimeError as error:
        humid = '-'
        temp = '-'
        return jsonify(hum=humid, tem=temp)
    except Exception as error:
        humid = '-'
        temp = '-'
        return jsonify(hum=humid, tem=temp)
#   time.sleep(5) # time interval






def ReadButton():
	if not GPIO.input(8):
		return True
	else:
		return False

@app.route('/')                       # 기본 주소
def home():
    return render_template('bmsmain.html')   
    #button.html에 스위치 눌림 여부 전달

# 입력창에서 받은 데이터 처리

	
@app.route("/ajax_page", methods=['POST'])
def ajax_page():
	data = request.get_json()
	print(data)
	# html javascript ajax요청으로 부터 받은 데이터 저장
	calc_result = calc(data['inputdata'])
	# 입력받은 데이터 서버 확인용
	rdata = {}
	rdata['inputdata']=data['inputdata']
	rdata['rlt']=calc_result
	print("server : ", rdata)
	return jsonify(rdata)

def calc(inputdata):
	print("calc")
	return str(eval(inputdata))

# javascript에서 주기적으로 요청 할 함수
# 라즈베리 파이의 센서값을 읽어들여 json형식으로 변환
@app.route("/_button")
def _button():
    if ReadButton():
        state = "not pressed"
    else:
        state = "pressed"
        # javascript로 데이터 전송
    return jsonify(buttonState=state)



if __name__ == "__main__":
	app.run(port = "8080", debug=True)
