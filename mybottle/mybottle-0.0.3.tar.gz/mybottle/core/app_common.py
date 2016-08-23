# -*- coding:utf-8 -*-
from bottle import TEMPLATE_PATH, Bottle

from mybottle.libs import log

app = Bottle()
TEMPLATE_PATH.append('tpl/')
app.install(log.stopwatch)

