#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import os.path
from shutil import copy
from flask import Flask
import flask
import requests
import json
import time
import logging

from flask_cors import CORS
import myterm.color
import myterm.log
from myterm.parser import arg, verb, alias, VerbParser

from flaskserver import __version__

app = Flask(__name__, template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates'))

DESCRIPTION = """client for ablog"""
AUTHOR = "Frederic Aoustin"
PROG = "flaskserver"
VERSION = __version__
GETBOOL = {'false': False, 'true': True}

def first_value(*args):
    for arg in args:
        if arg != None:
            return arg
    return args[-1]
    
def getUrl(base, path):
    url = path[len(base):]
    return '/'.join(url.split(os.sep))

def getParent(path):
    parent = '/'.join([i for i in path.split('/') if len(i)][:-1])
    if parent:
        return '/' + parent + '/'
    return '/'

class StreamHandler(logging.StreamHandler):
    """
        Change level by http code
    """
    def __init__(self, stream=None):
        logging.StreamHandler.__init__(self, stream)
    
    def emit(self, record):
        try:
            http_return = int(record.msg.split('-')[-2].split(' ')[-2])
            if http_return >= 400:
                record.levelno = 30
            if http_return >= 500:
                record.levelno = 40
        except:
            pass
        logging.StreamHandler.emit(self, record)        

class HistoryHandler(logging.StreamHandler):
    """
        Change level by http code
    """
    def __init__(self, stream=None):
        logging.StreamHandler.__init__(self, stream)
        self.history = []

    def emit(self, record):
        try:
            http_return = int(record.msg.split('-')[-2].split(' ')[-2])
            if http_return >= 400:
                record.levelno = 30
            if http_return >= 500:
                record.levelno = 40
        except:
            pass
        self.history.append(record)        


@app.route("/icons/folder.gif")
def iconfolder():
    return flask.send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates'), 'folder.gif')

@app.route("/icons/file.gif")
def iconfile():
    return flask.send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates'), 'file.gif')

@app.route("/icons/back.gif")
def iconback():
    return flask.send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates'), 'back.gif')

@app.route("/api/status")
def url_status():
    return json.dumps({'status':'run', 
                    'version':__version__, 
                    'path': app.config['PATH_HTML'],
                    'host' : app.config['HOST'],
                    'port' : app.config['PORT'],
                    'python' : '.'.join([str(a) for a in sys.version_info[0:3]])})

@app.route("/api/stop")
def url_stop():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route("/api/log")
def url_log():
    try:
        limit = -1 * int(flask.request.args.get('limit'))
    except:
        limit = -1 * len(app.config['historylog'].history)
    return json.dumps([ {'level' :record.levelno, 'msg': record.getMessage()}  for record in app.config['historylog'].history[limit:]])

@app.route("/")
@app.route("/<path:path>")
def static_web(path=""):
    try:
        if os.path.isdir(os.path.join(app.config['PATH_HTML'],path)):# and path[-1]== "/":
            if os.path.isfile(os.path.join(app.config['PATH_HTML'],path, app.config['DIRECTORY_INDEX'])):
                elt = os.path.abspath(os.path.join(app.config['PATH_HTML'],path, app.config['DIRECTORY_INDEX']))
                return flask.redirect(getUrl(app.config['PATH_HTML'],elt))#"/" + path + app.config['DIRECTORY_INDEX'])
            if app.config['INDEX']:
                parent = getParent(path)
                dirs = []
                files = []
                for i in os.listdir(os.path.join(app.config['PATH_HTML'],path)):
                    elt = os.path.abspath(os.path.join(app.config['PATH_HTML'],path,i))
                    if os.path.isfile(elt):
                        files.append({'name':i, 'path': getUrl(app.config['PATH_HTML'],elt) })#elt[len(app.config['PATH_HTML']):]})
                    else:
                        dirs.append({'name':i, 'path': getUrl(app.config['PATH_HTML'],elt)+'/'})#elt[len(app.config['PATH_HTML']):]+'/'})
                return flask.render_template('dirs.html', parent= parent, path=path, dirs=dirs, files=files)
            return flask.abort(404)
        return flask.send_from_directory(app.config['PATH_HTML'],path)
    except: 
        flask.abort(404)

def check_arg(verb, arg, value):
    if arg == 'host':
        return first_value(value, app.config.get('HOST',None), '0.0.0.0')
    if arg == 'port':
        return first_value(value, app.config.get('PORT',None), 5001)
    if arg == 'cors':
        return GETBOOL[first_value(value, app.config.get('CORS',None), 'false')]



def arg_flask(func):
    arg(func, '-H', '--host', dest='host', type=str, default=None, check=check_arg,
        help="host of web server")
    arg(func, '-p', '--port', dest='port', type=int, default=None, check=check_arg,
        help="port of web server")
    return func

def _log(type, message, *args, **kwargs):
    getattr(app.logger, type)(message.rstrip(), *args, **kwargs)

import werkzeug._internal
werkzeug._internal._log = _log

@verb('start', usage="%s start [options] path" % PROG) 
@arg_flask
@arg('--cors', dest='cors', choices = ['true', 'false'], type='choice', default=None, help="cors authorization")
@arg('-d', dest='detach', action = "store_true", default=False, help="detach process")
@arg('--no-log', dest='nolog', action = "store_true", default=False, help="not print log")
def start(path=None, host=None, port=None, color=None, cors=None, detach=False, nolog=False):
    """start web server"""
    if detach:
        sys.argv.append('--no-log')
        idx = sys.argv.index('-d')
        del sys.argv[idx]
        cmd = sys.executable + ' ' + ' '.join([sys.argv[0], 'start'] + sys.argv[1:])
        if os.name == 'nt':
            cmd = 'start /B %s' % cmd
        else:
            cmd = '%s &' % cmd
        os.system(cmd)
    else:    
        app.config['PATH_HTML']= first_value(os.path.abspath(path), app.config.get('PATH_HTML',None), os.getcwd())
        app.config['HOST'] = first_value(host, app.config.get('HOST',None), '0.0.0.0')
        app.config['PORT'] = int(first_value(port, app.config.get('PORT',None), 5001))
        app.logger.setLevel(logging.DEBUG)
        app.config['historylog'] = HistoryHandler()
        app.logger.addHandler(app.config['historylog'])
        if not nolog:
            app.logger.addHandler(StreamHandler())
        if cors: CORS(app)
        app.run(host = app.config['HOST'],
                port = app.config['PORT'],
                threaded = True)

@verb('status')
@arg_flask
def status(host=None, port=None):
    """status web server"""
    app.config['HOST'] = first_value(host, app.config.get('HOST',None), '0.0.0.0')
    app.config['PORT'] = int(first_value(port, app.config.get('PORT',None), 5001))
    if app.config['HOST'] == "0.0.0.0": 
        host="127.0.0.1"
    else:
        host = app.config['HOST']
    port = app.config['PORT']    
    try:
        rep = requests.get('http://%s:%s/api/status' % (host,port))
        if rep.status_code == 200:
            try:
                rep = json.loads(rep.text)
                for k in rep:
                    print('%s\t: %s' % (k, rep[k]))
            except:
                print('web server is not flaskserver', file=sys.stderr)
        else:
            print('web server is not flaskserver', file=sys.stderr)
    except:
        print('web server is not started', file=sys.stderr)


@verb('stop')
@arg_flask
def stop(host=None, port=None):
    """stop of web server"""
    app.config['HOST'] = first_value(host, app.config.get('HOST',None), '0.0.0.0')
    app.config['PORT'] = int(first_value(port, app.config.get('PORT',None), 5001))
    if app.config['HOST'] == "0.0.0.0": 
        host="127.0.0.1"
    else:
        host = app.config['HOST']
    port = app.config['PORT']    
    try:
        if requests.get('http://%s:%s/api/status' % (host, port)).status_code == 200:
            requests.get('http://%s:%s/api/stop' % (host,port))
            print('web server is stopped', file=sys.stdinfo)
        else:
            print('web server is not flaskserver', file=sys.stderr)
    except:
        print('web server is not flaskserver or not start', file=sys.stderr)
 
@verb('log')
@arg_flask
@arg('-l', '--limit', dest='limit', type=int, default=20, help="limit of record log")
def log(host=None, port=None, limit=0):
    """view log of web server"""
    app.config['HOST'] = first_value(host, app.config.get('HOST',None), '0.0.0.0')
    app.config['PORT'] = int(first_value(port, app.config.get('PORT',None), 5001))
    if app.config['HOST'] == "0.0.0.0": 
        host="127.0.0.1"
    else:
        host = app.config['HOST']
    port = app.config['PORT']    
    try:
        res = requests.get('http://%s:%s/api/log?limit=%s' % (host, port, limit))
        if res.status_code == 200:
            for record in json.loads(res.text):
                if record['level'] >= 30:
                    print(record['msg'], file=sys.stderr)
                else:    
                    print(record['msg'], file=sys.stdinfo)
        else:
            print('web server is not flaskserver', file=sys.stderr)
    except:
        print('web server is not flaskserver or not start', file=sys.stderr)

if __name__ == "__main__":
    try:
        if not os.path.isfile(os.path.join(os.path.expanduser("~"),'.flaskserver','conf.py')):
            if not os.path.isdir(os.path.join(os.path.expanduser("~"),'.flaskserver')):
                os.mkdir(os.path.join(os.path.expanduser("~"),'.flaskserver'))
            copy(os.path.join(os.path.dirname(__file__),'flask.py'), os.path.join(os.path.expanduser("~"),'.flaskserver','conf.py'))
    except:
        pass
    app.config.from_pyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)),'flask.conf'))
    if os.path.isfile(os.path.join(os.path.expanduser("~"),'.flaskserver','conf.py')):
        app.config.from_pyfile(os.path.join(os.path.expanduser("~"),'.flaskserver','conf.py'))
    if os.path.isfile(os.path.join(os.getcwd(), 'flask.conf')):
        app.config.from_pyfile(os.path.join(os.getcwd(),'flask.conf'))
    for key in os.environ:
        if key.startswith('FLASKSERVER_') and key.isupper():
           app.config[key[len('FLASKSERVER_'):]] = os.environ.get(key)
    parser = VerbParser()
    parser.prog = PROG
    parser.version = "%s %s" % (PROG, VERSION)
    parser.description= DESCRIPTION
    parser.epilog = AUTHOR
    parser.parse_args()
