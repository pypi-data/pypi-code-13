#!/usr/bin/env python
# encoding: utf-8
__version__ = '1.0'
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , login_user , login_required
from flask import flash , request , render_template , url_for , redirect
from flask_mail import Mail, Message


template_folder = os.path.dirname(os.path.dirname(__file__)) + '/templates'
static_folder = os.path.dirname(os.path.dirname(__file__)) + '/static'


core = Flask('app', template_folder=template_folder , static_folder=static_folder)
core.config.from_object('onyx.bddconfig')
db = SQLAlchemy(core)

from controllers import *
from models import *

core.config['SECRET_KEY'] = 'onyx'


from onyx.core.assets import getAlarm
getAlarm.setAlarm()




