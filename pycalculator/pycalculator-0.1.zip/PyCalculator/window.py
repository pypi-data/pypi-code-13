import sys
from PyQt4 import QtGui, QtCore
from eqInput import Eq_Input

class CalcWindow(QtGui.QMainWindow):
	gridX = 70
	gridY = 85

	def __init__(self):
		super(CalcWindow, self).__init__()
		self.setGeometry(450, 250, 300, 300)
		self.setFixedSize(300, 300)
		self.setWindowTitle('Calculator')
		self.setWindowIcon(QtGui.QIcon('logo2.png'))

		self.num_buttons = self.set_num_buttons()
		self.operators = self.set_operatos()
		self.eq_input = self.set_equation_input()
		self.set_actions()

		self.modeAction = self.set_mode_action()
		self.set_menu()

	def set_mode_action(self):
		self.eq_input.mode = 'normal'
		modeAction = QtGui.QAction('&Equation mode', self, checkable=True)
		modeAction.setChecked(False)
		modeAction.setShortcut('Ctrl+Q')
		modeAction.setStatusTip('Change the mode of calculator')
		# modeAction.triggered.connect(self.close)
		modeAction.triggered.connect(self.change_mode)
		return modeAction

	def set_menu(self):
		self.statusBar()

		mainMenu = self.menuBar()
		modeMenu = mainMenu.addMenu('&Mode')
		modeMenu.addAction(self.modeAction)	

	# changing mode of calc, in case modes were changed or smth - it should work fine
	def change_mode(self):
		isChecked = self.modeAction.isChecked()
		modes = ('normal', 'equation')
		try:
			self.eq_input.mode = modes[int(isChecked)]
			self.eq_input.setText('0')
		except:
			print 'Error in setting mode of calculator!'
			if isChecked:
				self.modeAction.setChecked(False)
			else:
				self.modeAction.setChecked(True)
		else:
			# if everything goes fine we change the mode and clear the input
			self.eq_input.setText('')

	def set_num_buttons(self):
		buttons = [QtGui.QPushButton(str(i), self) for i in xrange(10) if i != 0]
		buttons.append(QtGui.QPushButton('0', self))
		buttons.append(QtGui.QPushButton('.', self))
		buttons.append(QtGui.QPushButton('00', self))

		for i, b in enumerate(buttons):
			b.move(self.gridX + i % 3 * 35 + 10, self.gridY + i / 3 * 35 + 15)
			b.resize(30,30)
		return buttons

	def set_operatos(self):
		operators = [QtGui.QPushButton(i, self) for i in ('+', '-', '*', '/', '=', 'Clear')]
		for i, op in enumerate(operators[:len(operators) - 2]):
				op.move(self.gridX + 115, self.gridY + i * 35 + 15)
				op.resize(30,30)
		operators[-2].move(self.gridX + 80, self.gridY + 155)
		operators[-1].move(self.gridX + 10, self.gridY + 155)
		operators[-2].resize(65,30)
		operators[-1].resize(65,30)
		return operators

	def set_equation_input(self):
		eq_input = Eq_Input(self)
		eq_input.resize(250, 40)
		eq_input.move(25, 30)
		eq_input.setLineWrapMode(QtGui.QTextEdit.NoWrap)
		return eq_input

	def set_actions(self):
		for b in self.num_buttons + self.operators[:len(self.operators) - 1]:
			b.clicked.connect(self.eq_input.write_to_input)
		self.operators[-1].clicked.connect(self.eq_input.clear_eq)
		# self.operators[-2].clicked.connect(self.eq_input.show_result)

	def closeEvent(self, event):
		choice = QtGui.QMessageBox.question(self, 'Extract!', 'Are you quiting this wonderful app?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

		if choice == QtGui.QMessageBox.Yes:
			event.accept()
		elif choice == QtGui.QMessageBox.No:
			event.ignore()

def main():
	app = QtGui.QApplication(sys.argv)
	w = CalcWindow()
	w.show()
	app.exec_()

if __name__ == '__main__':
	main()