

class InstanceCase():

    def run(self, API, sleep):
        API.conn.call('DescribeInstances')
