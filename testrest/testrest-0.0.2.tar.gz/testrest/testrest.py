import requests
import datetime
import time
import inspect
import os
import json


class Dictfactory(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, v):
        res = self.base.copy()
        res.update(v)
        return res


def r(method, url, headers={}, **kwargs):
    header = {'user-agent': "Testrest version: 1", }
    header.update(headers)
    t0 = datetime.datetime.utcnow()
    req = requests.request(method, url, headers=header, **kwargs)
    t1 = datetime.datetime.utcnow()
    keys = "url status_code url content reason encoding"
    res = {}
    for k in keys.split():
        res[k] = getattr(req, k)
    res["response_headers"] = dict((k.lower(), v)
                                   for k, v in req.headers.items())
    res["request_headers"] = dict((k.lower(), v)
                                  for k, v in req.request.headers.items())
    res["elapsed_response"] = req.elapsed.total_seconds()
    res["elapsed_total"] = (t1 - t0).total_seconds()
    res["method"] = method
    return res


def test(method, url, conditions={}, headers={}, requests_kwargs={}):
    req = r(method=method, url=url, headers=headers, **requests_kwargs)
    res = {
        'created': datetime.datetime.utcnow().isoformat(),
        'ts': time.time(),
        'request': req,
        'conditions': [],
        'result': [],
        'pass': True
    }
    for name, predicate in conditions.items():
        p = predicate(req)
        res['conditions'].append((name,
                                  p, ))
        if not p:
            res['pass'] = False
    return res


class Suite(object):
    def __init__(self, base_url="", **requests_kwargs):
        self.base_url = base_url
        self.requests_kwargs = requests_kwargs
        self.tests = []

    def t(self, name, method, url, fun, setup=[], **requests_kwargs):
        kwargs = self.requests_kwargs.copy()
        kwargs.update(requests_kwargs)
        self.tests.append((name, method, url, fun, kwargs, setup))

    def r(self, method, url, **requests_kwargs):
        u = "%s%s" % (self.base_url, url)
        kwargs = self.requests_kwargs.copy()
        kwargs.update(requests_kwargs)

        def fun():
            r(method, u, **kwargs)

        return fun

    def run(self, names=[]):
        all_results = []
        for name, method, url, fun, requests_kwargs, setup in self.tests:
            if len(names) > 0 and name not in names:
                continue
            for setup_fun in setup:
                setup_fun()
            u = "%s%s" % (self.base_url, url)
            req = r(method, u, **requests_kwargs)
            res = {
                'created': datetime.datetime.utcnow().isoformat(),
                'name': name,
                'request': req,
                'outcome': "pass" if fun(req) else "fail",
                'pass': fun(req),
                'ts': time.time(),
            }
            yield res

    def pretty(self, verbose=False, names=[]):

        q = self.run(names)
        for res in q:
            lines = []
            if not res["pass"]:
                lines.append("")
            lines.append("%s\t%s\t%s" % (res["created"], res["outcome"],
                                         res["name"]))
            if verbose or not res["pass"]:
                lines.append("%s %s %s %s" % (res["request"]["method"],
                                              res["request"]["url"],
                                              res["request"]["status_code"],
                                              res["request"]["reason"], ))
                lines.extend(
                    ["> %s:%s" % (k, v)
                     for k, v in res["request"]["request_headers"].items()])
                lines.extend(
                    ["< %s:%s" % (k, v)
                     for k, v in res["request"]["response_headers"].items()])
                try:
                    z = json.loads(res["request"]["content"])
                    lines.append(json.dumps(z, sort_keys=True, indent=4))
                except ValueError:
                    lines.append(res["request"]["content"])
            print("\n".join(lines))
