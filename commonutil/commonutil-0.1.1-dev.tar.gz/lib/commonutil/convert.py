
# -*- coding: utf-8 -*-

""" 值轉換輔助函式值 / Value convert functions """

import re
import datetime
import uuid

import logging
_log = logging.getLogger(__name__)



def to_text(v, default_value=None):
	"""
	將輸入值轉換為字串，當輸入值為 None 或空字串或是無法轉換的物件時傳回 None

	Convert given variable into string. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		非空字串，或是 None 當輸入是空字串或是無法轉換的物件
	"""
	if v is None:
		return default_value
	# {{{ convert to unicode string
	r = None
	if isinstance(v, unicode):
		r = v
	elif isinstance(v, str):
		r = unicode(v, 'utf-8', 'ignore')
	else:
		try:
			r = unicode(str(v), 'utf-8', 'ignore')
		except:
			_log.warning("cannot convert input (%r) to string @[convert.to_text]", v)
			r = None
	# }}} convert to unicode string
	if r is not None:
		r = r.strip()
		if len(r) > 0:
			return r
	return default_value
# ### def to_text


def to_integer(v, default_value=None):
	"""
	將輸入值轉換為整數，當輸入值為 None 或是無法轉換的物件時傳回 None

	Convert given variable into integer. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		整數，或是 None 當輸入是空字串或是無法轉換的物件
	"""
	if v is None:
		return default_value
	try:
		r = int(v)
		return r
	except:
		_log.warning("cannot convert input (%r) to integer @[convert.to_integer]", v)
	return default_value
# ### def to_integer

def to_float(v, default_value=None):
	"""
	將輸入值轉換為浮點數，當輸入值為 None 或是無法轉換的物件時傳回 None

	Convert given variable into float. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		非空字串，或是 None 當輸入是空字串或是無法轉換的物件
	"""
	if v is None:
		return default_value
	try:
		r = float(v)
		return r
	except:
		_log.warning("cannot convert input (%r) to float @[convert.to_float]", v)
	return default_value
# ### def to_float


def to_bool(v, default_value=None):
	"""
	將輸入值轉換為布林值，當輸入值為 None 或是無法轉換的物件時傳回 None

	Convert given variable into boolean. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		布林值，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	try:
		if isinstance(v, bool):
			return v
		if isinstance(v, (str, unicode,)):
			if len(v) < 1:
				return False
			elif str(v[0]) in ('Y', 'y', 'T', 't', '1', '+',):
				return True
			return False
		elif isinstance(v, (int, float,)):
			return True if (int(v) > 0) else False
		else:
			return bool(v)
	except:
		_log.warning("cannot convert input (%r) to boolean @[convert.to_bool]", v)
	return default_value
# ### def to_bool


_DATETIME_REGEX_yyyymmddhhmmss = re.compile('([0-9]{4})-?([0-9]{2})-?([0-9]{2})[_T\s\.]?([0-9]{2})?[\:\.\s_]?([0-9]{2})?[\:\.\s_]?([0-9]{2})?')
_DATETIME_REGEX_hhmmoffset = re.compile('([-+]?)([0-9]{2})([0-9]{2})?')
def to_datetime(v, default_value=None):
	"""
	將輸入值轉換為時間格式，當輸入值為 None 或是無法轉換的物件時傳回 None

	Convert given variable into datetime.datetime object. Return None or given default value when convert failed.

	輸入範例 / Input Examples:
		整數/浮點數 (視為 UNIX time-stamp) / Integer or Float (will treat as UNIT time-stamp):
			1352454146.387523
		字串 / String:
			'2012-11-10 10:10:10', '+01' (加 1 小時), '+0123' (加 1 小時 23 分鐘)
		串列或數對 / List or Tuple):
			(2012, 11, 10, 10, 10, 10, 0, 0, 0,)

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		時間格式，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	if isinstance(v, datetime.datetime):
		return v
	elif isinstance(v, (int, float,)):
		return datetime.datetime.fromtimestamp(v)
	elif isinstance(v, (str, unicode,)):
		m = _DATETIME_REGEX_yyyymmddhhmmss.match(v)
		if m is not None:
			year = to_integer(m.group(1), 1970)
			month = to_integer(m.group(2), 1)
			day = to_integer(m.group(3), 1)
			hour = to_integer(m.group(4), 0)
			minute = to_integer(m.group(5), 0)
			second = to_integer(m.group(6), 0)
			return datetime.datetime(year, month, day, hour, minute, second)
		m = _DATETIME_REGEX_hhmmoffset.match(v)
		if m is not None:
			direction = m.group(1)
			hour_offset = to_integer(m.group(2), 0)
			minute_offset = to_integer(m.group(3), 0)
			# when not +/- mode, replace given hour and minute into current time as result
			current_tstamp = datetime.datetime.now()
			if (direction is None) or ("" == direction):
				return current_tstamp.replace(hour=hour_offset, minute=minute_offset, second=0)
			# when not offset to any time point
			if (0 == hour_offset) and (0 == minute_offset):
				return current_tstamp
			# when offset symbol (+/-) is given
			d = datetime.timedelta(hours=hour_offset, minutes=minute_offset)
			if '-' == direction:
				return current_tstamp - d
			else:
				return current_tstamp + d
	elif isinstance(v, (list, tuple,)):
		year = None
		month = 1
		day = 1
		hour = 0
		minute = 0
		second = 0
		if len(v) >= 3:
			year = to_integer(v[0], 1970)
			month = to_integer(v[1], 1)
			day = to_integer(v[2], 1)
		if len(v) >= 4:
			hour = to_integer(v[3], 0)
		if len(v) >= 5:
			minute = to_integer(v[4], 0)
		if len(v) >= 6:
			second = to_integer(v[5], 0)
		# return result if valid
		if year is not None:
			return datetime.datetime(year, month, day, hour, minute, second)
	_log.warning("cannot convert input (%r) to datetime @[convert.to_datetime]", v)
	return default_value
