import websocket, json, requests

class SlackRTM():
	def __init__(self, token):
		self.TOKEN = token
		self.connected = False
	def connect(self):
		self.ws = websocket.WebSocket()
		self.connection_json = json.loads(requests.get(
					'https://slack.com/api/rtm.start',
					params={
						'token': self.TOKEN,
						'simple_latest': 'true',
		                                'no_unreads': 'true'
					}).text)
		self.connect_url = self.connection_json['url']
		self.ws.connect(self.connect_url)
		if True: #TODO if response is ok...
			self.connected = True
			return True
	def receive(self):
		return self.ws.recv()
	def receive_dict(self):
		return json.loads(self.ws.recv())
	def msg(self, msg, channel="D0HJBJSG3"): #channel with therightman
		self.ws.send(json.dumps({
                	"id": 1,
        	        "type": "message",
	                "channel": channel,
                	"text": msg
        	}))
