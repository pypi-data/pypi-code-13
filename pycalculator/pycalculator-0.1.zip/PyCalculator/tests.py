from calculator import Calculator
from rpn import Rpn
from nose.tools import assert_equal

class RpnTester(object):

	def test_to_postfix(self, eq_list, eq_results):
		for i, eq in enumerate(eq_list):
			assert_equal(Rpn.to_postfix(eq), eq_results[i])
		print 'All tests passed!'


class CalculatorTester(object):

	def test_create_calculator(self):
		c = Calculator()
		assert_equal(isinstance(c, Calculator), True)
		return c

	def test_give_result(self, eq_list, eq_results):
		c = self.test_create_calculator()
		for i, eq in enumerate(eq_list):
			assert_equal(c.calculate_equation(eq), eq_results[i])
		print 'All tests passed!'

eq_list = ['5+(6*2-2)*9+3^(7-1)', '0+2', '-2+7*9+3/2*6 +++-- 12^(+--2)',
 '5+((1+2)*4)-3', '(1+5*(4+3)-(1+2))+((3))', '(-3)^2^2', '-3^2^2', '3^2^2^1+(5+2)*4', '(((1*1+(--2)*3+0)))']

postfix_results = []
eq_results = [824, 2, 214, 14, 36, 81, -81, 109, 7]

rpnT = RpnTester()
# rpnT.test_to_postfix(eq_list, postfix_results)

ct = CalculatorTester()
ct.test_give_result(eq_list, eq_results)