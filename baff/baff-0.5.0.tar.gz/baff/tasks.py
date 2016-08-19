import time
import threading


class Tarea(object):
    """ Based on a system process pipe, it calls a CLI command
    and receive the "stderr", "stdout" and can send "stdin".
    Also it counts the time process have been running before it
    exists. There is a unique "token" that identify this
    specific instance. """
    __slots__ = ['id', 'pipe', 'time_start', 'time_end',
                 'token']
                 

class Thread(threading.Thread):
    """ A wrapper for a python function that contains more
    information """
    __slots__ = ['id', 'time_start', 'time_end',
                 'token']

class RequestThread(threading.Thread):
    """ A process can be a background request. Which uses
    module 'requests' to send and receive HTTP requests. """
    __slots__ = ['id', 'time_start', 'time_end', 'request',
                 'finished', 'response']

    def __init__(self, request):
        super(RequestThread, self).__init__()
        self.finished = False
        self.request = request

    def run(self):
        s = requests.Session()
        try:
            request = s.prepare_request(self.request)
            response = s.send(request)
            self.response = response
            print(response.status_code)
        except requests.ConnectionError:
            print("error")

        self.finished = True