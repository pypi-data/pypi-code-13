from distutils.core import setup # import the setup function from Python's distribution utilities

setup (
	# these are the setup function's argument names
	name			= 'nesterHarkit',
	version 		= '1.0.4',
	py_modules		= ['nester'], # associate your module's metadata with the setup function's arguments
	author 			= 'Harkit',
	author_email	= 'harkit.shrestha@gmail.com',
	url				= 'http://www.thebukhara.com',
	description 	= 'A simple printer of nested lists',
)