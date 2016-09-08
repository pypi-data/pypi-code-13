#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lzma, codecs
class ecrypt(object):
	@staticmethod
	def compr(in_str):
		if in_str is None or len(in_str)<1: return ''
		return codecs.encode( lzma.compress(in_str.encode()), 'base64').decode()
	@staticmethod
	def decompr(in_str):
		if in_str is None or len(in_str)<1: return ''
		return lzma.decompress(codecs.decode( in_str.encode(), 'base64')).decode()
