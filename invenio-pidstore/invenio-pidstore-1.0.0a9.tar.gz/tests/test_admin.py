# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.
"""Admin interface tests."""

from __future__ import absolute_import, print_function

import uuid

from flask_admin import Admin, menu
from invenio_db import db

from invenio_pidstore.admin import FilterUUID, object_formatter, pid_adminview
from invenio_pidstore.models import PersistentIdentifier


def test_admin(app):
    """Test flask-admin interace."""
    admin = Admin(app, name="AdminExt")

    pid_kwargs = dict(pid_adminview)

    assert 'model' in pid_adminview
    assert 'modelview' in pid_adminview

    # Register both models in admin
    pid_model = pid_kwargs.pop('model')
    pid_mv = pid_kwargs.pop('modelview')
    admin.add_view(pid_mv(pid_model, db.session, **pid_kwargs))

    # Check if generated admin menu contains the correct items
    menu_items = {str(item.name): item for item in admin.menu()}

    # PIDStore should be a category
    assert 'Records' in menu_items
    assert menu_items['Records'].is_category()
    assert isinstance(menu_items['Records'], menu.MenuCategory)

    # Items in PIDStore menu should be the modelviews
    submenu_items = {str(item.name): item for item in
                     menu_items['Records'].get_children()}
    assert 'Persistent Identifier' in submenu_items
    assert isinstance(submenu_items['Persistent Identifier'], menu.MenuView)


def test_filter_uuid(app):
    """Test FilterUUID."""
    with app.app_context():
        myuuid = uuid.uuid4()
        PersistentIdentifier.create(
            'doi', '10.1234/a', object_type='tst', object_uuid=myuuid)

        query = FilterUUID(PersistentIdentifier.object_uuid, 'Test').apply(
            PersistentIdentifier.query, str(myuuid), None)
        assert query.count() == 1


def test_object_formatter(app):
    """Test FilterUUID."""
    @app.route('/<id>')
    def test_detail(id=None):
        return str(id)

    with app.test_request_context():
        app.config['PIDSTORE_OBJECT_ENDPOINTS']['tst'] = 'test_detail'
        pid = PersistentIdentifier.create(
            'doi', '10.1234/a', object_type='tst', object_uuid=uuid.uuid4())
        assert 'View' in object_formatter(None, None, pid, None)

        pid = PersistentIdentifier.create(
            'doi', '10.1234/b', )
        assert object_formatter(None, None, pid, None) == ''
