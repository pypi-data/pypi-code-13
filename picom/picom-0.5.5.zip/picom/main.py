# Standard library imports
import requests
import json
import socket
import os

api_id = None
api_key = None
deviceId = None
ip = None

tokenData = None
BASE_JSON_STRUCTURE = """{
    "idA" :"",
    "key": "",
    "deviceId": "",
    "ip":""
}"""

# Get the credentials from a JSON file
try:
    tokenFile = open("token.json", 'r')
    tokenData = tokenFile.read()
    tokenFile.close()
    tokenData = json.loads(tokenData)
except IOError:
    tokenFile = open("token.json", "w")
    tokenFile.write(BASE_JSON_STRUCTURE)
    tokenData = json.loads(BASE_JSON_STRUCTURE)
    tokenFile.close()

api_id = tokenData['idA']
api_key = tokenData['key']
deviceId = tokenData['deviceId']
ip = tokenData['ip']


def get_credentials():
    return tokenData


def store_API_id(idA):
    global api_id
    tokenData['idA'] = idA
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(tokenData))
    tokenFile.close()
    api_id = idA


def storeAPI_key(key):
    global api_key
    tokenData['key'] = key
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(tokenData))
    tokenFile.close()
    api_key = key


def store_credentials(APIId, APIKey):
    global api_id
    global api_key
    tokenData['idA'] = APIId
    tokenData['key'] = api_key
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(tokenData))
    tokenFile.close()
    api_key = APIKey
    api_id = APIId


def store_id(idD):
    global deviceId
    tokenData['deviceId'] = idD
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(tokenData))
    tokenFile.close()
    deviceId = idD


def store_ip(ipD):
    global ip
    tokenData['ip'] = ipD
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(tokenData))
    tokenFile.close()
    ip = ipD


def store_all(idG, key, ipD, dID):
    global api_id, api_key, ip, deviceId
    tokenData['idA'] = idG
    tokenData['key'] = key
    tokenData['ip'] = ipD
    tokenData['deviceId'] = dID
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(tokenData))
    tokenFile.close()
    api_id = idG
    api_key = key
    ip = ipD
    deviceId = dID


def renew_credentials():
    headers = {'Device-Id': api_id, 'Device-Key': api_key}
    r = requests.post("http://" + ip + "/api/v1/device/gen_token/{}".format(deviceId), headers=headers)
    res = r.json()
    store_credentials(res['token_id'], res['token_key'])


def test_connection():
    headers = {'Device-Id': api_id, 'Device-Key': api_key}
    r = requests.get("http://{}/api/v1/ping".format(ip), headers=headers)
    if "Pong" in r.text:
        return True
    else:
        return r.text


def get_api_free():
    headers = {'Device-Id': api_id, 'Device-Key': api_key}
    r = requests.get("http://" + ip + "/api/v1/apifrees", headers=headers)
    return r.json()


def update_garage_state(garage, state):
    headers = {'Device-Id': api_id, 'Device-Key': api_key}
    payload = {"state": state}
    r = requests.post("http://{ip}/api/v1/garage/{garage_id}".format(ip=ip, garage_id=garage),
                      data=payload, headers=headers)
    return r.status_code


def get_garages():
    headers = {'Device-Id': api_id, 'Device-Key': api_key}
    r = requests.get("http://{ip}/api/v1/garages".format(ip=ip), headers=headers)
    try:
        return r.json()
    except json.decoder.JSONDecodeError:
        return "{} // {}".format(r.status_code, r.text)

def send_alarm_signal():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 5402))
    s.send(("{api_id}*{api_key}*alarm/".format(api_id=api_id, api_key=api_key)).encode())

