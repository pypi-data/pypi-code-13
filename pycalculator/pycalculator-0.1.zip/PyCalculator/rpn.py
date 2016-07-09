class Rpn(object):

	"Converts equation into postfix/reverse polish notation"

	d = {'+': 0, '-': 0, '*':1, '/':1, '^':2, '(':3, ')':3}

	@classmethod
	def to_postfix(cls, eq):
		output = []
		stack = []
		for x in eq:
			if x in cls.d:
				cls.test(x, stack, output)
			else:
				output.append(x)
		while len(stack) != 0:
			output.append(stack.pop())
		return [x for x in output if x not in ('(', ')', ' ')]

	@classmethod
	def test(cls, x, stack, output):
		if len(stack) == 0 or stack[-1] == '(':
			stack.append(x)
		elif x == '(':
			stack.append(x)
		elif x == ')':
			op = stack.pop()
			while op != '(':
				output.append(op)
				op = stack.pop()
		elif cls.d[x] > cls.d[stack[-1]]:
			stack.append(x)
		elif cls.d[x] == cls.d[stack[-1]]:
			if x in ('+', '-', '*', '/'):
				output.append(stack.pop())
				stack.append(x)
			elif x == '^':
				stack.append(x)
		elif cls.d[x] < cls.d[stack[-1]]:
			op = stack.pop()
			output.append(op)
			cls.test(x, stack, output)


# eq = '5+(6*2-2)*9+3^(7-1)'
# eq = '((((1+2)))'
# eq = '1- -5'
# print Rpn.to_postfix(eq)