import urllib2
import urllib
import json

class DingTalk:

    def __init__(self, token, post_string):
        self.token = token
        self.post_string = string


    def dingtalk_bot(self):
        data = {
            'msgtype': 'text', 'text': {'content': '%s' % self.post_string}
        }
        json_str = json.dumps(data)
        req = urllib2.Request(
            "https://oapi.dingtalk.com/robot/send?access_token=%s" % self.token, json_str)
        req.add_header('Content-type', 'application/json')
        response = urllib2.urlopen(req, timeout=120)
        return response.read()