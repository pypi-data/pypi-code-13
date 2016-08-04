
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.cmd import Command



class Serve_PyDoc(Command):
	""" 啟動 PyDoc 伺服程式 / Run PyDoc server """

	# Brief (40-50 characters) description of the command
	description = "start up pydoc serve"

	# List of option tuples: long name, short name (None if no short name), and help string.
	user_options = [
		('port', 'p', 'specify the listening port',),
	]

	def initialize_options(self):
		self.port = 8080
	# ### def initialize_options

	def finalize_options(self):
		self.port = int(self.port)
		if (self.port < 1024) or (self.port > 32767):
			self.port = 8080
	# ### def finalize_options

	def run(self):
		import pydoc
		def pydocserv_ready(server):
			print '> serving at: %r ...' % (server.url,)
		def pydocserv_stopped():
			print '> pydoc server stopped.'
		pydoc.serve(self.port, pydocserv_ready, pydocserv_stopped)
	# ### def run
# ### class Serve_PyDoc



setup(name='commonutil',
		version='0.1.1-dev',
		url='https://bitbucket.org/cheyinl/commonutil-py',
		description='Common utility functions',
		packages=['commonutil', ],
		package_dir={'': 'lib'},
		cmdclass={'serv_doc': Serve_PyDoc, },
		classifiers=['Development Status :: 5 - Production/Stable',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: MIT License',
			'Operating System :: POSIX',
			'Programming Language :: Python :: 2.6',
			'Programming Language :: Python :: 2.7', ],
		license='MIT License',
	)



# vim: ts=4 sw=4 ai nowrap
