import paho.mqtt.client as mqtt
import time
import json
import sys
import datetime
import ssl
import subprocess
import os
from Adafruit_BME280 import *
from PI_MONITOR import * 
class testli:
    IP = "192.168.1.38"
    PORT = "8883"
    sensor = BME280(mode=BME280_OSAMPLE_8)

    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()
        
    def on_message(client, userdata, msg):
        data = json.dumps(json.loads(str(msg.payload))["command"]["command"]["name"])
        if(str(data) == '"flashLed"'):
            print(msg.topic+" "+str(data))
            GPIO.output(18,GPIO.HIGH)
        if('"flashLedoff"' == str(data)):
            print(msg.topic+" "+str(data))
            GPIO.output(18,GPIO.LOW)
        if('"update"' == str(data)):
            path = json.dumps(json.loads(str(msg.payload))["command"]["parameters"]["path"])
            print(msg.topic+" "+str(data))
            os.system("sudo easy_install --upgrade "+path)
            time.sleep(5)
            print("done")
            python =sys.executable
            os.execl(python,python,*sys.argv)
        if('"monitor"' == str(data)):
            datasend = {}
          

            cpu_info = getCPUuse()
            

            ram_info = getRAMinfo()
            

            disk_info = getDISKinfo()
            strDate = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            temperature = json.dumps({"hardwareId" : "ccc-cccc-cccccccccc",
                              "type": "DeviceMeasurements"
                              ,"request": {"measurements": {"CPUtemperature":getCPUtemp(),

"CPU_USAGE":cpu_info[0],    "RAM_USAGE":ram_info[1]},
                                           "updateState": "true",
                                           "eventDate": strDate }})
     
            client.publish("SiteWhere/input/json", temperature, qos=1)
    
    
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("SiteWhere/commands/ccc-cccc-cccccccccc")

    def on_publish(client, userdata, msg):
        print "Message has been   sent."
    
    
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.tls_set("client.crt")
    client.connect(IP,PORT,60)

    client.loop_start()
 

    while 1:
        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()
        hectopascals = pascals / 100
        humidity = sensor.read_humidity()
    
        strDate = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        temperature = json.dumps({"hardwareId" : "ccc-cccc-cccccccccc",
                              "type": "DeviceMeasurements"
                              ,"request": {"measurements": {"temperature":degrees,
                                                            "humidity": humidity },
                                           "updateState": "true",
                                           "eventDate": strDate }})
     
        client.publish("SiteWhere/input/json", temperature, qos=1)


        time.sleep(10)
