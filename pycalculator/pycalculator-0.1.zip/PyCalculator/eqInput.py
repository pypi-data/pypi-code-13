import sys
import string
from PyQt4 import QtGui, QtCore
from calculator import Calculator

class Eq_Input(QtGui.QTextEdit):
	operators = {ord(x): x for x in '+-*/^'}
	equation_chars = {ord(x) for x in string.digits + '+-*/^.() '}
	equation_chars.update({16777219, 16777234, 16777236})
	normal_chars = {ord(x) for x in string.digits + '.'}
	normal_chars.update({16777219, 16777234, 16777236})

	def __init__(self, *args, **kwargs):
		QtGui.QTextEdit.__init__(self, *args)
		self.allowed_chars = self.normal_chars
		self.calc = Calculator()
		self.clear_input = False
		self.ready_to_calculate = True

	@property
	def mode(self):
		return self._mode

	@mode.setter
	def mode(self, value):
		self.calc.clear()
		if value == 'normal':
			self._mode = value
			self.allowed_chars = self.normal_chars
		elif value == 'equation':
			self._mode = value
			self.allowed_chars = self.equation_chars
		else:
			raise Exception('Mode does not exist!')

	def keyPressEvent(self, event):
		# self.add_to_eq(event.key())

		modifiers = QtGui.QApplication.keyboardModifiers()
		
		if modifiers == QtCore.Qt.ControlModifier and event.key() in (67, 86):
			QtGui.QTextEdit.keyPressEvent(self, event)
		if modifiers == QtCore.Qt.ShiftModifier and event.key() in (16777232, 16777233):
			QtGui.QTextEdit.keyPressEvent(self, event)

		if event.key() in self.allowed_chars:
			if self.clear_input: 
				self.setText('')
				self.clear_input = False
				self.ready_to_calculate = True
			QtGui.QTextEdit.keyPressEvent(self, event)

		self.add_to_eq(event.key())

	def write_to_input(self):
		if str(self.sender().text()) == '00':
			self.setText(self.toPlainText() + '00')
			return

		key = ord(str(self.sender().text()))

		if key in self.allowed_chars:
			if self.clear_input: 
				self.setText('')
				self.clear_input = False
				self.ready_to_calculate = True

			eq = self.toPlainText()
			self.setText(eq + unichr(key))

		self.add_to_eq(key)

	def do_calculation(self, eq):
		num = eq
		try:
			if self.mode == 'normal':
				self.show_result(self.calc.calculate('=', float(num)))
			elif self.mode == 'equation':
				self.show_result(self.calc.calculate_equation(eq))
		except:
			print('Invalid input!')


	def add_to_eq(self, key):
		eq = str(self.toPlainText())
		if eq == '': 
			eq = '0'
			self.setText('0')

		if self.mode == 'normal':
			num = eq

			if not self.ready_to_calculate:
				# if key not in (16777220, 16777221, ord('=')):
				if key in self.operators:
					self.calc.set_operator(unichr(key))
				return

			if key in self.operators:
				self.show_result(self.calc.calculate(unichr(key), float(num)))
			elif key in (16777220, 16777221, ord('=')):
				self.do_calculation(num)

		if self.mode == 'equation':
			if key in (16777220, 16777221, ord('=')):
				self.do_calculation(eq)

	def clear_eq(self):
		self.setText('')
		self.calc.clear()

	def show_result(self, result):
		if self.mode == 'normal':
			self.ready_to_calculate = False
			self.clear_input = True
			self.setText(str(result))
		elif self.mode == 'equation':
			eq = self.toPlainText()
			self.setText(eq + ' = ' + str(result))