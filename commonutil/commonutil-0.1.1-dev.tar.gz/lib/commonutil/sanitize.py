
# -*- coding: utf-8 -*-

""" 非法字元清除輔助函式庫 / Routines perform text sanitize """


# {{{ 以下常數字串可搭配 via_allowed() 等使用黑/白名單的函式使用

WHITE_CHARACTERS = " \t\n\r\v\f\x00"	#: 應被視為空白字元的字元集 (常用於進行 strip 處理) / Characters treat as spaces in general cases
DWHITE_CHARACTERS = ". \t\n\r\v\f\x00"	#: 應被視為空白字元由檔名前後去除的字元集 (常用於進行檔名的 strip 處理，比單純的空白字元集多了點號) / Characters treat as spaces in file name

ALPHANUMBERDASHUL_CHARCTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"	#: 大小寫英文字母、數字、減號、底線 / Upper and lower case of alphabets, digits, dash and underline
ALPHANUMBER_CHARCTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"	#: 大小寫英文字母與數字 / Upper and lower case of alphabets and digits

# }}} 以上常數字串可搭配 via_allowed() 等使用黑/白名單的函式使用



def path_component(original_name):
	"""
	將給定檔案或資料夾名稱中的不允許字元轉換成底線 (``_``) 並去除在頭或尾的點 (``.``) 與空白 (``\\ \\t\\r\\n``)
	不允許字元包含 ``\\/*?:<>|\\t\\n\\r`` (不包含空白).

	Replace illegal characters in given purposed file name with underline.
	Spaces and dots at beginning and end of purposed name will be stripped.

	Args:
		original_name: 原訂檔名 / Purposed file name

	Returns:
		重組後檔名 / Sanitized file name
	"""
	if not isinstance(original_name, unicode):
		original_name = unicode(original_name, "utf-8", "ignore")
	return u''.join([u"_" if (c in u"\\/*?:<>|\t\n\r") else c for c in original_name.strip(u". \t\n\r\v\f\x00")])
# ### def path_component


def via_allowed(val, allowed_characters="0123456789", replace_char="_", strip_characters=None):
	"""
	將字串中未列在允許字元的字元代換成指定字元

	Replace characters in given string which does not included in white list with given character.

	Characters at beginning and end of given string will be stripped if which is included in strip character list.

	Args:
		val: 要處理的字串 / String to be sanitized
		allowed_characters="0123456789": 允許的字元 / Allowed characters
		replace_char="_": 非允許字元要代換成的字元 / Character to replace illegal characters
		strip_characters=None: 如指定則檢查前進行 strip() 操作 / Characters to be strip from begin and end of given string

	Returns:
		重組後的字串 / Sanitized string
	"""
	val = str(val)
	if strip_characters is not None:
		val = val.strip(strip_characters)
	return ''.join([c if (c in allowed_characters) else replace_char for c in val])
# ### def via_allowed



# vim: ts=4 sw=4 ai nowrap
