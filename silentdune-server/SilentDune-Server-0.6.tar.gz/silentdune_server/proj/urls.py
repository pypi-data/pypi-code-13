#
# Authors: Robert Abram <robert.abram@entpack.com>,
#          Brett Donohoo <brett.donohoo@entpack.com>
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

from django.conf.urls import patterns, include, url
from django.contrib import admin


# TODO: Replace these views with oauth enabled views
from django.contrib.auth.views import logout_then_login, password_change, password_reset, password_change_done

# Replacement oauth enabled views
from apps.accounts.views import sdLogin
from apps.accounts.forms import SDAuthenticationForm

# Import app views
from proj.views import *
from apps.rules.iptables.views import *
from apps.rules.views import *
from apps.node.views import *
from apps.alerts.views import IPAlertEventViewSet
# from apps.alerts.views import *

# Set REST routes
from rest_framework import routers

admin.autodiscover()

# API urls
router = routers.DefaultRouter()
# router.register(r'accounts/users', UserViewSet)
# router.register(r'accounts/groups', GroupViewSet)
# router.register(r'lists/rule-platform', RulePlatformViewSet)
# router.register(r'lists/chainsetslots', ChainSetSlotsViewSet)
# router.register(r'iptables/chains', IPChainViewSet)
# router.register(r'iptables/chainsets', IPChainSetViewSet)
# router.register(r'iptables/rules', IPRuleViewSet)
# router.register(r'iptables/rings', IPRingViewSet)
# router.register(r'iptables/lists/transportversion', IPTransportVersionViewSet)
# router.register(r'iptables/lists/protocols', IPProtocolsViewSet)
# router.register(r'iptables/lists/protocols-adv', IPProtocolsAdvViewSet)
# router.register(r'iptables/lists/tables', IPTablesViewSet)
# router.register(r'iptables/lists/tables-adv', IPTablesAdvViewSet)
# router.register(r'iptables/lists/chains', IPChainsViewSet)
# router.register(r'iptables/lists/match-ext', IPMatchExtensionsViewSet)
# router.register(r'iptables/lists/match-ext-adv', IPMatchExtensionsAdvViewSet)

# --- Global Preferences --- #
router.register(r'globals', GlobalPreferencesViewSet)

router.register(r'alerts/iptables', IPAlertEventViewSet)

# --- Node APIs --- #
router.register(r'nodes/(?P<node>.+)/interfaces', NodeInterfaceViewSet)
router.register(r'nodes/(?P<node>.+)/bundle', NodeBundleViewSet)
router.register(r'nodes/(?P<node>.+)/processes', NodeProcessViewSet)
router.register(r'nodes', NodeViewSet)

# --- Bundle APIs --- #
router.register(r'bundles/(?P<bundle>.+)/machine_subsets', IPMachineSetViewSet)
router.register(r'bundles', BundleViewSet)

# --- iptables platform APIs --- #
router.register(r'iptables/machine_subsets/(?P<set>.+)/chains/(?P<chain>.+)/rings/(?P<ring>.+)/rules', IPRuleViewSet)
router.register(r'iptables/machine_subsets/(?P<set>.+)/chains/(?P<chain>.+)/rings', IPRingViewSet)
router.register(r'iptables/machine_subsets/(?P<set>.+)/chains', IPChainViewSet)
router.register(r'iptables/machine_subsets', IPMachineSubsetViewSet)

urlpatterns = [

    url(r'^$', index, name='index'),

    # Account Management urls
    url(r'^accounts/', include('apps.accounts.urls', namespace='accounts', app_name='accounts')),

    url(r'^accounts/login/', sdLogin,
        {'template_name': 'accounts/login.html', 'authentication_form': SDAuthenticationForm,
         'redirect_field_name': 'next'}, name='login'),
    url(r'^accounts/logout/', logout_then_login, name='logout'),
    url(r'^accounts/passwordchange/', password_change,
        {'template_name': 'accounts/password_change_form.html'}, name='passwordchange'),
        
    url(r'^preferences/', preferences, name='preferences'),    

    # Dashboard urls
    url(r'^dashboard/', include('apps.dashboard.urls', namespace='dashboard')),

    # Rule urls
    url(r'^rules/', include('apps.rules.urls', namespace='rules')),

    # Node urls
    url(r'^node/', include('apps.node.urls')),

    # Alert urls
    url(r'^alert/', include('apps.alerts.urls', namespace='alerts')),

    # Oauth urls
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # django admin urls
    url(r'^admin/', include(admin.site.urls)),

    # API urls
    url(r'^api/', include(router.urls)),

]

