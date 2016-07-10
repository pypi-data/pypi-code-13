import sys
import requests


def help():
    print('Usage: simdict word')


def get_definition(word):
    url = "https://api.shanbay.com/bdc/search/?word=%s" % word
    data = requests.get(url).json()
    if data['status_code'] == 0:
        print("uk:[%s] us:[%s] \n%s" % (data['data']['pronunciations']['uk'], data[
              'data']['pronunciations']['us'], data['data']['definition']))
    else:
        print("Not Found!")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            help()
        else:
            get_definition(sys.argv[1])
    else:
        help()
