#import sys
import time
#import csv
#import json
#from os import path
#flask 설치 필요
from flask import Flask, request, jsonify, render_template
import RPi.GPIO as GPIO 

sw_pin_list = [8, 15, 18]  # 스위치로 사용할 핀
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)     


GPIO.setup(sw_pin_list[0], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)   
GPIO.setup(sw_pin_list[1], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(sw_pin_list[2], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

sw_state_list = [0, 0, 0]   # 스위치 눌림 기록

app = Flask(__name__)  


def ReadButton():
	if not GPIO.input(8):
		return True
	else:
		return False

@app.route('/')                       # 기본 주소
def home():
    for ii in range(3):               # 눌림여부 저장
        sw_state_list[ii] = GPIO.input(sw_pin_list[ii])
    return render_template('bmsmain.html', sw_state_list = sw_state_list)   
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
