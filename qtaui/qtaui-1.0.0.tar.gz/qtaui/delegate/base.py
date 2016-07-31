#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /delegate.py
#  NAME
#    delegate --
#  COPYRIGHT
#
#  Copyright (C) 2016 Jérôme Laheurte <fraca7@free.fr>
#
# This library  is free software; you can  redistribute it and/or
# modify  it under  the terms  of the  GNU Lesser  General Public
# License as  published by  the Free Software  Foundation; either
# version  2.1 of  the License,  or  (at your  option) any  later
# version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY;  without even the implied warranty of
# MERCHANTABILITY or  FITNESS FOR A PARTICULAR  PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You  should have  received a  copy  of the  GNU Lesser  General
# Public License  along with this  library; if not, write  to the
# Free  Software Foundation,  Inc., 59  Temple Place,  Suite 330,
# Boston, MA 02111-1307 USA
#
#  CREATION DATE
#    14 Jul 2016
#***


from PySide import QtCore, QtGui
from qtaui.utils import QAUILoggingMixin


class QAUIPos(object): # pylint: disable=R0903
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    CENTER = 4
    FLOATING = 5


class QAUIDelegate(QAUILoggingMixin, QtCore.QObject):
    def __init__(self, frameChildren):
        self._mouseState = 0
        self._frameChildren = frameChildren
        self._frame = None
        self._mouseClickOrigin = None
        super(QAUIDelegate, self).__init__()

    def attach(self, frame):
        self._frame = frame
        for child in self._frameChildren:
            child.setParent(frame)
            child.setFrameParent(frame)
            child.show()

    def detach(self):
        for child in self._frameChildren:
            child.hide()
            child.setParent(None)
            child.setFrameParent(None)
        self._frame = None

    def saveState(self):
        raise NotImplementedError

    def replace(self, oldFrame, newFrame):
        index = self._frameChildren.index(oldFrame)
        self._frameChildren[index] = newFrame
        newFrame.setParent(self._frame)
        newFrame.setFrameParent(self._frame)
        newFrame.show()

    def frame(self):
        return self._frame

    def title(self):
        from qtaui.frame import QAUILeafFrame
        return self._frame._title if isinstance(self._frame, QAUILeafFrame) else ''

    def addChild(self, child):
        child.setParent(self.frame())
        child.setFrameParent(self.frame())
        child.show()
        child.setFocus(QtCore.Qt.OtherFocusReason)

    def childRemoved(self, child):
        self._frameChildren.remove(child)
        child.setParent(None)
        child.setFrameParent(None)
        if len(self._frameChildren) == 1:
            self._frame.frameParent()._delegate.replace(self._frame, self._frameChildren[0])
            self._frame.deleteLater()

    def resized(self):
        for child in self._frameChildren:
            child._delegate.resized()

    def paint(self, event):
        pass

    def startDrag(self, pos):
        parent = self._frame.frameParent()
        if parent is not None:
            parent.removeChild(self._frame)
            self._frame.move(QtGui.QCursor.pos() - pos)
            self._frame.setWindowOpacity(0.5)
            self._frame.show()
            self._frame.undocked.emit()
            parent.titleChanged.emit()

    def titlePress(self, event):
        self._mouseClickOrigin = event.pos()
        self._mouseState = 1

    def titleMove(self, event):
        if self._mouseState == 1:
            if (event.pos() - self._mouseClickOrigin).manhattanLength() >= \
                   QtGui.QApplication.startDragDistance():
                self._mouseState = 2
                self.startDrag(event.pos())
                self._frame._manager.startShowDropView()
                self._frame.grabMouse()
                self._frame.setFocus(QtCore.Qt.ActiveWindowFocusReason)
                if self._frame.parent() is None:
                    self._frame.setWindowOpacity(0.5)

    def titleRelease(self, event):
        self._mouseState = 0

    def mousePress(self, event):
        pass

    def mouseMove(self, event):
        if self._mouseState == 2:
            self._frame.move(QtGui.QCursor.pos() - self._mouseClickOrigin)
            self._frame._manager.notifyFrameMove(self._frame.mapToGlobal(event.pos()))

    def mouseRelease(self, event):
        if self._mouseState == 2:
            self._frame.releaseMouse()
            self._frame.setWindowOpacity(1.0)
            self._frame._manager.stopShowDropView(self._frame)
        self._mouseState = 0
