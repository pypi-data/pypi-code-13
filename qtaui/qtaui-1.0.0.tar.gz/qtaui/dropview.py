#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /dropview.py
#  NAME
#    dropview --
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
#    17 Jul 2016
#***

from PySide import QtGui, QtCore

from .delegate.base import QAUIPos
from .delegate.splitter import QAUISplitterDelegate
from .delegate.noop import QAUINoopDelegate

# XXXTODO: use QGraphicsView? => drop shadows, etc.


class QAUIDropView(QtGui.QWidget):
    STATE_HIDDEN = 0
    STATE_SHOWING = 1
    STATE_HIDING = 2
    STATE_SHOWN = 3

    finished = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        self._manager = kwargs.pop('manager')
        super(QAUIDropView, self).__init__(*args, **kwargs)
        self._currentValue = 0.0
        self._animation = None
        self._state = self.STATE_HIDDEN

        font = self.font()
        font.setWeight(font.Bold)
        self.setFont(font)

        metrics = QtGui.QFontMetrics(self.font())
        self._baseHeight = metrics.height() * 2
        self._hitRegions = []
        self._currentHitRegion = (None, None, None)

    def start(self):
        if self._state == self.STATE_HIDDEN:
            self._state = self.STATE_SHOWING
            self._animation = QtCore.QPropertyAnimation(self, 'currentValue')
            self._animation.setStartValue(0.0)
            self._animation.setEndValue(1.0)
            self._animation.finished.connect(self._animationFinished)
            self._animation.start()
        elif self._state == self.STATE_HIDING:
            self._state = self.STATE_SHOWING
            self._animation.stop()
            self._animation.setStartValue(self.currentValue)
            self._animation.setEndValue(1.0)
            self._animation.start()
        elif self._state == self.STATE_SHOWING:
            pass
        elif self._state == self.STATE_SHOWN:
            pass
        else:
            assert False

    def stop(self, frame):
        if self._state == self.STATE_HIDDEN:
            pass
        elif self._state == self.STATE_HIDING:
            pass
        elif self._state == self.STATE_SHOWING:
            self._animation.stop()
            self._state = self.STATE_HIDING
            self._animation.setStartValue(1.0)
            self._animation.setEndValue(0.0)
            self._animation.start()
        elif self._state == self.STATE_SHOWN:
            self._state = self.STATE_HIDING
            self._animation = QtCore.QPropertyAnimation(self, 'currentValue')
            self._animation.setStartValue(self.currentValue)
            self._animation.setEndValue(0.0)
            self._animation.finished.connect(self._animationFinished)
            self._animation.start()
            if self._currentHitRegion != (None, None, None):
                _, parent, position = self._currentHitRegion
                parent.addFrame(frame, position)
                frame.docked.emit(parent, position)
        else:
            assert False

    def _animationFinished(self):
        if self._state == self.STATE_SHOWING:
            self._state = self.STATE_SHOWN
        elif self._state == self.STATE_HIDING:
            self._state = self.STATE_HIDDEN
            self._hitRegions = []
            self._currentHitRegion = (None, None, None)
            self.finished.emit()
        else:
            assert False

        self._animation.finished.disconnect(self._animationFinished)
        self._animation = None

    def _get_currentValue(self):
        return self._currentValue
    def _set_currentValue(self, value):
        self._currentValue = value
        self.update()
    currentValue = QtCore.Property(float, _get_currentValue, _set_currentValue)

    def notifyFrameMove(self, pos):
        pos = self.mapFromGlobal(pos)
        for rect, frame, position in self._hitRegions:
            if rect.contains(pos):
                if self._currentHitRegion != (rect, frame, position):
                    self._currentHitRegion = (rect, frame, position)
                    self.update()
                break
        else:
            if self._currentHitRegion != (None, None, None):
                self._currentHitRegion = (None, None, None)
                self.update()

    def paintEvent(self, event):
        self._hitRegions = []
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.Antialiasing, True)
        frame = self._manager.topFrame()
        if isinstance(frame._delegate, QAUINoopDelegate):
            painter.setOpacity(self.currentValue)
            if self._currentHitRegion != (None, None, None):
                painter.fillRect(self._manager.rect(), QtCore.Qt.blue)
            self._drawHint(painter, self._manager, self._manager.rect().center(), None)
        else:
            self._renderFrame(painter, frame, frame.rect())

    def _renderFrame(self, painter, frame, targetRect):
        if frame.width() <= 0 or frame.height() <= 0:
            return

        painter.save()
        try:
            # Draw frame centered and scaled in targetRect
            pixmap = QtGui.QPixmap(frame.size())
            frame.render(pixmap)
            pixmap = pixmap.scaled(targetRect.size(), QtCore.Qt.KeepAspectRatio)
            rect = QtCore.QRect(QtCore.QPoint(0, 0), pixmap.size())
            rect.moveCenter(targetRect.center())
            painter.drawPixmap(rect, pixmap)
            # Darken the whole stuff
            painter.setOpacity(0.5 * self.currentValue)
            painter.fillRect(targetRect, QtCore.Qt.black)
            # Draw hint region
            if frame == self._currentHitRegion[1]:
                hint = QtCore.QRect(rect)
                if self._currentHitRegion[2] == QAUIPos.TOP:
                    hint.adjust(0, 0, 0, -hint.height()/2)
                elif self._currentHitRegion[2] == QAUIPos.BOTTOM:
                    hint.adjust(0, hint.height()/2, 0, 0)
                elif self._currentHitRegion[2] == QAUIPos.LEFT:
                    hint.adjust(0, 0, -hint.width()/2, 0)
                elif self._currentHitRegion[2] == QAUIPos.RIGHT:
                    hint.adjust(hint.width()/2, 0, 0, 0)
                painter.fillRect(hint, QtCore.Qt.blue)
            # Draw title
            painter.setOpacity(self.currentValue)
            metrics = painter.fontMetrics()
            text = metrics.elidedText(unicode(frame._delegate),
                                      QtCore.Qt.ElideRight,
                                      rect.width() - 20)
            painter.setPen(QtCore.Qt.red)
            painter.drawText(rect.x() + 10, rect.y() + metrics.ascent() + 4, text)
            # Blue rect around frame thumbnail
            painter.setPen(QtGui.QPen(QtCore.Qt.blue, 3))
            painter.drawRect(rect)

            pos = rect.center()
            self._drawHint(painter, frame,
                           pos - QtCore.QPoint(0, rect.height() / 2 - self._baseHeight * 3 / 2),
                           QAUIPos.CENTER)
            self._drawHint(painter, frame,
                           pos - QtCore.QPoint(0, rect.height() / 2 - self._baseHeight / 2),
                           QAUIPos.TOP)
            self._drawHint(painter, frame,
                           pos + QtCore.QPoint(0, rect.height() / 2 - self._baseHeight / 2),
                           QAUIPos.BOTTOM)
            self._drawHint(painter, frame,
                           pos - QtCore.QPoint(rect.width() / 2 - self._baseHeight / 2, 0),
                           QAUIPos.LEFT)
            self._drawHint(painter, frame,
                           pos + QtCore.QPoint(rect.width() / 2 - self._baseHeight / 2, 0),
                           QAUIPos.RIGHT)
        finally:
            painter.restore()

        # Leave room for hints
        rect.adjust(self._baseHeight * self.currentValue,
                    self._baseHeight * 2 * self.currentValue,
                    -self._baseHeight * self.currentValue,
                    -self._baseHeight * self.currentValue)

        if isinstance(frame._delegate, QAUISplitterDelegate):
            scaleX = 1.0 * rect.width() / frame.width()
            scaleY = 1.0 * rect.height() / frame.height()

            for child in frame._delegate._frameChildren:
                childRect = QtCore.QRect(child.x() * scaleX,
                                         child.y() * scaleY,
                                         child.width() * scaleX,
                                         child.height() * scaleY)
                childRect.translate(rect.topLeft())
                self._renderFrame(painter, child, childRect)
        elif frame._delegate.currentFrameChild() is not None:
            self._renderFrame(painter, frame._delegate.currentFrameChild(), rect)

    def _drawHint(self, painter, frame, center, position):
        if position == QAUIPos.CENTER:
            path = QtGui.QPainterPath()
            rect = QtCore.QRect(0, 0, 2 * self._baseHeight, self._baseHeight * 0.6)
            rect.moveCenter(center)
            self._hitRegions.append((rect, frame, position))
            path.addRoundedRect(rect, self._baseHeight * 0.6 / 2, self._baseHeight * 0.6 / 2)
            color = QtGui.QColor(QtCore.Qt.blue)
            painter.setPen(color.lighter(150))
            painter.fillPath(path, color)
            rect = QtCore.QRect(0, 0, 2 * self._baseHeight / 3, self._baseHeight * 0.6)
            rect.moveCenter(center)
            path.addRect(rect)
            painter.drawPath(path)
        else:
            color = QtGui.QColor(QtCore.Qt.blue)
            painter.setPen(color.lighter(150))

            rect = QtCore.QRect(0, 0, 0.8 * self._baseHeight, 0.6 * self._baseHeight)
            rect.moveCenter(center)
            self._hitRegions.append((rect, frame, QAUIPos.CENTER if position is None else position))

            path = QtGui.QPainterPath()
            path.addRoundedRect(rect, 5, 5)
            painter.drawPath(path)

            if position in [QAUIPos.TOP, QAUIPos.BOTTOM]:
                rect = QtCore.QRect(0, 0, 0.7 * self._baseHeight, 0.2 * self._baseHeight)
                if position == QAUIPos.TOP:
                    rect.moveCenter(QtCore.QPoint(center.x(), center.y() - 0.2 * self._baseHeight))
                else:
                    rect.moveCenter(QtCore.QPoint(center.x(), center.y() + 0.2 * self._baseHeight))
            elif position in [QAUIPos.LEFT, QAUIPos.RIGHT]:
                rect = QtCore.QRect(0, 0, 0.2 * self._baseHeight, 0.5 * self._baseHeight)
                if position == QAUIPos.LEFT:
                    rect.moveCenter(QtCore.QPoint(center.x() - 0.15 * self._baseHeight, center.y()))
                else:
                    rect.moveCenter(QtCore.QPoint(center.x() + 0.15 * self._baseHeight, center.y()))
            else: # None
                rect = QtCore.QRect(0, 0, 0.7 * self._baseHeight, 0.7 * self._baseHeight)
                rect.moveCenter(center)

            path = QtGui.QPainterPath()
            path.addRoundedRect(rect, 5, 5)
            painter.fillPath(path, color)
            painter.drawPath(path)
