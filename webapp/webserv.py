import Adafruit_DHT as dht
from flask import Flask, render_template
#from gpiozero

app = Flask(__name__)

@app.route('/')
def index():
    sensor = dht.DHT22
    pin = 4

    humidity, temperature = dht.read_retry(sensor, pin)
    temp = round(temperature, 1)
    humid = round(humidity, 1)
    DHT = { 'temp' : temp, 'humid' : humid }
    return render_template('index.html', **DHT)

if __name__ == '__main__':
    app.run(debug=True, port = 80, host = '0.0.0.0')

