#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from apps.node import views
from django.conf.urls import patterns, url

urlpatterns = [
#    url(r'^auth/', views.authenticate, name='authenticate'),
    url(r'^nodes/', views.nodes, name='nodes'),
    url(r'^node/(?P<incoming_id>[0-9]+)/edit', views.edit_node, name='edit_node'),
    url(r'^node/(?P<incoming_id>[0-9]+)/delete', views.delete_node, name='delete_node'),
    url(r'^node/toggle_locked/', views.toggle_locked, name="toggle locked"),
    url(r'^node/(?P<incoming_id>[0-9]+)', views.view_node, name='view_node'),
    
    #url(r'^/node/(?P<id>[0-9]+)/edit', views.edit_node, name='edit_node'),
    #bundles/bundle/(?P<id>[0-9]+)/edit
]
