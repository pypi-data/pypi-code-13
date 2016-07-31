#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /tab.py
#  NAME
#    tab --
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

from PySide import QtCore, QtGui

from .base import QAUIDelegate, QAUIPos


class QAUITabDelegate(QAUIDelegate):
    def __init__(self, frameChildren):
        self._titleBar = None
        self._tabs = None
        self._layout = None
        self._stackLayout = None
        super(QAUITabDelegate, self).__init__(frameChildren)

    def __unicode__(self):
        return self._frame._manager.labelForTabs().format(title=self.currentFrameChild().title())

    def currentFrameChild(self):
        return self._frameChildren[self._tabs.currentIndex()]

    def attach(self, frame):
        super(QAUITabDelegate, self).attach(frame)

        self._tabs = QtGui.QTabBar(self._frame)
        self._tabs.setMovable(True)
        self._tabs.tabMoved.connect(self._tabMoved)
        self._tabs.currentChanged.connect(self._updateTitle)

        from qtaui.frame import QAUITitleBar
        self._titleBar = QAUITitleBar(self._frame)

        self._stackLayout = QtGui.QStackedLayout()
        self._stackLayout.setContentsMargins(0, 0, 0, 0)
        self._tabs.currentChanged.connect(self._stackLayout.setCurrentIndex)

        self._layout = QtGui.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self._titleBar)
        self._layout.addWidget(self._tabs)
        self._layout.addLayout(self._stackLayout, stretch=1)
        self._frame.setLayout(self._layout)
        self._frame.titleChanged.connect(self._updateTabs)

        for child in self._frameChildren:
            self._tabs.addTab(child.title())
            self._stackLayout.addWidget(child)

    def saveState(self):
        state = {'type': 'tab', 'current': self._tabs.currentIndex()}
        children = state['children'] = list()
        for child in self._frameChildren:
            children.append(child.saveState())
        return state

    def setCurrent(self, index):
        self._tabs.setCurrentIndex(index)

    def _updateTabs(self):
        for index, child in enumerate(self._frameChildren):
            self._tabs.setTabText(index, child.title())

    def _updateTitle(self, index):
        self._frame.titleChanged.emit()

    # XXXFIXME: Documentation says 'from, to' but in practice this is 'to, from' ?
    def _tabMoved(self, toIndex, fromIndex):
        frame = self._frameChildren.pop(fromIndex)
        self._frameChildren.insert(toIndex, frame)
        item = self._stackLayout.takeAt(fromIndex)
        self._stackLayout.insertWidget(toIndex, item.widget())
        self._stackLayout.setCurrentIndex(self._tabs.currentIndex())

    def detach(self):
        if self._frame is not None:
            self._frame.titleChanged.disconnect(self._updateTabs)
            self._tabs.tabMoved.disconnect(self._tabMoved)
            self._tabs.currentChanged.disconnect(self._updateTitle)
            self._tabs.currentChanged.disconnect(self._stackLayout.setCurrentIndex)
            self._frame.setLayout(None)
            self._layout.deleteLater()
            self._tabs.deleteLater()
            self._titleBar.deleteLater()
            self._stackLayout.deleteLater()
            self._layout = self._tabs = self._stackLayout = self._titleBar = None
        super(QAUITabDelegate, self).detach()

    def replace(self, oldFrame, newFrame):
        for index in six.moves.range(self._tabs.count()):
            if self._frameChildren[index] == oldFrame:
                break
        else:
            assert False

        super(QAUITabDelegate, self).replace(oldFrame, newFrame)

        self._tabs.removeTab(index) # pylint: disable=W0631
        self._stackLayout.removeWidget(oldFrame)
        self._frameChildren.pop(index) # pylint: disable=W0631
        self._frameChildren.insert(index, newFrame) # pylint: disable=W0631
        self._tabs.insertTab(index, newFrame.title()) # pylint: disable=W0631
        self._stackLayout.insertWidget(index, newFrame) # pylint: disable=W0631
        self._tabs.setCurrentIndex(index) # pylint: disable=W0631

    def title(self):
        return u'' if self._tabs is None else self._frameChildren[self._tabs.currentIndex()].title()

    def addChild(self, child, position=QAUIPos.CENTER):
        if position == QAUIPos.CENTER:
            super(QAUITabDelegate, self).addChild(child)
            self._frameChildren.append(child)
            self._tabs.addTab(child.title())
            self._stackLayout.addWidget(child)
        else:
            from .splitter import QAUISplitterDelegate
            from qtaui.frame import QAUIFrame
            grandFather = self._frame.frameParent()
            parentFrame = QAUIFrame(grandFather)
            delegate = QAUISplitterDelegate([self._frame], QtCore.Qt.Horizontal \
                           if position in [QAUIPos.LEFT, QAUIPos.RIGHT] else QtCore.Qt.Vertical)
            parentFrame.setDelegate(delegate)
            grandFather._delegate.replace(self._frame, parentFrame)
            delegate.addChild(child, position)

    def childRemoved(self, child):
        index = self._frameChildren.index(child)
        self._tabs.removeTab(index)
        # setParent() in super will remove the child from the stacked layout
        super(QAUITabDelegate, self).childRemoved(child)
