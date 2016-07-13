#!/usr/bin/python
# -*- coding: utf-8 -*-

# Libervia: a SAT frontend
# Copyright (C) 2009-2016 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ..common import constants


class Const(constants.Const):

    APP_NAME = 'Libervia'
    APP_NAME_FILE = "libervia"
    SERVICE_PROFILE = 'libervia'  # the SàT profile that is used for exporting the service

    SESSION_TIMEOUT = 300  # Session's timeout, after that the user will be disconnected
    HTML_DIR = "html/"
    THEMES_DIR = "themes/"
    THEMES_URL = "themes"
    MEDIA_DIR = "media/"
    CARDS_DIR = "games/cards/tarot"

    ERRNUM_BRIDGE_ERRBACK = 0  # FIXME
    ERRNUM_LIBERVIA = 0  # FIXME

    # Security limit for Libervia (get/set params)
    SECURITY_LIMIT = 5

    # Security limit for Libervia server_side
    SERVER_SECURITY_LIMIT = constants.Const.NO_SECURITY_LIMIT

    # keys for cache values we can get from browser
    ALLOWED_ENTITY_DATA = {'avatar', 'nick'}

    STATIC_RSM_MAX_LIMIT = 100
    STATIC_RSM_MAX_DEFAULT = 10
    STATIC_RSM_MAX_COMMENTS_DEFAULT = 10
