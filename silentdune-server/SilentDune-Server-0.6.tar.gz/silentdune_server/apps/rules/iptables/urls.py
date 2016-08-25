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

from django.conf.urls import patterns, url
from apps.rules.iptables import views

urlpatterns = [
    # url(r'^activate/(?P<code>\w{24})/$', views.activate, name='activate'),

    # Bundle Urls

    url(r'^bundles/bundle/(?P<id>[0-9]+)/edit', views.edit_bundle, name='edit_bundle'),
    url(r'^bundles/bundle/(?P<id>[0-9]+)/delete', views.delete_bundle, name='delete_bundle'),
    url(r'^bundles/bundle/(?P<id>[0-9]+)', views.view_bundle, name='view_bundle'),
    url(r'^bundles/bundle/alter_bundle_nodes/', views.alter_bundle_nodes, name="alter bundle nodes"),
    url(r'^bundles/', views.bundles, name='bundles'),
    
    # Chain Urls
    #~ url(r'^chainset/chain/(?P<chain_id>[0-9]+)/edit', views.edit_chain, name='edit_chain'), 
    #~ url(r'^chainset/chain/(?P<chain_id>[0-9]+)/delete', views.delete_chain, name='delete_chain'),
    #~ url(r'^chainset/chain/(?P<chain_id>[0-9]+)', views.view_chain, name='view_chain'),    

    # Chain Set Urls
    
    url(r'^machine_subset/(?P<machine_subset_id>[0-9]+)/edit', views.edit_machine_subset, name='edit_machine_subset'),
    url(r'^machine_subset/(?P<machine_subset_id>[0-9]+)/delete', views.delete_machine_subset, name='delete_machine_subset'),
    url(r'^machine_subset/create', views.create_machine_subset, name='create_machine_subset'),
    url(r'^machine_subset/(?P<machine_subset_id>[0-9]+)', views.view_machine_subset, name='view_machine_subset'),
    

    
    # Ring urls
    url(r'^rings/ring/move', views.move_rule, name="move_rule"),

    # Rule Urls
    url(r'^rules/rule/(?P<rule_id>[0-9]+)/edit', views.edit_rule, name='edit_rule'),
    url(r'^rules/rule/(?P<rule_id>[0-9]+)/delete', views.delete_rule, name='delete_rule'),
    url(r'^rules/rule/create/(?P<ring_id>[0-9]+)/(?P<machine_subset_id>[0-9]+)', views.create_rule, name='create_rule'),
    url(r'^rules/rule/create/(?P<machine_subset_id>[0-9]+)', views.create_rule, name='create_rule'),
    url(r'^rules/rule/enable', views.enable, name='enable'),
]

