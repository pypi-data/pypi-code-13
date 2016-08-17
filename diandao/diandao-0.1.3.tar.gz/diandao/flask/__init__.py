# -*- coding: utf-8 -*-
stacker = {"app":None}

from flask_sqlalchemy import SQLAlchemy as Flask_SQLAlchemy
from .globals import *


class SQLAlchemy(Flask_SQLAlchemy):

	def __init__(self, app=None, use_native_unicode=True, session_options=None, metadata=None):
		"""重构父级初始化方法,缓存app对象"""
	 	super(self.__class__, self).__init__(app, use_native_unicode, session_options, metadata)
	 	if app is not None:
	 		apply_app(app)
	 	pass

	def init_app(self, app):
		"""重构父级初始化方法,缓存app对象"""
		super(self.__class__, self).init_app(app)
		if app is not None:
			apply_app(app)
	 	pass

def apply_app(app):
	stacker["app"] = app
	app.config.setdefault("CACHE_LIFE_TIME", 600)
	


