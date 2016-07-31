#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /splitter.py
#  NAME
#    splitter --
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

import six
import math
import platform

from PySide import QtCore, QtGui

from qtaui.utils import QAUILoggingMixin
from .base import QAUIDelegate, QAUIPos


class _Handle(QAUILoggingMixin, QtGui.QWidget):
    def __init__(self, delegate):
        super(_Handle, self).__init__(delegate.frame())
        self._delegate = delegate
        self._shouldBeVisible = True
        if delegate.orientation() == QtCore.Qt.Horizontal:
            self.setFixedWidth(delegate.handleSize)
            self.setCursor(QtCore.Qt.SizeHorCursor)
        else:
            self.setFixedHeight(delegate.handleSize)
            self.setCursor(QtCore.Qt.SizeVerCursor)

    def setVisible(self, visible):
        super(_Handle, self).setVisible(visible)
        self._shouldBeVisible = visible

    def shouldBeVisible(self):
        return self._shouldBeVisible

    def paintEvent(self, event):
        style = QtCore.QCoreApplication.instance().style()
        opt = QtGui.QStyleOption()
        opt.palette = self.palette()

        # On OSX, drawControl seems to ignore the state option and
        # draws a horizontal splitter even when we want a vertical
        # one. In this case, draw a horizontal one and rotate it...
        if platform.system() == 'Darwin' and self._delegate.orientation() == QtCore.Qt.Horizontal:
            pixmap = QtGui.QPixmap(self.height(), self.width())
            opt.state = QtGui.QStyle.State_None
        else:
            pixmap = QtGui.QPixmap(self.size())
            opt.state = QtGui.QStyle.State_Horizontal \
              if self._delegate.orientation() == QtCore.Qt.Vertical else QtGui.QStyle.State_None

        pixmap.fill(self.palette().color(QtGui.QPalette.Window))
        opt.rect = pixmap.rect()
        painter = QtGui.QPainter(pixmap)
        try:
            style.drawControl(QtGui.QStyle.CE_Splitter, opt, painter)
        finally:
            painter.end()

        if platform.system() == 'Darwin' and self._delegate.orientation() == QtCore.Qt.Horizontal:
            # this is supposed to be slow, but we don't have much choice
            rot = QtGui.QTransform()
            rot.rotate(90)
            pixmap = pixmap.transformed(rot)

        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), pixmap)

    def mousePressEvent(self, event):
        self.grabMouse()
        self._delegate._handleStartDrag(self, self.mapToGlobal(event.pos()))

    def mouseMoveEvent(self, event):
        self._delegate._handleDrag(self.mapToGlobal(event.pos()))

    def mouseReleaseEvent(self, event):
        self.releaseMouse()
        self._delegate._handleEndDrag(self.mapToGlobal(event.pos()))


