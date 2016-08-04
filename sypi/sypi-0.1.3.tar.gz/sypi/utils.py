import logging, os, errno

LOG_FORMAT_STRING = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def mkdir_p(path):
	"""
	http://stackoverflow.com/a/600612/190597 (tzot)
	"""

	try:
		os.makedirs(path, exist_ok=True)  # Python>3.2
	except TypeError:
		try:
			os.makedirs(path)
		except OSError as exc: # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(path):
				pass
			else: raise


class MakeFileHandler(logging.FileHandler):
	"""
	http://stackoverflow.com/a/20667049
	"""

	def __init__(self, filename, mode='a', encoding=None, delay=0):            
	
		mkdir_p(os.path.dirname(filename))
		logging.FileHandler.__init__(self, filename, mode, encoding, delay)


def _logging_string_to_class(logging_level_str):
	"""
	"""

	if logging_level_str == 'debug':
		return logging.DEBUG

	elif logging_level_str == 'info':
		return logging.INFO

	elif logging_level_str == 'warning':
		return logging.WARNING

	elif logging_level_str == 'error':
		return logging.ERROR

	elif logging_level_str == 'critical':
		return logging.CRITICAL

	else:
		return logging.DEBUG

def create_file_handler(log_file, handler_level, formatter=logging.Formatter(LOG_FORMAT_STRING)):
	"""
	Creates file handler which logs even debug messages.
	"""

	fh = MakeFileHandler(log_file)
	fh.setLevel(_logging_string_to_class(handler_level))
	fh.setFormatter(formatter)

	return fh

def config_logger(name, log_file, formatter=logging.Formatter(LOG_FORMAT_STRING), logging_level='debug'):
	"""
	Returns logger object
	"""

	logger = logging.getLogger(name)
	logger.setLevel(_logging_string_to_class(logging_level))
	logger.addHandler(create_file_handler(log_file, logging_level, formatter))

	return logger