import re
from io import BytesIO

from ccjob import CommonCrawl

class GoogleAnalytics(CommonCrawl):

    def mapper_init(self):
        self.pattern = re.compile('[\"\']UA-(\d+)-(\d)+[\'\"]')

if __name__ == '__main__':
    GoogleAnalytics.run()
