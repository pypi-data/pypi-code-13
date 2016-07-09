from baseCalculator import BaseCalculator
from rpn import Rpn

class Calculator(BaseCalculator):

	digits = set('0123456789')

	def refactor(self, equation):
		# print equation
		output = ''
		for i, x in enumerate(equation):
			if x in ('-', '+'):
				if i == 0 or (equation[i - 1], equation[i + 1]) == ('(', '(') or (equation[i - 1] == '(' and equation[i + 1] in self.digits):
					output += x + '1*'
				else:
					output += x
			else:
				output += x
		return output

	def find_multiple_ops(self, equation):
		d = dict()
		idx = -1
		j = -1
		for i, x in enumerate(equation):
			if x in ('+', '-'):
				if j == i:
					d[idx].append(x)
					j += 1
				else:
					d[i] = [x]
					idx, j = i, i + 1	
		return d

	def calculate_multiple_ops(self, dict_of_lists):
		for k in dict_of_lists:
			res = '+'
			for op in dict_of_lists[k]:
				if (res, op) == ('+', '-') or (res, op) == ('-', '+'):
					res = '-'
				else:
					res = '+'
			dict_of_lists[k] = res

	def remove_multiple_ops(self, equation):
		output = ''
		equation = equation.replace(' ', '')
		d = self.find_multiple_ops(equation)
		# print d
		self.calculate_multiple_ops(d)
		# print d
		for i, x in enumerate(equation):
			if x not in ('+', '-'):
				output += x
			elif i in d:
				output += d[i]
		return output

	def get_eq_list(self, equation):
		eq = self.remove_multiple_ops(equation)
		eq = self.refactor(eq)
		eq_list, num, idx = [], '', 0
		while idx < len(eq):
			if eq[idx] in ('+', '-', '*', '/', '^', '(', ')'):
				if num:
					eq_list.append(num)
					num = ''
				if eq[idx] in ('+', '-') and (idx == 0 or eq[idx - 1: idx + 3] in ('(-1*', '(+1*')):
					eq_list.append(eq[idx] + '1')
					eq_list.append('*')
					idx += 2
				else:
					eq_list.append(eq[idx])
			else:
				num += eq[idx]
			idx += 1
		if num != '':
			eq_list.append(num)
		return eq_list

	def calculate_rpn(self, rpn_eq):
		stack = []
		ops = ('+', '-', '*', '/', '^')
		for x in rpn_eq:
			if x in ops:
				a = float(stack.pop())
				b = float(stack.pop())
				if x == '+':
					r = a + b
				elif x == '-':
					r = b - a
				elif x == '*':
					r = a * b
				elif x == '/':
					r = b / a
				elif x == '^':
					r = b**a
				stack.append(r)
			else:
				stack.append(x)
		return stack

	def calculate_equation(self, equation):
		try:
			eq_list = self.get_eq_list(equation)
			rpn_list = Rpn.to_postfix(eq_list)
			result = self.calculate_rpn(rpn_list)
			return result[0]
		except:
			raise Exception('Invalid equation')


# s = '(1-1.2)   /  22 +2.222'
# s = '5+(6*2-2)*9-+(-3)^(7+(-1))'
# s = '(1+2)-((0)+-(2+-1)-(-1))'
# s = '((0)+(2+1)-(-1))'
# s = '(2+(0-1))-(1-3)'
# s = '1++--2 - -2.5555'
# s = '-(-(-(1-(--2))))'
# s = '+-+--(1--+-58)+5-1*2'
# s = '1/1/1/1/1/(2'
# s = '(1)-(-----2)'
# s = '-(-(-(-(1+-(-2)^3)))'
# c = Calculator()
# result = c.remove_multiple_ops(s)
# print result
# ref = c.refactor(result)
# print ref
# eq_list =  c.get_eq_list(s)
# print eq_list
# rpn_list = Rpn.to_postfix(eq_list)
# print rpn_list
# print c.calculate_rpn(rpn_list)
# print c.calculate_equation(s)