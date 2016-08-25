import requests, json

class SlackAPI():
	def __init__(self, token):
		self.TOKEN = token
		self.domain = 'https://slack.com/api/'

	def get_channel_list(self):
		"""returns updated channel list"""
		response_dict = json.loads(requests.get(
					self.domain + 'channels.list',
					params={
						'token': self.TOKEN
					}
				).text)
		self.channel_list = response_dict["channels"]
		return self.channel_list

	def get_channel_name(self, channel_id):
		"""returns the channel name when given an id"""
		self.channel_list = self.get_channel_list()
		for channel in self.channel_list:
			if channel["id"] == channel_id:
				return channel["name"]

	def get_channel_id(self, channel_name):
		"""returns the channel id when given a name"""
		self.channel_list = self.get_channel_list()
		for channel in self.channel_list:
			if channel["name"] == channel_name:
				return channel["id"]
