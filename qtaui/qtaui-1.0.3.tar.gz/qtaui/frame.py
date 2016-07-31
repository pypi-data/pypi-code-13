#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /qtaui.py
#  NAME
#    qtaui -- AUI for PySide/PyQt
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
#    31 Jan 2016
#***

import cPickle
from PySide import QtCore, QtGui

from .utils import QAUILoggingMixin
from .delegate import QAUIPos
from .delegate.base import QAUIDelegate
from .delegate.noop import QAUINoopDelegate
from .delegate.leaf import QAUILeafDelegate
from .delegate.splitter import QAUISplitterDelegate
from .delegate.tab import QAUITabDelegate
from .dropview import QAUIDropView


class QAUITitleBar(QAUILoggingMixin, QtGui.QWidget):
    margin = 2

    def __init__(self, frame):
        self._frame = frame
        super(QAUITitleBar, self).__init__()

        font = frame.font()
        font.setPointSizeF(font.pointSizeF() * 0.8)
        self.setFont(font)

        metrics = QtGui.QFontMetrics(font)
        self._dim = metrics.height() + 2 * self.margin
        self.setFixedHeight(self._dim)

        self._btn = QtGui.QPushButton(self)
        self._btn.setIcon(QtGui.QIcon(':images/close.svg'))
        self._btn.setFixedSize(QtCore.QSize(self._dim, self._dim))
        self._btn.setFlat(True)
        self._btn.clicked.connect(self._closeClicked)

        frame.titleChanged.connect(self.update)
        frame.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def resizeEvent(self, event):
        self._btn.move(self.width() - self._dim, 0)
        event.ignore()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        grad = QtGui.QLinearGradient(0, 0, self.width(), self.height())
        color = QtGui.QColor(QtCore.Qt.blue if self._frame.hasFocus() else QtCore.Qt.gray)
        grad.setColorAt(0.0, color)
        grad.setColorAt(1.0, color.lighter(150))
        painter.fillRect(self.rect(), QtGui.QBrush(grad))

        metrics = QtGui.QFontMetrics(self.font())
        available = self.width() - 3 * self.margin - self._dim
        text = metrics.elidedText(self._frame.title(), QtCore.Qt.ElideMiddle, available)
        painter.setPen(QtCore.Qt.white if self._frame.hasFocus() else QtCore.Qt.black)
        painter.drawText(self.margin, self.margin + metrics.ascent(), text)

    def _closeClicked(self):
        if self._frame.frameParent() is None:
            self._frame.close()
        else:
            self._frame.frameParent().removeChild(self._frame)
            self._frame.notifyClose()
        self._frame.closed.emit()
        self._frame.deleteLater()

    def mousePressEvent(self, event):
        self._frame.setFocus(QtCore.Qt.MouseFocusReason)
        self._frame._delegate.titlePress(event)

    def mouseMoveEvent(self, event):
        self._frame._delegate.titleMove(event)

    def mouseReleaseEvent(self, event):
        self._frame._delegate.titleRelease(event)


class QAUIFrame(QAUILoggingMixin, QtGui.QWidget):
    titleChanged = QtCore.Signal()
    undocked = QtCore.Signal()
    docked = QtCore.Signal(QtGui.QWidget, int)
    closed = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        self._manager = kwargs.pop('manager', None)
        super(QAUIFrame, self).__init__(*args, **kwargs)

        if self._manager is None:
            parent = self.parent()
            while parent is not None and not isinstance(parent, QAUIManager):
                parent = parent.parent()
            if parent is not None:
                self._manager = parent

        if self._manager is None:
            raise RuntimeError('QAUIFrame without manager')

        self._frameParent = None
        self.setFrameParent(self.parent())

        self._delegate = None
        self.setDelegate(QAUINoopDelegate([]))
        if self.frameParent() is None:
            self.show()

    def saveState(self):
        return self._delegate.saveState()

    def frameParent(self):
        return self._frameParent

    def setFrameParent(self, parent):
        if self._frameParent is not None:
            self._frameParent.titleChanged.emit()
            self.titleChanged.disconnect(self._frameParent.titleChanged)
        self._frameParent = parent
        if self._frameParent is not None:
            self.titleChanged.connect(self._frameParent.titleChanged)
            self._frameParent.titleChanged.emit()

    def title(self):
        return self._delegate.title()

    def setDelegate(self, delegate):
        if self._delegate is not None:
            self._delegate.detach()
        self._delegate = delegate
        self._delegate.attach(self)
        self.titleChanged.emit()

    def addFrame(self, frame, position=QAUIPos.CENTER):
        self._delegate.addChild(frame, position)
        return frame

    def notifyClose(self):
        if self._delegate is not None:
            for child in self._delegate._frameChildren:
                child.notifyClose()

    def removeChild(self, frame):
        frame.hide()
        self._delegate.childRemoved(frame)

    def resizeEvent(self, event):
        super(QAUIFrame, self).resizeEvent(event)
        self._delegate.resized()

    def paintEvent(self, event):
        super(QAUIFrame, self).paintEvent(event)
        self._delegate.paint(event)

    def mousePressEvent(self, event):
        self._delegate.mousePress(event)

    def mouseMoveEvent(self, event):
        self._delegate.mouseMove(event)

    def mouseReleaseEvent(self, event):
        self._delegate.mouseRelease(event)

    def dump(self, indent=0):
        self.d('DUMP %s%s (%s)', '  ' * indent, self, self._delegate)
        for child in self._delegate._frameChildren:
            child.dump(indent + 1)


