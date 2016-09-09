from PyQt5.QtWidgets import *
from PyQt5 import uic
from kryptal.pluginmanager.KryptalPlugins import KryptalPlugins
import pkg_resources


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        uipath = pkg_resources.resource_filename(__name__, "mainwindow.ui")
        uic.loadUi(uipath, self)
        plugins = KryptalPlugins()
        for p in plugins.filesystems():
            self.pluginsList.addItem("Filesystem: %s" % p.name())
        for p in plugins.storage_providers():
            self.pluginsList.addItem("StorageProvider: %s" % p.name())
