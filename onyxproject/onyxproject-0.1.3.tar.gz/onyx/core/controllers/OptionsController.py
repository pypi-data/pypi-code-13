#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask import render_template , redirect , url_for , flash
from flask.ext.login import login_required
import pip

@core.route('/options')
@login_required
def options():
    return render_template('options/index.html')

@core.route('/maj')
@login_required
def maj():
	pip.main(['install', '--upgrade', "onyxproject"])
	flash("Onyx vient d'etre mis a jour !",'success')
	return redirect(url_for('options'))