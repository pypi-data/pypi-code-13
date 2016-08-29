import sys
import os
import requests
import webbrowser
from codecs import open


DATA_DIR = './data'
MPORT = 8000

SERVER_ADDRESS = ''

JQ_ADDRESS = 'http://code.jquery.com/jquery-latest.min.js'
STY_ADDRESS = 'http://aimath.org/knowlstyle.css'
JS_ADDRESS = 'http://aimath.org/knowl.js'


browser = "open -a /Applications/Google\ Chrome.app %s"

if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

sys.path.append(DATA_DIR)

confs = [JQ_ADDRESS, STY_ADDRESS, JS_ADDRESS]
for address in confs:
    filename = os.path.join(DATA_DIR,address.split('/')[-1])
    if not os.path.exists(address):
        page = requests.get(address)
        with open(filename,'w', encoding='utf-8') as f:
            f.write(page.content)
