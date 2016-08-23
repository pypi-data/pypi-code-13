#!/usr/bin/env python3
import time
from functools import wraps

def print_x(msg,logger=None):
	if logger:
		logger.info(msg)
	else:
		print(msg)

def retry(ExceptionToCheck, tries=3, delay=1, backoff=1,stoponerror=False, logger=None):
	'''
	Retry calling the decorated function using an exponential backoff.
    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to retry before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param stoponerror: Stop running if still error after mutil-trying
    :type stoponerror:bool
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
	Note: raise the error again in except block if you want to print
		customized msg written by yourself. eg:
		-----------------------------------------------------------------------
		@retry(HTTPError) #accept Error-obj or tuple of Error-obj
		def get_req(self):
			try:
				response=urlopen(self.url)
			except HTTPError as he:
				#This following line is customized msg mentioned above.
				msg='Occured HttpErrors {0}: {1}'.format(self.url,he.__str__())
				logger.error(msg)
				raise   <---------Here it is
		-----------------------------------------------------------------------
	'''
	def deco_retry(f):

		@wraps(f)
		def f_retry(*args, **kwargs):
			mtries, mdelay ,mlogger= tries, delay, logger
			while mtries >= 0:
				try:
					return f(*args, **kwargs)
				except ExceptionToCheck as e:
					if mtries > 0:
						msg = "Error:{0}. Retrying in {1} seconds...".format(e, mdelay)
						print_x(msg, logger=mlogger)
						time.sleep(mdelay)
					else:
						msg="Error:{0}".format(e)
						print_x(msg, logger=mlogger)
					mtries -= 1
					mdelay *= backoff
			if stoponerror:
				return f(*args, **kwargs)

		return f_retry  # true decorator
	return deco_retry
