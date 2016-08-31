import paho.mqtt.client as mqtt
import time
import json
import sys
import datetime
import ssl
import subprocess
class testli:
    IP = "192.168.1.38"
    PORT = "1883"

    def on_message(client, userdata, msg):
        data = json.dumps(json.loads(str(msg.payload))["command"]["command"]["name"])
        if('"update"' == str(data)):
            print(msg.topic+" "+str(data))
            cmd=['easy_install', '--upgrade' ,'PI_INFO_SENDER']
            p=subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            p.wait()
            print("done")
            python = sys.executable
            os.execl(python, python, * sys.argv)

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("SiteWhere/commands/ccc-cccc-cccccccccc")

    def on_publish(client, userdata, msg):
        print "Message has been sent."
    
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(IP,PORT,60)

    client.loop_start()

    while True:
    
        strDate = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        temperature = json.dumps({"hardwareId" : "ccc-cccc-cccccccccc",
                              "type": "DeviceMeasurements"
                              ,"request": {"measurements": {"temperature":"37",
                                                            "humidity":"50" },
                                           "updateState": "true",
                                           "eventDate": strDate }})
     
        client.publish("SiteWhere/input/json", temperature, qos=1)


        time.sleep(1)
