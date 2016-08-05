import requests

def send(key, title, message):
    if not key or not message:
        raise ValueError("Key and message argument must be set")

    if title:
        requests.get('https://api.simplepush.io/send/%s/%s/%s' % (key, title, message))
    else:
        requests.get('https://api.simplepush.io/send/%s/%s' % (key, message))
