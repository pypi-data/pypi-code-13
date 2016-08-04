
# -*- coding: utf-8 -*-

""" 算式處理函式庫 / Formula processing functions """

import re
import collections
import logging
_log = logging.getLogger(__name__)


class BaseOperator(object):
	""" 表現運算子的基底物件 / Base class of operator """

	def __init__(self, *args, **kwds):
		super(BaseOperator, self).__init__(*args, **kwds)
	# ### def __init__
	def get_priority(self):
		"""
		取得運算子的優先順序，愈高的優先順序應傳回愈大的值

		Get the priority of operator. Bigger value means higher priority.

		Returns:
			運算子的優先權 / Priority of operator
		"""
		return -1
	# ### def get_priority
	def is_left_associative(self):
		"""
		運算子是否為左結合

		Return a boolean value to indicate associative of operator.

		Returns:
			傳回 True 時表示運算子為左結合，否則為右結合 / Return True for left-associative operator; False for right-associative operator
		"""
		return True
	# ### def is_left_associative
	def get_operand_count(self):
		"""
		取得運算元的數量

		Get the number of operand

		Return:
			運算元的數量 / Number of operand(s)
		"""
		raise NotImplementedError("not implemented get_operand_count() yet")
	# ### def get_operand_count
	def evaluate(self, *args):
		"""
		進行運算，參數數量為 get_operand_count() 方法所傳回的數值

		Perform the computation. The number of parameter will be the value returned by get_operand_count() method.

		Returns:
			運算結果 / Result of evaluation
		"""
		raise NotImplementedError("not implemented evaluate() yet")
	# ### def evaluate
# ### class BaseOperator

class BaseFunction(object):
	""" 表現函數的基底物件 / Base class of function """

	def __init__(self, *args, **kwds):
		super(BaseFunction, self).__init__(*args, **kwds)
	# ### def __init__
	def get_argument_count(self):
		"""
		取得參數的數量

		Get the number of arguments

		Return:
			參數的數量 / Number of arguments
		"""
		raise NotImplementedError("not implemented get_argument_count() yet")
	# ### def get_argument_count
	def evaluate(self, *args):
		"""
		進行運算，參數數量為 get_argument_count() 方法所傳回的數值

		Perform the computation. The number of parameter will be the value returned by get_argument_count() method.

		Returns:
			運算結果 / Result of evaluation
		"""
		raise NotImplementedError("not implemented evaluate() yet")
	# ### def evaluate
# ### class BaseFunction

class ParenthesisL(object):
	""" 表現左括弧的物件 / Class of left parenthesis """

	def __init__(self, v=None, *args, **kwds):
		super(ParenthesisL, self).__init__(*args, **kwds)
	# ### def __init__
# ### class ParenthesisL

class ParenthesisR(object):
	""" 表現右括弧的物件 / Class of right parenthesis """

	def __init__(self, v=None, *args, **kwds):
		super(ParenthesisR, self).__init__(*args, **kwds)
	# ### def __init__
# ### class ParenthesisR

class ArgumentSeparator(object):
	""" 表現參數分隔字元的物件 / Class of argument separator token """

	def __init__(self, v=None, *args, **kwds):
		super(ArgumentSeparator, self).__init__(*args, **kwds)
	# ### def __init__
# ### class ArgumentSeparator



class Plus(BaseOperator):
	def __init__(self, v=None, *args, **kwds):
		super(Plus, self).__init__(*args, **kwds)
	# ### def __init__
	def get_priority(self):
		return 2
	# ### def get_priority
	def get_operand_count(self):
		return 2
	# ### def get_operand_count
	def evaluate(self, a, b, *args):
		return (a + b)
	# ### def evaluate
# ### class Plus

class Minus(BaseOperator):
	def __init__(self, v=None, *args, **kwds):
		super(Minus, self).__init__(*args, **kwds)
	# ### def __init__
	def get_priority(self):
		return 2
	# ### def get_priority
	def get_operand_count(self):
		return 2
	# ### def get_operand_count
	def evaluate(self, a, b, *args):
		return (a - b)
	# ### def evaluate
# ### class Minus

class Multiply(BaseOperator):
	def __init__(self, v=None, *args, **kwds):
		super(Multiply, self).__init__(*args, **kwds)
	# ### def __init__
	def get_priority(self):
		return 3
	# ### def get_priority
	def get_operand_count(self):
		return 2
	# ### def get_operand_count
	def evaluate(self, a, b, *args):
		return (a * b)
	# ### def evaluate
# ### class Multiply

class Divide(BaseOperator):
	def __init__(self, v=None, *args, **kwds):
		super(Divide, self).__init__(*args, **kwds)
	# ### def __init__
	def get_priority(self):
		return 3
	# ### def get_priority
	def get_operand_count(self):
		return 2
	# ### def get_operand_count
	def evaluate(self, a, b, *args):
		return (a / b)
	# ### def evaluate
