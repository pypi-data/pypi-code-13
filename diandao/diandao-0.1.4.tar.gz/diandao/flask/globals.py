# -*- coding: utf-8 -*-

from functools import partial
from werkzeug.local import LocalStack, LocalProxy
from . import stacker


def _lookup_(name):
    return stacker[name]

app=LocalProxy(partial(_lookup_,"app"))