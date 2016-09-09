from PyQt5.QtWidgets import *
from PyQt5 import uic
from kryptal.pluginmanager.KryptalPlugins import KryptalPlugins
from kryptal.utils import Paths
import os


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        uic.loadUi(os.path.join(Paths.exe_path(), 'gui/mainwindow.ui'), self)
        plugins = KryptalPlugins()
        for p in plugins.filesystems():
            self.pluginsList.addItem("Filesystem: %s" % p.name())
        for p in plugins.storage_providers():
            self.pluginsList.addItem("StorageProvider: %s" % p.name())
