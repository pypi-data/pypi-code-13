from jsonrpc import dispatcher
from .rpc import RpcClient, RpcServer
import socket, asyncore, multiprocessing

class MAPI():
    def __init__(self, module):
        self.mod = module

    def InvokeCommand(self, cmd_data):
        command = self.mod.commands[cmd_data["Name"]]
        command.get("Fun")(cmd_data["Msg"], cmd_data["Args"])
        return ""

class Module:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.master = RpcClient()
        self.commands = dict()
        self.lock = multiprocessing.Lock()
        self.port = 0

    def start_rpc_server(self):
        mapi = MAPI(self)
        dispatcher.build_method_map(mapi, self.name+".")
        rpc = RpcServer("localhost")
        self.port = rpc.socket.getsockname()[1]

    def add_command(self, name, command):
        self.commands[name] = command
        data = dict(Name=name, Module=self.name)
        self.master.call("Master.RegisterCommand", data)

    def register(self):
        self.start_rpc_server()
        self.master.call("Master.Register", dict(Port=str(self.port), Name=self.name))
        asyncore.loop()

    def say(self, channel, text):
        self.master.call("Master.Send", channel + " :" + text)
