#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, platform, datetime


def _linux_get_system_memory():
	"""
	Get node total memory and memory usage.
	http://stackoverflow.com/a/17718729.
	"""

	try:

		with open('/proc/meminfo', 'r') as mem:
			ret = {}
			tmp = 0
			for i in mem:
				sline = i.split()
				if str(sline[0]) == 'MemTotal:':
					ret['total'] = int(sline[1])
				elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
					tmp += int(sline[1])
				ret['free'] = tmp
				ret['used'] = int(ret['total']) - int(ret['free'])
	except:

		return {'error': "can't read meminfo"}

	return ret

def _linux_uptime():
	"""
	Retrieves uptime for linux-based systems.
	"""

	try:

		with open('/proc/uptime', 'r') as f:

			uptime_seconds = float(f.readline().split()[0])

			uptime_string = str(datetime.timedelta(seconds = uptime_seconds))

		return {'seconds': uptime_seconds, 'string': uptime_string}

	except:

		return {'error': "can't read uptime"}

def get_current_date():
	"""
	Returns current hour.
	"""

	now = datetime.datetime.now()

	return {
	
		"year": now.year,
		"day": now.day,
		"month": now.month,
		"hour": now.hour,
		"minute": now.minute,
		"seconds": now.second
	}

def get_uptime():
	"""
	Retrieves system uptime.
	"""

	system_string = platform.system().lower()

	if system_string == 'linux':

		return _linux_uptime()
	else:

		return None

def get_system_memory():
	"""
	This function discovers system type and executes proper function.
	"""

	system_string = platform.system().lower()

	if system_string == 'linux':

		return _linux_get_system_memory()
	else:

		return {'total': None, 'used': None, 'free': None}


def get_system_info():
	"""
	Returns dict with system info
	"""

	return {
	
		"system": platform.system(),
		"version": platform.version(),
		"name": platform.node(),
		"uname": platform.uname(),
		"architecture": platform.architecture(),
		"machine": platform.machine(),
		"platform": platform.platform(),
		"processor": platform.processor(),
		"python_version": platform.python_version(),
		"date": get_current_date(),
		"uptime": get_uptime(),
		"memory": get_system_memory()
	}

if __name__ == '__main__':

	info_dict = get_system_info()

	for k, v in info_dict.items():

		print("{key}: {value}".format(key=k, value=v))
	
