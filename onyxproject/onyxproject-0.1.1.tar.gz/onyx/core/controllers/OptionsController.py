#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask import render_template
from flask.ext.login import login_required

@core.route('/options')
@login_required
def options():
    return render_template('options/index.html')