class QAUILeafFrame(QAUIFrame):
    def __init__(self, *args, **kwargs):
        self._title = kwargs.pop('title', 'Untitled')
        super(QAUILeafFrame, self).__init__(*args, **kwargs)
        self.setDelegate(QAUILeafDelegate())

        self._titleBar = QAUITitleBar(self)
        self._layout = QtGui.QVBoxLayout()
        self._layout.addWidget(self._titleBar)
        self._layout.addStretch(1)
        self._sizeGrip = QtGui.QSizeGrip(self)
        hlayout = QtGui.QHBoxLayout()
        hlayout.addStretch(1)
        hlayout.addWidget(self._sizeGrip)
        self._layout.addLayout(hlayout)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        super(QAUILeafFrame, self).setLayout(self._layout)
        if self.frameParent() is not None:
            self._sizeGrip.hide()
        self._manager.registerFrame(self)

    def saveState(self):
        return {'type': 'leaf', 'id': self._manager.frameId(self)}

    def closeEvent(self, event):
        self.notifyClose()
        event.ignore()

    def notifyClose(self):
        self._manager.unregisterFrame(self)

    def layout(self):
        return self._layout.itemAt(1).layout()

    def setLayout(self, layout):
        self._layout.takeAt(1)
        self._layout.insertLayout(1, QtGui.QVBoxLayout() if layout is None else layout)

    def setParent(self, parent):
        super(QAUILeafFrame, self).setParent(parent)
        self._sizeGrip.setVisible(parent is None)


class QAUIStackedDelegate(QAUINoopDelegate):
    def __init__(self, frameChildren):
        super(QAUIStackedDelegate, self).__init__(frameChildren)
        self._layout = None
        self._dropView = None

    def attach(self, frame):
        super(QAUIStackedDelegate, self).attach(frame)
        self._layout = QtGui.QStackedLayout()
        self._dropView = QAUIDropView(manager=frame)
        self._dropView.finished.connect(self._dropViewStopped)
        self._layout.addWidget(self._dropView)
        self._layout.addWidget(self._frameChildren[0])
        frame.setLayout(self._layout)
        self._layout.setCurrentIndex(1)

    def addChild(self, child): # pylint: disable=W0221
        self._frameChildren[0].addFrame(child)

    def childRemoved(self, child):
        super(QAUIStackedDelegate, self).childRemoved(child)
        self._frameChildren = [QAUIFrame(self._frame)]
        QAUIDelegate.addChild(self, self._frameChildren[0])

    def saveState(self):
        if self._frameChildren:
            return {'main': self._frameChildren[0].saveState()}
        return dict()

    def start(self):
        self._dropView.start()
        self._layout.setCurrentIndex(0)

    def stop(self, frame):
        self._dropView.stop(frame)

    def notifyFrameMove(self, pos):
        self._dropView.notifyFrameMove(pos)

    def _dropViewStopped(self):
        self._layout.setCurrentIndex(1)

    def replace(self, oldFrame, newFrame):
        super(QAUIStackedDelegate, self).replace(oldFrame, newFrame)

        self._layout.removeWidget(oldFrame)
        self._layout.addWidget(newFrame)
        self._layout.setCurrentIndex(1)


