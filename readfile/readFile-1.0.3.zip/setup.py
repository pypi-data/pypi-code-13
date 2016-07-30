from distutils.core import setup # import the setup function from Python's distribution utilities

setup (
	# these are the setup function's argument names
	name			= 'readFile',
	version 		= '1.0.3',
	py_modules		= ['readFile'], # associate your module's metadata with the setup function's arguments
	author 			= 'Harkit',
	author_email	= 'harkit.shrestha@gmail.com',
	url				= 'http://www.thebukhara.com',
	description 	= 'Is used to read the sketch.txt file',
)