import abc, operator

class BaseCalculator(object):
	__metaclass__ = abc.ABCMeta

	ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.div, '^': operator.pow}

	@abc.abstractmethod
	def calculate_equation(self):
		"Calculate the result"

	def __init__(self):
		self.operators, self.res = [], None

	def set_operator(self, key):
		if key in self.ops:
			if len(self.operators) == 0:
				self.operators.append(key)
			self.operators[0] = key

	def clear(self):
		self.operators, self.res = [], None

	def calculate(self, op, num):
		if op != '=':
			self.operators = [op] + self.operators

		if self.res is None or self.operators == []:
			self.res = num
		else:
			self.res = self.ops[self.operators.pop()](self.res, num)
		return self.res