class QAUIManager(QAUIFrame):
    frameUndocked = QtCore.Signal(QAUILeafFrame)
    frameDocked = QtCore.Signal(QAUILeafFrame, QAUIFrame, int)
    frameClosed = QtCore.Signal(QAUILeafFrame)

    def __init__(self, *args, **kwargs):
        kwargs['manager'] = self
        super(QAUIManager, self).__init__(*args, **kwargs)
        self.setDelegate(QAUIStackedDelegate([QAUIFrame(self)]))
        self._managedFrames = list()

    @staticmethod
    def labelForTabs():
        return u'Tabs ({title})'

    @staticmethod
    def labelForSplitter(orientation):
        return u'Horizontal splitter' if orientation == QtCore.Qt.Horizontal \
               else u'Vertical splitter'

    def saveState(self):
        state = super(QAUIManager, self).saveState()
        undocked = state['undocked'] = dict()
        for frame in self._managedFrames:
            if frame.parent() is None:
                undocked[self.frameId(frame)] = frame.saveGeometry()
        return QtCore.QByteArray(cPickle.dumps(state))

    def shutdown(self):
        for frame in self._managedFrames:
            if frame.parent() is None:
                frame.hide()

    def restoreState(self, state):
        state = cPickle.loads(str(state))

        # Undock all
        for frame in self._managedFrames:
            if frame.parent() is not None:
                frame.parent().removeChild(frame)

        restored = set()

        # Follow the trail. First undocked frames.
        for id_, frameGeometry in state['undocked'].items():
            # XXXFIXME there's a focus problem here
            frame = self.frameById(id_)
            frame.restoreGeometry(frameGeometry)
            frame.show()
            restored.add(id_)

        if 'main' in state:
            self._restoreState(self._delegate, state['main'], restored)

        # Frames that may have been added since the state save are restored undocked.
        desktop = QtCore.QCoreApplication.instance().desktop().availableGeometry(self)
        for frame in self._managedFrames:
            if self.frameId(frame) not in restored:
                rect = frame.geometry()
                rect.moveCenter(desktop.center())
                frame.setGeometry(rect)
                frame.show()

        self._delegate.resized()

    def _restoreState(self, delegate, state, restored):
        if state['type'] == 'leaf':
            delegate.addChild(self.frameById(state['id']))
            restored.add(state['id'])
        elif state['type'] == 'splitter':
            frame = QAUIFrame(self, manager=self)
            frame.setDelegate(QAUISplitterDelegate([], QtCore.Qt.Horizontal \
                                    if state['orientation'] == 0 else QtCore.Qt.Vertical))
            for childState in state['children']:
                self._restoreState(frame._delegate, childState, restored)
            frame._delegate.setRatios(state['ratios'])
            delegate.addChild(frame)
        elif state['type'] == 'tab':
            frame = QAUIFrame(self, manager=self)
            frame.setDelegate(QAUITabDelegate([]))
            for childState in state['children']:
                self._restoreState(frame._delegate, childState, restored)
            frame._delegate.setCurrent(state['current'])
            delegate.addChild(frame)

    def registerFrame(self, frame):
        if frame.objectName() != '':
            for other in self._managedFrames:
                if other.objectName() == frame.objectName():
                    raise RuntimeError('Duplicate frame ID "%s"' % frame.objectName())
        self._managedFrames.append(frame)
        def forwardUndock():
            self.frameUndocked.emit(frame)
        frame.undocked.connect(forwardUndock)
        def forwardDock(parent, position):
            self.frameDocked.emit(frame, parent, position)
        frame.docked.connect(forwardDock)
        def forwardClose():
            self.frameClosed.emit(frame)
        frame.closed.connect(forwardClose)

    def unregisterFrame(self, frame):
        self._managedFrames.remove(frame)

    def frameId(self, frame):
        if frame.objectName() != '':
            return frame.objectName()
        return self._managedFrames.index(frame)

    def frameById(self, id_):
        if isinstance(id_, int):
            return self._managedFrames[id_]
        for frame in self._managedFrames:
            if frame.objectName() == id_:
                return frame
        raise RuntimeError('No such frame "%s"' % id_)

    def startShowDropView(self):
        self._delegate.start()

    def stopShowDropView(self, frame):
        self._delegate.stop(frame)

    def notifyFrameMove(self, pos):
        self._delegate.notifyFrameMove(pos)

    def topFrame(self):
        return self._delegate._frameChildren[0] if self._delegate._frameChildren else None

    def addFrame(self, frame, position=QAUIPos.CENTER):
        if position == QAUIPos.FLOATING:
            frame.show()
        else:
            self._delegate._frameChildren[0].addFrame(frame, position=position)
        return frame

    def setFrameParent(self, parent):
        self._frameParent = parent # Don't connect
