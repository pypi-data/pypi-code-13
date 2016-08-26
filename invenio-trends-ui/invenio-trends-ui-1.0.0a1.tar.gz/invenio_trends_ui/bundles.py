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

"""UI for Invenio-Search."""

from flask_assets import Bundle
from invenio_assets import NpmBundle

css = NpmBundle(
        'scss/invenio_trends_ui/trends.scss',
        filters='scss, cleancss',
        output='gen/trends.%(version)s.css'
)

js = NpmBundle(
        'js/invenio_trends_ui/app.js',
        'js/invenio_trends_ui/trends.vis.js',
        filters='requirejs',
        depends=('node_modules/invenio-trends-js/dist/*.js',),
        output='gen/trends.%(version)s.js',
        npm={
            "almond": "~0.3.1",
            'angular': '~1.4.10',
            'angular-loading-bar': '~0.9.0'
        },
)
