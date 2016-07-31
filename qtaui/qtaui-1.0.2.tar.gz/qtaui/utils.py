#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /utils.py
#  NAME
#    utils --
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


class QAUILoggingMixin(object):
    _logger = logging.getLogger('qtaui')

    def d(self, *args, **kwargs): # pylint: disable=C0103
        self._logger.debug(*args, **kwargs)

    def i(self, *args, **kwargs): # pylint: disable=C0103
        self._logger.info(*args, **kwargs)

    def w(self, *args, **kwargs): # pylint: disable=C0103
        self._logger.warning(*args, **kwargs)

    def e(self, *args, **kwargs): # pylint: disable=C0103
        self._logger.error(*args, **kwargs)