class QAUISplitterLayout(QAUILoggingMixin, QtGui.QLayout):
    def __init__(self, delegate):
        super(QAUISplitterLayout, self).__init__()
        self._delegate = delegate
        self._items = list() # (handle, item)
        self._rect = None
        self._ratios = None
        # Keep references to QWidgetItems or we'll crash on PySide
        self._cache = list()

    def ratios(self):
        if self._ratios is None:
            return [1.0 / len(self._items) for _ in self._items]
        return self._ratios

    def addItem(self, item, index=-1):
        if index == -1:
            index = self.count()

        self._items.insert(index, (_Handle(self._delegate), item))
        if self._ratios is not None:
            ratio = 1.0
            for index, other in enumerate(self._ratios):
                other *= 0.9
                ratio -= other
                self._ratios[index] = other
            self._ratios.append(ratio)

        for index, (handle, item) in enumerate(self._items):
            handle.setVisible(index != 0)

        self.setGeometry(self._rect)

    def insertWidget(self, index, widget):
        item = QtGui.QWidgetItem(widget)
        self._cache.append(item)
        self.addItem(item, index=index)

    def sizeHint(self):
        prefDim = 0
        for handle, item in self._items:
            if handle.shouldBeVisible():
                prefDim += self._delegate.handleSize
            prefDim += self._dim(item.widget().sizeHint())
        return prefDim

    def setGeometry(self, rect):
        if rect is None:
            return

        # Resize all widgets, keeping ratios
        available = self._dim(rect)
        for handle, item in self._items:
            if handle.shouldBeVisible():
                available -= self._delegate.handleSize

        # Don't assume the sum is 1.0...
        remaining = available
        curPos = 0
        ratios = self.ratios()

        for index, (handle, item) in enumerate(self._items):
            if handle.shouldBeVisible():
                self._resize(handle, self._delegate.handleSize, rect)
                self._move(handle, curPos)
                curPos += self._delegate.handleSize
            if index == len(self._items) - 1:
                dim = remaining
            else:
                dim = int(math.floor(ratios[index] * available))
                remaining -= dim
            self._resize(item.widget(), dim, rect)
            self._move(item.widget(), curPos)
            curPos += dim

        self._rect = rect

    def setRatios(self, ratios):
        self._ratios = None if ratios is None else list(ratios)
        if self._rect is not None:
            self.setGeometry(self._rect)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        try:
            return self._items[index][1]
        except IndexError:
            return None

    def handleAt(self, index):
        try:
            return self._items[index][0]
        except IndexError:
            return None

    def takeAt(self, index):
        try:
            handle, item = self._items.pop(index)
        except IndexError:
            return None

        handle.setParent(None)
        handle.deleteLater()

        if self._ratios is not None:
            ratio = self._ratios.pop(index)
            for index, other in enumerate(self._ratios):
                other += ratio / len(self._items)
                self._ratios[index] = other

        for index, (handle, _) in enumerate(self._items):
            handle.setVisible(index != 0)

        self.setGeometry(self._rect)

        return item

    def _moveHandle(self, handle, center):
        for index in six.moves.range(self.count()):
            if self.handleAt(index) is handle:
                break
        else:
            return

        pos = self._pos(center)
        prevFrame = self.itemAt(index - 1).widget() # pylint: disable=W0631
        nextFrame = self.itemAt(index).widget() # pylint: disable=W0631
        minPos = self._pos(prevFrame) + self._delegate.handleSize // 2
        # XXXFIXME: preferred size rather ?
        if self._dim(prevFrame.minimumSize()) >= 0:
            minPos += self._dim(prevFrame.minimumSize())
        maxPos = self._pos(nextFrame) + self._dim(nextFrame) - self._delegate.handleSize // 2
        if self._dim(nextFrame.minimumSize()) >= 0:
            maxPos -= self._dim(nextFrame.minimumSize())
        pos = max(pos, minPos)
        pos = min(pos, maxPos)

        self._move(handle, pos - self._delegate.handleSize // 2)
        self._resize(prevFrame, pos - self._delegate.handleSize // 2 \
                     - self._pos(prevFrame), self._rect)
        self._resize(nextFrame, self._pos(nextFrame) + self._dim(nextFrame) \
                     - (pos + self._delegate.handleSize // 2), self._rect)
        self._move(nextFrame, pos + self._delegate.handleSize // 2)

        available = self._dim(self._rect) # _rect cannot be None, we've been shown
        for index, (handle, item) in enumerate(self._items):
            if handle.shouldBeVisible():
                available -= self._delegate.handleSize
        self._ratios = [1.0 * self._dim(item.widget()) / available for handle, item in self._items]
        self.setGeometry(self._rect)

    @staticmethod
    def _dim(widget):
        raise NotImplementedError

    @staticmethod
    def _pos(widget):
        raise NotImplementedError

    @staticmethod
    def _resize(widget, size, rect):
        raise NotImplementedError

    @staticmethod
    def _move(widget, pos):
        raise NotImplementedError


class QAUIHSplitterLayout(QAUISplitterLayout):
    def sizeHint(self):
        dim = super(QAUIHSplitterLayout, self).sizeHint()
        return QtCore.QSize(dim, -1)

    @staticmethod
    def _dim(widget):
        return widget.width()

    @staticmethod
    def _pos(widget):
        return widget.x()

    @staticmethod
    def _resize(widget, size, rect):
        widget.resize(size, rect.height())

    @staticmethod
    def _move(widget, pos):
        widget.move(pos, 0)


class QAUIVSplitterLayout(QAUISplitterLayout):
    def sizeHint(self):
        dim = super(QAUIVSplitterLayout, self).sizeHint()
        return QtCore.QSize(-1, dim)

    @staticmethod
    def _dim(widget):
        return widget.height()

    @staticmethod
    def _pos(widget):
        return widget.y()

    @staticmethod
    def _resize(widget, size, rect):
        widget.resize(rect.width(), size)

    @staticmethod
    def _move(widget, pos):
        widget.move(0, pos)


class QAUISplitterDelegate(QAUIDelegate):
    handleSize = 10

    def __init__(self, frameChildren, orientation):
        self._orientation = orientation
        super(QAUISplitterDelegate, self).__init__(frameChildren)

        self._layout = None
        self._dragState = (None, None, None)

    def __unicode__(self):
        return self._frame._manager.labelForSplitter(self._orientation)

    def resized(self):
        if self._layout is not None:
            self._layout.setGeometry(self._frame.rect())
        super(QAUISplitterDelegate, self).resized()

    def attach(self, frame):
        super(QAUISplitterDelegate, self).attach(frame)
        self._layout = QAUIHSplitterLayout(self) \
                       if self._orientation == QtCore.Qt.Horizontal else QAUIVSplitterLayout(self)
        frame.setLayout(self._layout)
        for child in self._frameChildren:
            self._layout.addWidget(child)

    def detach(self):
        if self._frame is not None:
            self._frame.setLayout(None)
            self._layout.deleteLater()
            self._layout = None
        super(QAUISplitterDelegate, self).detach()

    def saveState(self):
        state = {'type': 'splitter', 'orientation': 0 if self._orientation == QtCore.Qt.Horizontal \
                 else 1, 'ratios': self._layout._ratios}
        children = state['children'] = list()
        for child in self._frameChildren:
            children.append(child.saveState())
        return state

    def setRatios(self, ratios):
        self._layout.setRatios(ratios)

    def replace(self, oldFrame, newFrame):
        index = self._frameChildren.index(oldFrame)

        super(QAUISplitterDelegate, self).replace(oldFrame, newFrame)

        self._layout.takeAt(index) # pylint: disable=W0631
        self._layout.insertWidget(index, newFrame) # pylint: disable=W0631

    def title(self):
        return ','.join([child.title() for child in self._frameChildren])

    def orientation(self):
        return self._orientation

    def addChild(self, child, position=None): # pylint: disable=W0221
        if position is None:
            position = QAUIPos.RIGHT if self._orientation == QtCore.Qt.Horizontal \
                       else QAUIPos.BOTTOM

        if self._orientation == QtCore.Qt.Horizontal and position in [QAUIPos.LEFT, QAUIPos.RIGHT]:
            if position == QAUIPos.LEFT:
                self._frameChildren.insert(0, child)
                self._layout.insertWidget(0, child)
            else:
                self._frameChildren.append(child)
                self._layout.addWidget(child)
        elif self._orientation == QtCore.Qt.Vertical and position in [QAUIPos.TOP, QAUIPos.BOTTOM]:
            if position == QAUIPos.TOP:
                self._frameChildren.insert(0, child)
                self._layout.insertWidget(0, child)
            else:
                self._frameChildren.append(child)
                self._layout.addWidget(child)
        else:
            # Either CENTER or still split, but different orientation. Create a new
            # parent frame and tell our parent to replace us with it.

            from qtaui.frame import QAUIFrame
            grandFather = self._frame.frameParent()
            parentFrame = QAUIFrame(grandFather)
            if position == QAUIPos.CENTER:
                from .tab import QAUITabDelegate
                delegate = QAUITabDelegate([self._frame])
            else:
                delegate = QAUISplitterDelegate([self._frame], QtCore.Qt.Horizontal \
                      if self._orientation == QtCore.Qt.Vertical else QtCore.Qt.Vertical)
            parentFrame.setDelegate(delegate)
            grandFather._delegate.replace(self._frame, parentFrame)
            delegate.addChild(child, position)

            return # No super()!

        super(QAUISplitterDelegate, self).addChild(child)

    def _handleStartDrag(self, handle, pos):
        self._dragState = (handle, pos, handle.geometry().center())

    def _handleDrag(self, pos):
        if self._dragState is not None:
            handle, initialDragPos, initialPos = self._dragState
            self._frame.layout()._moveHandle(handle, initialPos + pos - initialDragPos)

    def _handleEndDrag(self, pos):
        self._dragState = (None, None, None)
