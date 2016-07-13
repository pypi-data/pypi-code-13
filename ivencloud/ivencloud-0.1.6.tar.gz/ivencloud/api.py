""" iven cloud api """
from hashlib import sha1
import hmac
import requests
import json
from models import IvenResponse
from time import sleep

callback_fxn = None
activation_url = "http://demo.iven.io/activate/device"
data_url = "http://demo.iven.io/data"
api_key = None
break_loop = False
freq = 0
isFreqSet = False


def activate_device(secret_key, device_uid):
    """
    Activates device in Iven Cloud.
    Devices must be activate first to be able to send data.

    :param secret_key: string
    :param device_uid: string
    :return: IvenResponse object on success, None on error
    """

    if device_uid is not None and isinstance(device_uid, str) and \
                    secret_key is not None and isinstance(secret_key, str) and \
            bool(device_uid) and bool(secret_key):
        global api_key

        # HMAC-SHA1 encryption to get activation code
        hashed = hmac.new(secret_key, device_uid, sha1)
        activation_code = hashed.digest().encode("hex")
        headers = {'Activation': activation_code, 'Content-Type': "application/json"}
        r = requests.get(activation_url, headers=headers)
        ir = IvenResponse()
        ir.status = r.status_code
        if r.status_code < 500 and 'application/json' in r.headers['Content-Type']:
            j = r.json()
            if 'api_key' in j:
                api_key = j['api_key']
                ir.api_key = api_key  # this may be wrong reference garbage collector wont delete
            if 'description' in j:
                ir.description = j['description']
            if 'device_uid' in j:
                ir.device_uid = j['device_uid']
            if 'ivenCode' in j:
                ir.iven_code = j['ivenCode']
        return ir
    else:
        return None  # TODO: Add error result codes


def send_data(datas):
    """
    Sends data to Iven Cloud
    Device must be activated to be able to send data

    :param datas: dictionary
    :return: IvenResponse object on success, error codes on error
    """
    if api_key is not None:
        if isinstance(datas, dict) and bool(datas):
            headers = {'API-KEY': api_key, 'Content-Type': "application/json"}

            # turn data into json string
            payload = {"data": []}
            payload['data'].append(datas)
            if isFreqSet:
                # TODO: need to change
                payload['data'].append({"task": 0})
            r = requests.post(data_url, data=json.dumps(payload), headers=headers)  # TODO:add null check
            ir = IvenResponse()
            ir.status = r.status_code
            if r.status_code < 500 and 'application/json' in r.headers['Content-Type']:
                j = r.json()
                if 'description' in j:
                    ir.description = j['description']
                if 'ivenCode' in j:
                    ir.iven_code = j['ivenCode']
                if 'task' in j:
                    if j['ivenCode'] == 10180:  # change this
                        global freq
                        freq = j['task']
                if 'message' in j:
                    ir.message = j['message']
                    if 'UPDATE_REQUIRED' in ir.message:
                        ir.need_firm_update = True
                    if 'CONFIGURATION_UPDATE_REQUIRED' in ir.message:
                     ir.need_conf_update = True
            return ir
        else:
            # datas is NULL or not valid format
            return [None, 1]  # TODO: Change return type
    else:
        # Api key is not set
        return [None, 2]


def send_data_wloop(data, frequency, callback):
    """
    *** This function is blocking ***
    Sends the given data repeatedly. To stop sending data call break_sendloop function in
    the callback

    :param data: dictionary
    :param frequency: int as seconds
    :param callback: function(param)
    :return:
    """

    if set_frequency(frequency) is True:
        global break_loop
        while break_loop is False:
            if api_key is not None and data is not None:
                ir = send_data(data)
                callback(ir)  # TODO: check callback is not null
                sleep(freq)
        break_loop = False
        return True
    return False


def set_frequency(_freq):
    """
    Sets time interval for send_data_wloop function

    :param _freq: int as seconds
    :return: True on success
    """
    if _freq > 0:
        global freq
        freq = _freq
        return True
    return False


def break_sendloop():
    """
    Breaks the next while loop in the send_data_wloop function
    Call this method on the callback of send_data_wloop function

    :return: void
    """
    global break_loop
    break_loop = True

