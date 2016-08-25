#
# Authors: Robert Abram <robert.abram@entpack.com>
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

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django import forms
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.accounts.models import UserProfile
from apps.alerts.models import *

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from proj.serializer import RecordCountSerializer
from apps.alerts.serializers import IPAlertEventSerializer
from proj.models import RecordCount


@login_required
def alerts(request):
    context = {}
        
    
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True
 

    # get the alert summaries and individual isolated alerts and disply them.    
    alerts_to_list = list(Alerts.objects.filter(summary__isnull=True))
    
    summaries_to_list = AlertSummaries.objects.all()
    
    for summary in summaries_to_list:
        summary.time_stamp = Alerts.objects.filter(summary_id = summary.id).first().time_stamp
        summary.descr = 'this summary has been added'
        summary.total = Alerts.objects.filter(summary_id = summary.id).count()
        summary.id = Alerts.objects.filter(summary_id = summary.id).first().id
        alerts_to_list.append(summary)
        
    alerts_results = sorted(alerts_to_list, key=lambda alert: alert.time_stamp, reverse=True)     
    
    paginator = Paginator(alerts_results, 20)
     
    page = request.GET.get('page')

    
    try:
        alerts = paginator.page(page)
    except PageNotAnInteger:
        alerts = paginator.page(1)
    except EmptyPage:
        alerts = paginator.page(paginator.num_pages)
        
    context = {
        'can_edit': "write" in request.user.profile.oauth_scope,
        'alerts': alerts,
        'alert_count': Alerts.objects.filter(soft_delete=False).count(),
    }

    return render(request, 'alerts/alerts.html', context)
    
    
@login_required
def view(request, id):
    # if the displayed alerts are all from one summary group
    # then the id's are prepended with '0' so that their view
    # will be displayed in detail 
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()    
    
    breakout = False
    
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True  
        
    if id[0] == '0':
        breakout = True
        id = id[1:]
            
    this_alert = Alerts.objects.filter(id = id)
    
    if this_alert[0].summary == None or breakout:
        context['alert'] = this_alert[0]
        template = 'alerts/view_alert.html'
        
    else:
        context['alerts'] = Alerts.objects.filter(summary_id=this_alert[0].summary.id).order_by('-time_stamp')
        context['breakout'] = True
        template = 'alerts/alerts.html'
        
    return render(request, template, context)      
    
    
    


# ---- Start API code -------------#

class IPAlertEventViewSet(viewsets.ModelViewSet):
    """
    Node Model View Set
    """
    queryset = IPAlertEvent.objects.all()
    serializer_class = IPAlertEventSerializer

    # Return the Node model record count
    @list_route(['get'])
    def count(self, request):
        count = RecordCount(IPAlertEvent.objects.count())
        serializer = RecordCountSerializer(count)
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Allow filtering AlertEvent by dest_addr
        """
        queryset = IPAlertEvent.objects.all()

        dest_addr = self.request.query_params.get('dest_addr', None)
        if dest_addr is not None:
            queryset = queryset.filter(dest_addr=dest_addr)
        return queryset

    def create(self, request, *args, **kwargs):
        # https://docs.getsentry.com/hosted/learn/rollups/

        # TODO: Rollup Alerts into Alerts and AlertSummary.
        # Only create a new IPAlertEvent record if we are not rolling up.

        serializer = IPAlertEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # TODO: Create Alerts and AlertSummary records.

        return Response({'id': serializer.data['id']}, status=status.HTTP_201_CREATED)

# ---- End API code ---------------#
