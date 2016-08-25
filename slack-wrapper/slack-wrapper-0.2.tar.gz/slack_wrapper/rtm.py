import websocket, json, requests

class SlackRTM():
	def __init__(self, token):
		self.TOKEN = token
		self.connected = False
	def connect(self):
		self.ws = websocket.WebSocket()
		self.json_response = json.loads(requests.get(
					'https://slack.com/api/rtm.start',
					params={
						'token': self.TOKEN,
						'simple_latest': 'true',
		                                'no_unreads': 'true'
					}).text)
		if self.json_response['ok']:
			self.socket_url = self.json_response['url']
			print('url received:', self.socket_url)
			self.ws.connect(self.socket_url)
			hello = self.receive_dict()
			if hello['type'] == 'hello':
				print('Successfully connected to socket')
				return True
			elif hello['type'] == 'error':
				print('Error connecting to the socket...')
				print('Error message:', hello['error']['msg'])
				retry = input('Retry?(Y/n)')
				if retry.lower() == 'y' or retry == '':
					return self.connect()
				else:
					return False


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
