#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /leaf.py
#  NAME
#    leaf --
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

from PySide import QtCore
from .base import QAUIDelegate, QAUIPos


class QAUILeafDelegate(QAUIDelegate):
    def __init__(self):
        super(QAUILeafDelegate, self).__init__([])

    def __unicode__(self):
        return self.title()

    def currentFrameChild(self): # pylint: disable=R0201
        return None

    def saveState(self):
        raise RuntimeError('Should not be called')

    def addChild(self, child, position): # pylint: disable=W0221
        from ..frame import QAUIFrame
        frame = QAUIFrame(manager=self._frame._manager)
        self._frame.frameParent()._delegate.replace(self._frame, frame)

        if position == QAUIPos.CENTER:
            from .tab import QAUITabDelegate
            delegate = QAUITabDelegate([child, self._frame])
        elif position in [QAUIPos.LEFT, QAUIPos.RIGHT]:
            from .splitter import QAUISplitterDelegate
            if position == QAUIPos.LEFT:
                delegate = QAUISplitterDelegate([child, self._frame], QtCore.Qt.Horizontal)
            else:
                delegate = QAUISplitterDelegate([self._frame, child], QtCore.Qt.Horizontal)
        else:
            from .splitter import QAUISplitterDelegate
            if position == QAUIPos.TOP:
                delegate = QAUISplitterDelegate([child, self._frame], QtCore.Qt.Vertical)
            else:
                delegate = QAUISplitterDelegate([self._frame, child], QtCore.Qt.Vertical)

        frame.setDelegate(delegate)
