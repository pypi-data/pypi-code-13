# Copyright 2016 BMC Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
import socket
import sys


class PortScan:
    def __init__(self):
        self.host = None
        self.port = None
        self.result = None
        self.response = None

    def checkArgs(self, args):
        if len(args) != 3:
            self.usage()
            sys.exit(1)
        self.setHost(sys.argv[1])
        self.setPort(int(sys.argv[2]))

    def total_seconds(self, td):
        return (float(td.microseconds) + (float(td.seconds) + float(td.days) * 24 * 3600) * 10 ** 6) / 10 ** 6

    def usage(self):
        sys.stderr.write("usage: {} <hostname> <port>\n".format(sys.argv[0]))
        sys.stderr.write("\n")
        sys.stderr.write("where:\n")
        sys.stderr.write("   hostname - Host to check status of port\n")
        sys.stderr.write("   port - Port to check status\n")

    def printMetric(self):
        if self.result == 0:
            lresult = 1
        else:
            lresult = 0
        print("BOUNDARY_PORT_AVAILABILITY {0} {1}".format(lresult, self.host))
        print("BOUNDARY_PORT_RESPONSE {0} {1}".format(self.response, self.host))

    def setHost(self, host):
        self.host = host

    def setPort(self, port):
        self.port = port

    def execute(self):
        self.checkArgs(sys.argv)
        self.scan()
        self.printMetric()

    def scan(self):
        t1 = datetime.now()
        try:
            ip = socket.gethostbyname(self.host)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.result = sock.connect_ex((ip, self.port))
            sock.close()
        except KeyboardInterrupt:
            print "You pressed Ctrl+C"
            sys.exit()
        except socket.gaierror:
            print("Hostname could not be resolved. Exiting")
        except socket.error:
            print("Couldn't connect to server")

        # Checking the time again
        t2 = datetime.now()

        # Calculates the difference of time, to see how long it took to run the script
        t = t2 - t1
        self.response = self.total_seconds(t) * 1000


if __name__ == "__main__":
    p = PortScan()
    p.execute()
