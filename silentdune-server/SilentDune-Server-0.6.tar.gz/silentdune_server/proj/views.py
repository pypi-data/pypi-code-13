#
# Authors: Robert Abram <robert.abram@entpack.com>
#          Brett Donohoo <brett.donohoo@gmail.com>
#
# Copyright (C) 2015 EntPack
# see file 'COPYING' for use and warranty information
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

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
# from proj.permissions import *
from rest_framework import viewsets, mixins, permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import list_route
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response

from proj.mixins import *
from proj.models import *
from proj.serializer import *


class GlobalPreferencesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GlobalPreferences Model View Set
    """
    queryset = GlobalPreferences.objects.all()
    serializer_class = GlobalPreferencesSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Show id + field data for a html list object
    @list_route()
    def usernamelist(self, request):
        self.serializer_class = UserNameListSerializer
        return super(UserViewSet, self).list(self, request)

    # # Show default list - This method does nothing but call the parent method.
    # def list(self, request):
    #      return super(UserViewSet, self).list(self, request)

    # Return the record count
    @list_route(['get'])
    def count(self, request):
        count = RecordCount(User.objects.count())
        serializer = RecordCountSerializer(count)
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # Return the record count
    @list_route(['get'])
    def count(self, request):
        count = RecordCount(Group.objects.count())
        serializer = RecordCountSerializer(count)
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
        return Response(serializer.data)


def index(request):
    return HttpResponseRedirect('/dashboard/')
    
def preferences(request):
    context = {}
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True    
        if request.method == "POST":
            txt_cleaner = forms.CharField()
            txt_cleaner.required = False
            lockdown_level = txt_cleaner.clean(request.POST.get('lockdown_level',''))
            polling_interval = txt_cleaner.clean(request.POST.get('polling_interval',''))
            preferences = GlobalPreferences.objects.get(id=1)
            if lockdown_level != '':
                preferences.lockdown_slot_level = lockdown_level
            if polling_interval != '':
                preferences.polling_interval = polling_interval
                
            preferences.save()    
            
    preferences = GlobalPreferences.objects.get(id=1)
    context['lockdown_level'] = preferences.lockdown_slot_level
    context['polling_interval'] = preferences.polling_interval       
    return  render(request, 'preferences.html', context ) 