# ### def to_datetime


def to_uuid(v, default_value=None):
	"""
	將輸入值轉換為 UUID 物件

	Convert given variable into UUID object. Return None or given default value when convert failed.

	Args:
		v: 要轉換的值或物件
		default_value=None: 預設值

	Returns:
		uuid.UUID 物件實體，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	if isinstance(v, uuid.UUID):
		return v
	try:
		aux = uuid.UUID(v)
		return aux
	except:
		pass
	return default_value
# ### def to_uuid



def to_list(v, element_converter, default_value=None):
	"""
	將輸入值轉換為串列，各輸入值透過傳入的轉換函式進行轉換

	Convert given variable into list object with given element convert function.
	Return None or given default value when convert failed or result into empty list.

	Args:
		v: 要轉換的值或物件
		element_converter (callable): 單一個元素的轉換函式，當轉換結果為 None 時此元素會被丟棄
		default_value=None: 預設值

	Returns:
		串列，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	result = []
	if isinstance(v, (list, tuple, set,)):
		for e in v:
			item = element_converter(e)
			if item is not None:
				result.append(item)
	else:
		item = element_converter(v)
		if item is not None:
			result.append(item)
	if len(result) > 0:
		return result
	return default_value
# ### def to_list

def to_dict(v, element_converter, key_converter=None, default_value=None):
	"""
	將輸入值轉換為字典，各輸入值透過傳入的轉換函式進行轉換

	Convert given variable into dict object with given key and value convert function.
	Return None or given default value when convert failed or result into empty dict.

	Args:
		v: 要轉換的值或物件
		element_converter (callable): 單一個元素的轉換函式，當轉換結果為 None 時此元素會被丟棄
		key_converter=None (callable): 單一元素對應之鍵值的轉換函式，當轉換結果為 None 時此元素會被丟棄
		default_value=None: 預設值

	Return:
		字典，或是 None 當輸入無法轉換
	"""
	if v is None:
		return default_value
	if key_converter is None:
		key_converter = to_text
	result = {}
	if isinstance(v, dict):
		for k, e in v.iteritems():
			kidx = key_converter(k)
			if kidx is None:
				continue
			item = element_converter(e)
			if item is not None:
				result[kidx] = item
	if len(result) > 0:
		return result
	return default_value
# ### def to_dict



_HOSTPORT_ADDR_REGEX = re.compile("(.+)\\:([0-9]+)$")
def parse_hostport_location(loc, default_value=None):
	"""
	解析 Host:Port 型式的字串為 (Host, Port,) 型式的 tuple 物件

	Parse string in "Host:Port" form into tuple object in (Host, Port,) form.

	Args:
		loc (list of str): 要轉換的位址字串
		default_value=None: 當無法轉換時的預設值

	Returns:
		轉換結果，或是當失敗時為預設值
	"""
	m = _HOSTPORT_ADDR_REGEX.match(str(loc))
	if m is not None:
		addr = m.group(1)
		port = int(m.group(2))
		return (addr, port,)
	return default_value
# ### def parse_hostport_location

def parse_hostport_location_list(location_list):
	"""
	解析 Host:Port 型式的字串 list 為 (Host, Port,) 型式的 tuple 物件所構成的 list

	Parse list of strings in "Host:Port" form into list of tuple objects in (Host, Port,) form.

	Args:
		location_list (list of str): 要轉換的位址字串串列

	Returns:
		轉換結果，或是當失敗時為空的 tuple 物件
	"""
	return to_list(location_list, parse_hostport_location, ())
# ### def parse_hostport_location_list



# vim: ts=4 sw=4 ai nowrap
