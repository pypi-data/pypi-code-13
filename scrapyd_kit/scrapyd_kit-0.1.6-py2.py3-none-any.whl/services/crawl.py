# -*- coding: utf-8 -*-

import os
import json
from twisted.internet import reactor
from twisted.web import resource
from twisted.web import server
from subprocess import Popen, PIPE
from scrapyd.utils import get_crawl_args

class Crawl(resource.Resource):

    json_encoder = json.JSONEncoder()

    def __init__(self, root):
        resource.Resource.__init__(self)
        self.root = root

    def _render_object(self, obj, txrequest):
        r = self.json_encoder.encode(obj) + "\n"
        txrequest.setHeader('Content-Type', 'application/json')
        txrequest.setHeader('Access-Control-Allow-Origin', '*')
        txrequest.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE')
        txrequest.setHeader('Access-Control-Allow-Headers',' X-Requested-With')
        txrequest.setHeader('Content-Length', len(r))
        return r

    def jsonize(self, request, data):
        try:
            data = json.loads(data)
            return {'code': 0, 'message': 'success', 'data': data}
        except ValueError as e:
            request.setResponseCode(500)
            return {'code': 1, 'message': 'json parse error', 'errors': data}

    def crawl(self, args):
        env = os.environ.copy()
        cmd = ['scrapy', 'crawl']
        args['_spider'] = args.get('spider')
        args['_project'] = args.get('project')
        cargs = get_crawl_args(args)
        cmd = cmd + cargs + ['-t', 'json', '-o', '-']
        process = Popen(cmd, stdin=PIPE, stdout=PIPE, env=env)
        out, _ = process.communicate()
        return out

    def blockingio(self, request):
        settings = request.args.pop('setting', [])
        settings = dict(x.split('=', 1) for x in settings)
        args = dict((k, v[0]) for k, v in request.args.items())
        out = self.crawl(args)
        data = self.jsonize(request, out)
        resp = self._render_object(data, request)
        request.write(resp)
        request.finish()

    def render_POST(self, request):
        reactor.callInThread(self.blockingio, request)
        return server.NOT_DONE_YET
