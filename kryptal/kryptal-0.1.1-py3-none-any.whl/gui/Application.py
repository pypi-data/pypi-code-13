from PyQt5.QtWidgets import QApplication
import sys
from kryptal.gui.MainWindow import MainWindow


class Application(QApplication):
    def __init__(self):
        import sys
        super(Application, self).__init__(sys.argv)

    def run(self):
        mainWindow = MainWindow()
        mainWindow.show()
        return self.exec_()
