
# -*- coding: utf-8 -*-

""" Testing for convert module """


import unittest

from commonutil import convert



class Test_ToText(unittest.TestCase):
	def test_normal_string_1(self):
		r = convert.to_text("normal string")
		self.assertEqual(r, "normal string")
	# ### def test_normal_string_1

	def test_normal_string_2(self):
		r = convert.to_text("   normal string")
		self.assertEqual(r, "normal string")
	# ### def test_normal_string_2

	def test_normal_string_3(self):
		r = convert.to_text("normal string   ")
		self.assertEqual(r, "normal string")
	# ### def test_normal_string_3

	def test_empty_string_1(self):
		r = convert.to_text("")
		self.assertIsNone(r)
	# ### def test_empty_string_1

	def test_empty_string_2(self):
		r = convert.to_text(None)
		self.assertIsNone(r)
	# ### def test_empty_string_2

	def test_empty_string_3(self):
		r = convert.to_text(None, "-")
		self.assertEqual(r, "-")
	# ### def test_empty_string_3
# ### class Test_ToText



if __name__ == '__main__':
	unittest.main()
# vim: ts=4 sw=4 ai nowrap
