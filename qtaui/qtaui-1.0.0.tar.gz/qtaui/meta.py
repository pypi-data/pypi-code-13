#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

#****h* /meta.py
#  NAME
#    meta --
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
#    31 Jul 2016
#***

version = '1.0.0'
version_info = map(int, version.split('.'))

class PackageInfo(object):
    short_description = 'A clone of wx.aui for PySide'
    author_name = u'Jérôme Laheurte'
    author_email = 'jerome@jeromelaheurte.net'
    project_url = 'https://bitbucket.org/fraca7/qtaui'
    download_url = 'https://pypi.python.org/packages/source/q/qtaui/qtaui-%s.tar.gz' % version
    project_name = 'qtaui'
    version = version