# ### class Divide

def math_operator(v):
	if "+" == v:
		return Plus()
	if "-" == v:
		return Minus()
	if "*" == v:
		return Multiply()
	if "/" == v:
		return Divide()
	return None
# ### def math_operator



RegexParsePlan = collections.namedtuple("RegexParsePlan", ("regex_object", "element_mapper",))


LITERAL_MATH = RegexParsePlan(re.compile("([0-9]+)|([\\*\\/+-])|(\\()|(\\))|\s+"),
						(None, int, math_operator, ParenthesisL, ParenthesisR,))

def parse_token_w_regex(v, parse_plan):
	"""
	將給定的陳述式進行句元分割並轉換為後波蘭表示式

	Split given statement into tokens and transform into reverse polish (postfix) notation form

	Args:
		v: 要解析的陳述式字串
		parse_plan: 解析規則 (RegexParsePlan 物件)

	Returns:
		轉換為後波蘭表示式的句元所構成的串列 / Resulted token list in reverse polish notation
	"""
	s_pos = 0
	l = len(parse_plan.element_mapper)
	q = []
	result = []
	for m in parse_plan.regex_object.finditer(v):
		m_s, m_e, = m.span()
		if m_s != s_pos:
			raise ValueError("unknown token for %r, location %r ~ %r" % (v, s_pos, m_s,))
		s_pos = m_e
		for i in xrange(1, l):
			e = m.group(i)
			g = parse_plan.element_mapper[i]
			if e is not None:
				if g is not None:
					node = g(e)
					# https://en.wikipedia.org/wiki/Shunting-yard_algorithm
					if isinstance(node, BaseOperator):
						try:
							aux = q.pop()
							n_left_assoc = node.is_left_associative()
							n_priority = node.get_priority()
							while isinstance(aux, BaseOperator) and (
									(n_left_assoc and (aux.get_priority() >= n_priority))
									or ((not n_left_assoc) and (aux.get_priority() > n_priority))
									):
								result.append(aux)
								aux = q.pop()
							q.append(aux)
						except IndexError:
							pass
						q.append(node)
					elif isinstance(node, BaseFunction):
						q.append(node)
					elif isinstance(node, ParenthesisL):
						q.append(node)
					elif isinstance(node, ParenthesisR):
						try:
							aux = q.pop()
							while not isinstance(aux, ParenthesisL):
								result.append(aux)
								aux = q.pop()
						except IndexError:
							pass
					elif isinstance(node, ArgumentSeparator):
						try:
							aux = q.pop()
							while not isinstance(aux, ParenthesisL):
								result.append(aux)
								aux = q.pop()
							q.append(aux)
						except IndexError:
							raise ValueError("caught argument separator without parenthesis")
					else:
						result.append(node)
				break
	try:
		aux = q.pop()
		while isinstance(aux, (BaseOperator, BaseFunction,)):
			result.append(aux)
			aux = q.pop()
	except IndexError:
		pass
	return result
# ### def parse_token_w_regex

def parse_literal_math(v):
	"""
	將給定的數學算式陳述式進行句元分割並轉換為後波蘭表示式

	Convert given math formula to reverse polish notation

	Args:
		v: 要解析的算式字串 / String to be parse

	Returns:
		轉換為後波蘭表示式的句元所構成的串列 / Resulted token list in reverse polish notation
	"""
	return parse_token_w_regex(v, LITERAL_MATH)
# ### def parse_literal_math



def _pop_arguments(d, c):
	""" (internal) 由串列 d 尾端取出 c 個元素
	"""
	a = [d.pop() for _i in xrange(c)]
	a.reverse()
	return a
# ### def _pop_arguments

def evaluate(fm):
	"""
	計算由 parse_*() 函數所解析出的算式結果

	Evaluate the result of parse_*() function.

	Args:
		fm: 透過 parse_*() 函數所解析出的算式 / Formula object generated by parse_*() function

	Returns:
		計算結果 / Result of evaluation
	"""
	d = []
	for e in fm:
		if isinstance(e, BaseOperator):
			a = _pop_arguments(d, e.get_operand_count())
			r = e.evaluate(*a)
			d.append(r)
		elif isinstance(e, BaseFunction):
			a = _pop_arguments(d, e.get_argument_count())
			r = e.evaluate(*a)
			d.append(r)
		else:
			d.append(e)
	if len(d) > 1:
		_log.warning("there are more than 1 values in operand queue: %r", len(d))
	return d.pop()
# ### def evaluate



# vim: ts=4 sw=4 ai nowrap
