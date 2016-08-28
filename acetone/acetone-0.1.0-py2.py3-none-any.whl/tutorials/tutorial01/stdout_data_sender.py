import sys


# This class has the same interface as DataSender class. There is no inheritance to
# demonstrate that it's not required (you know, it's Python after all).
class StdoutDataSender(object):
    def send_data(self, data):
        sys.stdout.write(data)
        sys.stdout.write('\n')
