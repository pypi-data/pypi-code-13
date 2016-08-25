#!/usr/bin/env python3
import json
import re

NUMBER_RE = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))

global ALL_DICT_IN_RESPONSE
ALL_DICT_IN_RESPONSE=[]
def crtt_make_scanner(context):
    parse_object = context.parse_object
    parse_array = context.parse_array
    parse_string = context.parse_string
    match_number = NUMBER_RE.match
    strict = context.strict
    parse_float = context.parse_float
    parse_int = context.parse_int
    parse_constant = context.parse_constant
    object_hook = context.object_hook
    object_pairs_hook = context.object_pairs_hook
    memo = context.memo

    def _scan_once(string, idx):
        global ALL_DICT_IN_RESPONSE
        try:
            nextchar = string[idx]
        except IndexError:
            raise StopIteration(idx)

        if nextchar == '"':
            return parse_string(string, idx + 1, strict)
        elif nextchar == '{':
            all_dict= parse_object((string, idx + 1), strict,
                _scan_once, object_hook, object_pairs_hook, memo)
            ALL_DICT_IN_RESPONSE.append(all_dict[0])
            return all_dict
        elif nextchar == '[':
            return parse_array((string, idx + 1), _scan_once)
        elif nextchar == 'n' and string[idx:idx + 4] == 'null':
            return None, idx + 4
        elif nextchar == 't' and string[idx:idx + 4] == 'true':
            return True, idx + 4
        elif nextchar == 'f' and string[idx:idx + 5] == 'false':
            return False, idx + 5

        m = match_number(string, idx)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = parse_float(integer + (frac or '') + (exp or ''))
            else:
                res = parse_int(integer)
            return res, m.end()
        elif nextchar == 'N' and string[idx:idx + 3] == 'NaN':
            return parse_constant('NaN'), idx + 3
        elif nextchar == 'I' and string[idx:idx + 8] == 'Infinity':
            return parse_constant('Infinity'), idx + 8
        elif nextchar == '-' and string[idx:idx + 9] == '-Infinity':
            return parse_constant('-Infinity'), idx + 9
        else:
            raise StopIteration(idx)

    def scan_once(string, idx):
        try:
            return _scan_once(string, idx)
        finally:
            memo.clear()

    return _scan_once


class jsondecoder(json.decoder.JSONDecoder):
	def __init__(self, object_hook=None, parse_float=None,
		parse_int=None, parse_constant=None, strict=True,
		object_pairs_hook=None):
		"""Sub class of json.decoder.JSONDecoder, the purpose of this is to change:
		self.scan_once = scanner.make_scanner(self) ---->
		self.scan_once = scanner.py_make_scanner(self)
		Finally to get all dict by changing the class json.decoder.JSONObject
		"""
		self.object_hook = object_hook
		self.parse_float = parse_float or float
		self.parse_int = parse_int or int
		self.parse_constant = parse_constant or json.decoder._CONSTANTS.__getitem__
		self.strict = strict
		self.object_pairs_hook = object_pairs_hook
		self.parse_object = json.decoder.JSONObject
		self.parse_array = json.decoder.JSONArray
		self.parse_string = json.decoder.py_scanstring
		self.memo = {}
		self.scan_once = crtt_make_scanner(self)
		self.all_dicts={}
	def raw_decode(self, s, idx=0):
		try:
			global ALL_DICT_IN_RESPONSE
			ALL_DICT_IN_RESPONSE=[]
			obj, end = self.scan_once(s, idx)
			self.all_dicts=ALL_DICT_IN_RESPONSE
		except StopIteration as err:
			raise JSONDecodeError("Expecting value", s, err.value) from None
		return obj, end

json._default_decoder=jsondecoder(object_hook=None, object_pairs_hook=None)
