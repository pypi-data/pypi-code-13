# -*- coding: utf-8 -*-

# Resource object code
#
# Created: dim. juil. 31 17:37:40 2016
#      by: The Resource Compiler for PySide (Qt v4.8.7)
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore

qt_resource_data = "\x00\x00\x01L<svg xmlns=\x22http://www.w3.org/2000/svg\x22 width=\x2224\x22 height=\x2224\x22 viewBox=\x220 0 24 24\x22><path d=\x22M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm4.151 17.943l-4.143-4.102-4.117 4.159-1.833-1.833 4.104-4.157-4.162-4.119 1.833-1.833 4.155 4.102 4.106-4.16 1.849 1.849-4.1 4.141 4.157 4.104-1.849 1.849z\x22/></svg>"
qt_resource_name = "\x00\x06\x07\x03}\xc3\x00i\x00m\x00a\x00g\x00e\x00s\x00\x09\x06\x98\x8e\xa7\x00c\x00l\x00o\x00s\x00e\x00.\x00s\x00v\x00g"
qt_resource_struct = "\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x12\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
