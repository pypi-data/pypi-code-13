import operator

ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.div, '^': operator.pow}
def calc(eq):
	l = eq.split()
	return ops[l[0]](float(l[1]), float(l[2]))


print calc('* 1.005 2')