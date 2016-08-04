
# -*- coding: utf-8 -*-

""" 數值儲存用類別 / Value container classes """

from collections import namedtuple

class CountDownValuePopper(object):
	def __init__(self, initial_count, initial_pop, *pop_rules, **kwds):
		"""
		依據已取值次數回傳不同的數值

		Return different value according to number of pops

		Args:
			initial_count: 初始的計數值 / Initial count number
			initial_pop: 最一開始的回傳值 / Initial popped value
			*pop_rules: 以 (bound, pop_value,) 型式 tuple 構成的各計數起對應的回傳值 / Pop rule formed by tuple in (bound, pop_value,) format
		"""
		super(CountDownValuePopper, self).__init__(**kwds)
		self.c = initial_count
		self.base_pop = initial_pop
		self.pop_rules = pop_rules
	# ### def __init__

	def pop(self):
		prev_c = self.c
		self.c = prev_c - 1
		result = self.base_pop
		for bound_value, result_pop, in self.pop_rules:
			if prev_c > bound_value:
				return result
			result = result_pop
		return result
	# ### def pop

	def __call__(self, *args, **kwds):
		return self.pop()
	# ### def __call__
# ### class CountDownValuePopper

ContentListEntity = namedtuple("ContentListEntity", ("content_key", "content_list",))

class OrderedKeyContentList(object):
	""" 有順序的有鍵的值所構成的串列 / List of content with key """

	def __init__(self, *args, **kwds):
		super(OrderedKeyContentList, self).__init__(*args, **kwds)
		self.l = []
		self.m = {}
	# ### def __init__

	def add(self, k, content):
		"""
		增加給定的鍵值組

		Add given key-value pair. If given key does not existed in this container a list container will be created for keeping given value.

		Args:
			k: 給定值所屬的鍵 / Key value of given content
			content: 給定值 / Value of given content
		"""
		if k not in self.m:
			aux = ContentListEntity(k, list())
			self.l.append(aux)
			self.m[k] = aux
		self.m[k].content_list.append(content)
	# ### def add

	def __iter__(self):
		return iter(self.l)
	# ### def __iter__
# ### class OrderedKeyContentList



# vim: ts=4 sw=4 ai nowrap
