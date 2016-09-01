# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import time
from flask import Flask, Response, Request, request
from hookman.hookman.webs.event_tasks  import run_work

app = Flask(__name__)
PROJECT_DIR = './'
# app.debug = True

@app.route('/', methods=['POST'])
def home():
    event = request.headers.get('X-GitHub-Event', 'ping')
    if event == 'ping':
        return Response('pong')
    if event == 'push':
        run_work(projectdir=PROJECT_DIR)
        return Response('hookman-0.1.0 get')


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # global PROJECT_DIR
        PROJECT_DIR = sys.argv[1]
    app.run(host='0.0.0.0', port=3610)