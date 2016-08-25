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

from django.utils.translation import ugettext_lazy as _
from django.db import models
from proj.models import BaseModel
from apps.node.models import Node

ALERT_LEVELS = (
    ('high', _('High')),
    ('medium', _('Medium')),
    ('low', _('Low')),
)


class AlertSummaries (BaseModel):
    title = models.CharField(_('protocol'), max_length=50, default='BLANK TITLE')  
    description = models.CharField(_('Description'), max_length=500, default='', null=True, blank=True)
    delete_reason = models.CharField(_('Delete reason'), max_length=500, default='', null=True, blank=True)
    destination_ip = models.GenericIPAddressField(_('Destination IP'))
    port = models.PositiveIntegerField(_('Port'))
    protocol = models.CharField(_('protocol'), max_length=50, default='')
    ip_version = models.CharField(_('IP Version'), max_length=50, default='')
    soft_delete = models.BooleanField(_('Soft Delete'), default=False)        

    class Meta:
        db_table = 'alert_summaries'


# Alerts reported by nodes.
class Alerts (BaseModel):
    node = models.ForeignKey(Node, on_delete=models.DO_NOTHING, related_name='node', null=True, blank=True )
    summary = models.ForeignKey(AlertSummaries, on_delete=models.DO_NOTHING, related_name='alert_summaries', null=True, blank=True)   
    level =  models.CharField(_('Alert Level'), default='low', max_length=15, choices=ALERT_LEVELS)     
    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    destination_ip = models.GenericIPAddressField(_('Destination IP'))
    port = models.PositiveIntegerField(_('Port'))
    protocol = models.CharField(_('protocol'), max_length=50, default='')
    icmp_type = models.IntegerField(_('ICMP Type'), default=0)
    ip_version = models.CharField(_('IP Version'), max_length=50, default='')
    descr = models.CharField(_('Description'), max_length=500, default='', null=True, blank=True)
    soft_delete = models.BooleanField(_('Soft Delete'), default=False)

    class Meta:
        db_table = 'alerts'
        
    def rollup(self):
        roll_up_window = 25 # minutes
        
        total_alerts_count = Alerts.objects.count()
        
        if total_alerts_count == 0:
            self.save()
            return
        
        this_time = self.time_stamp
        
        last_alert = Alerts.objects.filter().last()
        last_time =  last_alert.time_stamp
        
        time_diff_in_seconds = (this_time - last_time).total_seconds()
        time_diff_in_minutes = time_diff_in_seconds // 60  
        
        self.save()      
        
        if time_diff_in_minutes < roll_up_window:
          # this alert is within the rollup window so assign this alert to the current summary
            if last_alert.summary is None:
                # the previous alert has not been assigned to a summary so do that here
                the_summary = AlertSummaries(
                                 title = " Roll These Up",
                                 destination_ip = self.destination_ip ,
                                 port = self.port ,
                                 protocol = self.protocol
                                 )   
                                 
                the_summary.save() 
                last_alert.summary = the_summary
                last_alert.save()              
                
            # assign this alert to the current summary alert
            the_summary = AlertSummaries.objects.get(id = last_alert.summary.id)
            self.summary = the_summary
            self.save()
 
        return


class IPAlertEvent (BaseModel):
    node = models.ForeignKey(Node, on_delete=models.DO_NOTHING, related_name='ae_node', null=True, blank=True )
    event = models.CharField(_('Raw Event Data'), max_length=1000, null=True)
    event_flag = models.CharField(_('Event Logging Flag'), max_length=30, null=True)

    # Top level event structure
    event_dt = models.DateTimeField(_('Event Time Stamp'), null=True)
    tz_offset = models.CharField(_('Time Zone Offset from UTC'), max_length=10, null=True)
    iface_in = models.CharField(_('Interface In'), max_length=50, null=True)
    iface_out = models.CharField(_('Interface Out'),  max_length=50, null=True)
    src_addr = models.GenericIPAddressField(_('Source Address'), null=True)
    dest_addr = models.GenericIPAddressField(_('Destination Address'), null=True)
    length = models.IntegerField(_('Length'), null=True)
    tos = models.CharField(_('Type Of Service'), max_length=10, null=True)
    prec = models.CharField(_('Precedence'), max_length=10, null=True)
    ttl = models.IntegerField(_('Time To Live'), null=True)
    packet_id = models.IntegerField(_('Packet ID'), null=True)
    frag_flags = models.CharField(_('Fragment Flags'),  max_length=50, null=True)
    protocol = models.CharField(_('Packet Protocol'),  max_length=10, null=True)

    # Event values based on protocol value.
    # TCP and UDP
    src_port = models.IntegerField(_('Source Port'), null=True)
    dest_port = models.IntegerField(_('Destination Port'), null=True)

    # TCP only
    window = models.IntegerField(_('Length of TCP Window'), null=True)
    reserved = models.CharField(_('Reserved Bits'), max_length=10, null=True)
    urgp = models.IntegerField(_('Urgent Pointer'), null=True)
    tcp_flags = models.CharField(_('TCP Flags'),  max_length=50, null=True)

    # UDP only
    udp_length = models.IntegerField(_('UDP Packet Length'), default=0)

    # ICMP
    icmp_type = models.IntegerField(_('ICMP Type'), default=0)
    icmp_code = models.IntegerField(_('ICMP Code'), default=0)
    icmp_id = models.IntegerField(_('ICMP ID'), default=0)
    icmp_seq = models.IntegerField(_('ICMP Sequence'), default=0)
    #icmp_error_header = models.BooleanField(_('Additional Event Information'), default=False)

    leftover = models.CharField(_('Unprocessed Event Data'),  max_length=500, null=True)

    # Parent event record pk when icmp_error_header is true in the parent record.
    parent_id = models.IntegerField(_('Parent Event ID'), null=True)

    class Meta:
        db_table = 'iptables_alert_event'
