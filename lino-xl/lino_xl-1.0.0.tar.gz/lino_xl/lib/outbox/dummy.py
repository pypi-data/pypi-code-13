# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
#
# This file is part of Lino XL.
#
# Lino XL is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino XL is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino XL.  If not, see
# <http://www.gnu.org/licenses/>.

"""
The :term:`dummy module` for `outbox`, 
used by :func:`lino.core.utils.resolve_app`.
"""
from lino.api import dd


class Mailable(object):
    pass

#~ class MailableType(object): pass


class MailableType(dd.Model):
    email_template = dd.DummyField()
    attach_to_email = dd.DummyField()

    class Meta:
        abstract = True

MailsByController = dd.DummyField()
