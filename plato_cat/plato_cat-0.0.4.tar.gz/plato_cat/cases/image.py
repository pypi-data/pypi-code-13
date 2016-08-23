

class ImageCase():

    def run(self, API, sleep):
        API.conn.call('DescribeImages')
