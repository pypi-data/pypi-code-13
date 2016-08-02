import simplejson as json

data = '{ "data": { } , "cmd": "list", "ret_text": "0 todos.", "ret": 0 }'

print json.loads(data)
