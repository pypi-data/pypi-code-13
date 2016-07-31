#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /demo.py
#  NAME
#    demo -- 
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

import logging
from PySide import QtCore, QtGui
from qtaui import QAUIPos, QAUIManager, QAUILeafFrame


class TestFrame(QtGui.QMainWindow):
    def __init__(self):
        super(TestFrame, self).__init__()

        frame = QAUIManager(self)
        self.setCentralWidget(frame)

        class QAUILabel(QAUILeafFrame):
            def __init__(self, text, *args, **kwargs):
                super(QAUILabel, self).__init__(title='Title %s' % text, *args, **kwargs)
                self._text = text
                btn = QtGui.QLabel(text)
                layout = QtGui.QHBoxLayout()
                layout.addWidget(btn)
                self.setLayout(layout)

            def __repr__(self):
                return self._text

        frame.addFrame(QAUILabel('Test 1', frame), QAUIPos.BOTTOM)
        frame.addFrame(QAUILabel('Test 2', frame), QAUIPos.BOTTOM)
        frame.addFrame(QAUILabel('Test 3', frame), QAUIPos.CENTER)
        frame.addFrame(QAUILabel('Test 4', frame), QAUIPos.CENTER)
        frame.addFrame(QAUILabel('Test 5', frame), QAUIPos.LEFT)
        frame.addFrame(QAUILabel('Top-level test', manager=frame), QAUIPos.FLOATING)

        self.resize(600, 400)
        self.show()
        self.raise_()

        frame.dump()
        self._manager = frame
        self._manager.frameDocked.connect(self.docked)
        self._manager.frameUndocked.connect(self.undocked)
        self._manager.frameClosed.connect(self.closed)

        settings = QtCore.QSettings('net.jeromelaheurte', 'QAUI Demo')
        if settings.contains('state'):
            self._manager.restoreState(settings.value('state'))

    def docked(self, frame, parent, position):
        print 'Frame %s docked to %s in position %d' % (frame, parent, position)

    def undocked(self, frame):
        print 'Frame %s undocked' % frame

    def closed(self, frame):
        print 'Frame %s closed' % frame

    def closeEvent(self, event):
        settings = QtCore.QSettings('net.jeromelaheurte', 'QAUI Demo')
        settings.setValue('state', self._manager.saveState())
        self._manager.shutdown()
        event.accept()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QtGui.QApplication([])
    win = TestFrame()
    app.exec_()
