#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /noop.py
#  NAME
#    noop --
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

from .base import QAUIDelegate


class QAUINoopDelegate(QAUIDelegate):
    def __unicode__(self):
        return self.title()

    def saveState(self):
        raise RuntimeError('Should not be called')

    def currentFrameChild(self):
        return self._frameChildren[0] if self._frameChildren else None

    def attach(self, frame):
        for child in self._frameChildren:
            child.setGeometry(frame.rect())
        super(QAUINoopDelegate, self).attach(frame)

    def title(self):
        from qtaui.frame import QAUILeafFrame
        if isinstance(self._frame, QAUILeafFrame):
            return self._frame._title
        return self._frameChildren[0].title() if self._frameChildren else ''

    def addChild(self, child):
        self._frame.frameParent()._delegate.replace(self._frame, child)

    def resized(self):
        for child in self._frameChildren:
            child.setGeometry(self._frame.rect())
        super(QAUINoopDelegate, self).resized()
