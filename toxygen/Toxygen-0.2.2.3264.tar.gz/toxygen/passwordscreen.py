from widgets import CenteredWidget, LineEdit
try:
    from PySide import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui


class PasswordArea(LineEdit):

    def __init__(self, parent):
        super(PasswordArea, self).__init__(parent)
        self.parent = parent
        self.setEchoMode(QtGui.QLineEdit.EchoMode.Password)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.parent.button_click()
        else:
            super(PasswordArea, self).keyPressEvent(event)


class PasswordScreenBase(CenteredWidget):

    def __init__(self, encrypt):
        super(PasswordScreenBase, self).__init__()
        self._encrypt = encrypt
        self.initUI()

    def initUI(self):
        self.resize(360, 170)
        self.setMinimumSize(QtCore.QSize(360, 170))
        self.setMaximumSize(QtCore.QSize(360, 170))

        self.enter_pass = QtGui.QLabel(self)
        self.enter_pass.setGeometry(QtCore.QRect(30, 10, 300, 30))

        self.password = PasswordArea(self)
        self.password.setGeometry(QtCore.QRect(30, 50, 300, 30))

        self.button = QtGui.QPushButton(self)
        self.button.setGeometry(QtCore.QRect(30, 90, 300, 30))
        self.button.setText('OK')
        self.button.clicked.connect(self.button_click)

        self.warning = QtGui.QLabel(self)
        self.warning.setGeometry(QtCore.QRect(30, 130, 300, 30))
        self.warning.setStyleSheet('QLabel { color: #F70D1A; }')
        self.warning.setVisible(False)

        self.retranslateUi()
        self.center()
        QtCore.QMetaObject.connectSlotsByName(self)

    def button_click(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            self.button_click()
        else:
            super(PasswordScreenBase, self).keyPressEvent(event)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("pass", "Enter password", None, QtGui.QApplication.UnicodeUTF8))
        self.enter_pass.setText(QtGui.QApplication.translate("pass", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.warning.setText(QtGui.QApplication.translate("pass", "Incorrect password", None, QtGui.QApplication.UnicodeUTF8))


class PasswordScreen(PasswordScreenBase):

    def __init__(self, encrypt, data):
        super(PasswordScreen, self).__init__(encrypt)
        self._data = data

    def button_click(self):
        if self.password.text():
            try:
                self._encrypt.set_password(self.password.text())
                new_data = self._encrypt.pass_decrypt(self._data[0])
            except Exception as ex:
                self.warning.setVisible(True)
                print('Decryption error:', ex)
            else:
                self._data[0] = new_data
                self.close()


class UnlockAppScreen(PasswordScreenBase):

    def __init__(self, encrypt, callback):
        super(UnlockAppScreen, self).__init__(encrypt)
        self._callback = callback
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def button_click(self):
        if self.password.text():
            if self._encrypt.is_password(self.password.text()):
                self._callback()
                self.close()
            else:
                self.warning.setVisible(True)
                print('Wrong password!')
