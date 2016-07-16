from slackclient import SlackClient

class Bot:

    def __init__(self, token):
        self.token = token

    def connect(self):
        self.client = SlackClient(self.token)
        self.client.rtm_connect()

    def read_msg(self):
            print("Connection Established")


    def hello(self):
        self.client.api_call("chat.postMessage", channel="#general", text="Hello World")
    
