import threading
import subprocess
import time
import tornado.ioloop
import shlex
from api import Type
from multiprocessing import Event
from Queue import Empty as EmptyError, Queue
from tornado import gen
from tornado.ioloop import PeriodicCallback
from tasks import Tarea, RequestThread


class SyncLoop(PeriodicCallback):
    """ Main Loop of daemon it spawns all of the 
    processes and background requests. Itself is a thread."""

    def __init__(self, queue=None, tabs=None):
        super(SyncLoop, self).__init__(self.iteration, 1000)
        self.queue = queue
        self.tabs = tabs
        self.processing = []

    def iteration(self):
        """ This is the everytime execute statement, it checks
        if there is new requests in queue, if so, then
        checks if it's a CLI or Request and instance the
        respective classes and add them to process. Finally
        call the sync process. """

        try:
            item, token, options = self.queue.get(timeout=0)
            tab = self.tabs[item]
            tab_type = tab['type']

            print("encontrado")

            if tab_type == Type.CLI:
                if 'user' in tab:
                    command = ['su', tab['user'], '-c', tab['command']]
                else:
                    command = shlex.split(self.tabs[item]['command'])

                tarea = Tarea()
                tarea.pipe = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
                
                tarea.time_start = time.time()
                tarea.time_end = time.time()
                tarea.token = token

                self.processing.append(tarea)

            elif tab_type == Type.REQUEST:
                request = requests.Request('GET', tab['uri'])
                tarea = RequestThread(request)
                tarea.start()
                
            self.processing.append(tarea)

        except EmptyError:
            pass

        self.handle_processes_sync()

    def handle_processes_sync(self):
        """ Pool open pipes and active requests waiting them
        to finish, where pipe must be returncode different to
        None, and Request a fail or a server response """
        
        toremove = []
        for tarea in self.processing:
            if isinstance(tarea, RequestThread):
                if tarea.finished:
                    toremove.append(tarea)

            elif isinstance(tarea, Tarea):
                returncode = tarea.pipe.poll()
                if returncode is not None:
                    toremove.append(tarea)
                    print("done (token: {})".format(tarea.token))
                else:
                    tarea.time_end = time.time()

        for tarea in toremove:
            self.processing.remove(tarea)

    def stop(self):
        self.event.set()