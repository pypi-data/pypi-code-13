from Adafruit_BME280 import *
import paho.mqtt.client as mqtt
import time
import json
import sys
import RPi.GPIO as GPIO
import datetime
import os
import subprocess

IP = sys.argv[1]
PORT = sys.argv[2]
TOPIC = sys.argv[3]

sensor = BME280(mode=BME280_OSAMPLE_8)

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()

print 'Timestamp = {0:0.3f}'.format(sensor.t_fine)
print 'Temp      = {0:0.3f} deg C'.format(degrees)
print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
print 'Humidity  = {0:0.2f} %'.format(humidity)


def on_message(client, userdata, msg):
    data = json.dumps(json.loads(str(msg.payload))["command"]["command"]["name"])
    
    if(str(data) == '"flashLed"'):
        print(msg.topic+" "+str(data))
        GPIO.output(18,GPIO.HIGH)
    if('"flashLedoff"' == str(data)):
        print(msg.topic+" "+str(data))
        GPIO.output(18,GPIO.LOW)
    if('"update"' == str(data)):
        print(msg.topic+" "+str(data))
        cmd=['easy_install', '--upgrade' ,'PI_INFO_SENDER']
        p=subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        p.wait()
        python = sys.executable
        os.execl(python, python, * sys.argv)



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("SiteWhere/commands/ccc-cccc-cccccccccc")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.LOW)
    
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(IP,PORT,60)
client.loop_start()

while True:
    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()
    
    strDate = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    temperature = json.dumps({"hardwareId" : "ccc-cccc-cccccccccc","type": "DeviceMeasurements","request": {"measurements": {"temperature":degrees, "humidity":humidity }, "updateState": "true", "eventDate": strDate }})
     
    client.publish("SiteWhere/input/json", temperature, qos=1)

    print humidity

    time.sleep(1)

     
