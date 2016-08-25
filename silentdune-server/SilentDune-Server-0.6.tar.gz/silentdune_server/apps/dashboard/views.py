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
import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from proj.models import WebLogView, activity_logger, get_client_ip

from apps.alerts.models import *
from apps.rules.models import *
from apps.node.models import *
from apps.rules.iptables.models import *


import logging
logger = logging.getLogger(__name__)

@login_required
def overview(request):
    context = {}
    alert_count = Alerts.objects.filter(soft_delete=False).count()
    bundle_count = Bundle.objects.filter().count()
    node_count = Node.objects.filter().count()
    chain_count = IPTablesMachineSubset.objects.count()
    
    current_alerts = Alerts.objects.filter(soft_delete=False).order_by('-time_stamp')[:7]
    right_now = timezone.now()
    earlier_14 = right_now - datetime.timedelta(days=14)
    
    day_start = right_now - datetime.timedelta(hours=24)
    day_end   = right_now
    
    alerts_by_day = [] 
    
    morris_data = ''
    
    total_days = 60
    
    for day in range(total_days):
        daily_alert_count = Alerts.objects.filter(time_stamp__gte=day_start, time_stamp__lte=day_end, soft_delete=False).count()
        alerts_by_day.append(daily_alert_count)
        offset_day = day + 1
        if day != total_days-1:
            morris_data += '{ period: \''+ day_start.strftime('%Y-%m-%d') +'\', alerts: '+ str(daily_alert_count) +' },'
        else: 
            morris_data += '{ period: \''+ day_start.strftime('%Y-%m-%d') +'\', alerts: '+ str(daily_alert_count) +' }'
            
        print('day start: ', day_start, ' day_end: ', day_end)
        print(' day: , ', day, ' alert count: ', daily_alert_count )
        day_end = day_start
        day_start = day_end - datetime.timedelta(hours=24)
        print()
        
        
    
    
    
    #two_weeks_of_alerts = Alerts.objects.filter(time_stamp__range=(earlier_14, right_now), soft_delete=False).count()
    #print('total alerts: ', two_weeks_of_alerts)
    
    
    context['morris_data'] = morris_data
    context['alerts_by_day'] = alerts_by_day
    context['right_now'] = right_now
    context['current_alerts'] = current_alerts
    context['alert_count'] = alert_count
    context['bundle_count'] = bundle_count
    context['node_count'] = node_count
    context['chain_count'] = chain_count

    return render(request, 'dashboard/overview.html', context)

