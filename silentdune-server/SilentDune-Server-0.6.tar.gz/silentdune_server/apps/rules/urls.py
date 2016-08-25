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

from django.conf.urls import patterns, url, include
from apps.rules import views

urlpatterns = [
    # url(r'^activate/(?P<code>\w{24})/$', views.activate, name='activate'),
    url(r'^bundles/create', views.create_bundle, name='create_bundle'),
    url(r'^bundles/', views.bundles, name='bundles'),
    

    # Chain Set Urls
    url(r'^machine_subsets/', views.machine_subsets, name='machine_subsets'),

    url(r'^iptables/', include('apps.rules.iptables.urls', namespace='iptables')),
]

