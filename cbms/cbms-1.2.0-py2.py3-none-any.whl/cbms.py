#
# The cbms module is used to interface with the API on the CBMS SVM.
# It uses HTTP Post requests to the REST Web Service.
#

# Import the requests module for sending http requests
import sys, traceback, requests, time, threading
from threading import Thread, Lock

# Constants for the IO point types
AI = 0
AO = 1
BI = 2
BO = 3

EXT_NONE = 0
EXT_BACNET = 1

IDLE = 0
CHANGED = 1

mutex = Lock()

#
# Io models an Io point in the CBMS SVM
#
class Io:
    def __init__(self, type, path, description, ext):
        self.type = type
        self.path = path
        self.description = description
        self.ext = ext
        self.readValue = 0
        self.writeValue = 0
        self.ts = -1
        self.errorValue = 0
        self.state = CHANGED

    def dump(self):
        print("path=%(path)s" % {"path": self.path})

    def addPayload(self):
        res = "%(path)s" % {"path": self.path}

        if (self.type == AI):
            res += " type=AI;"
        elif (self.type == AO):
            res += " type=AO;"
        elif (self.type == BI):
            res += " type=BI;"
        elif (self.type == BO):
            res += " type=BO;"

        res += "description=" + self.description + ";"

        if (self.ext == EXT_BACNET):
            res += "ext=BACnet;"

        res += "\n"

        return res

    def readPayload(self):

        if (self.type == AO):
            return "%(path)s %(ts)d\n" % {"path": self.path, "ts": self.ts}
        elif (self.type == BO):
            return "%(path)s %(ts)d\n" % {"path": self.path, "ts": self.ts}

        return ""

    def writePayload(self):
        if (self.state == IDLE):
            return ""
        self.state = IDLE

        res = "%(path)s " % {"path": self.path}

        if (self.type == AI or self.type == AO):
            res += "F %(readValue)f " % {"readValue": self.readValue}
        elif (self.type == BI or self.type == BO):
            res += "B %(readValue)d " % {"readValue": self.readValue}

        res += str(self.errorValue)

        res += "\n"

        return res

    def setReadValue(self, readValue):
        if (self.readValue != readValue):
            self.state = CHANGED
        self.readValue = readValue

    def setWriteValue(self, writeValue, error, ts):
        if (self.type == AI or self.type == AO):
            self.writeValue = float(writeValue)
        elif (self.type == BI or self.type == BO):
            self.writeValue = int(writeValue)
        self.ts = int(ts)
        self.errorValue = int(error)
        self.write(self.writeValue, self.errorValue)


#
# CbmsIo models the IO handler function
#
class Api:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.points = {}

    def add(self, io):
        self.points[io.path] = io

    def dump(self):
        for key, point in self.points.items():
            point.dump()

    def addPayload(self):
        payload = ""
        mutex.acquire()
        for key, point in self.points.items():
            payload += point.addPayload()
        mutex.release()
        return payload

    def readPayload(self):
        payload = ""
        mutex.acquire()
        for key, point in self.points.items():
            payload += point.readPayload()
        mutex.release()
        return payload

    def writePayload(self):
        payload = ""
        mutex.acquire()
        for key, point in self.points.items():
            payload += point.writePayload()
        mutex.release()
        return payload

    def write(self, line):
        args = line.split(' ')
        if (len(args) != 4):
            return
        mutex.acquire()
        if args[0] in self.points:
            point = self.points[args[0]]
            point.setWriteValue(args[1], args[3], args[2])
        mutex.release()

    def url(self, method):
        s = self.host
        if (self.port != 80):
            s += ":" + str(self.port)
        return s + "/io/" + method

    def start(self):
        host = self.host
        if (self.port != 80):
            host += ":" + str(self.port)
        while True:
            try:
                requests.post(self.url("add"), data=self.addPayload())
                print("Connected to " + host)
                break
            except KeyboardInterrupt:
                return
            except ConnectionError:
                print("Cannot connect to " + host, sys.exc_info()[0])
            except:
                return

        readWorker = WriteThread(self)
        readWorker.daemon = True
        readWorker.start()

        writeWorker = ReadThread(self)
        writeWorker.daemon = True
        writeWorker.start()

        while threading.active_count() > 0:
            time.sleep(0.01)

#
# Worker thread for updating the readValues
#
class WriteThread(Thread):
    def __init__(self, api):
        Thread.__init__(self)
        self.api = api

    def work(self):
        try:
            # Update the read value in all of the points
            mutex.acquire()
            for key, point in self.api.points.items():
                if hasattr(point, 'read'):
                    point.read()
            mutex.release()

            #Write the read values to the CBMS SVM
            payload = self.api.writePayload()
            if (len(payload) > 0):
                #print("Writing readValues")
                requests.post(self.api.url("write"), data=payload)
        except:
            print("Write readValues failed", sys.exc_info()[0])

    def run(self):
        while True:
            self.work()
            time.sleep(0.01)

#
# Worker thread for reading the writeValues from the SVM and writing the data to the physical IO
#
class ReadThread(Thread):
    def __init__(self, api):
        Thread.__init__(self)
        self.api = api

    def work(self):
        try:
            #Update the read value in all of the points
            payload = self.api.readPayload()
            if (len(payload) > 0):
                #print("Reading writeValues")
                r = requests.post(self.api.url("read"), data=payload)
                if (r.status_code == 200 and len(r.text) > 0):
                    lines = r.text.splitlines()
                    for line in lines:
                        self.api.write(line)
        except:
            print("Read writeValues failed", sys.exc_info()[0])

    def run(self):
        while True:
            self.work()

