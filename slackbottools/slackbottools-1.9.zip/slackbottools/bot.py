from slackclient import SlackClient

class Bot:

    def __init__(self, token):
        self.token = token
        print(self.token)

    def connect(self):
        print(self.token)
        self.client = SlackClient(self.token)
        self.client.rtm_connect()

    def read_msg(self):
            print("Connection Established")


    def hello(self):
        self.posttoken = self.token
        self.client.api_call("chat.postMessage", token=self.posttoken, channel="#general", text="Hello World")
    
