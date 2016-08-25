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

# The Models created here should apply to all firewall applications

from django.utils.translation import ugettext_lazy as _
from django.db import models
from proj.models import BaseModel


# List of firewall platforms supported by this app
RULE_PLATFORMS = (
    ('iptables', 'IPTables'),
)

RULE_MACHINE_SUBSET_SLOTS = (
    (110, _('Administration')),
    # (120, _('Silent Dune Server')),
    (130, _('Dynamic Name Service')),
    (140, _('Network Time Protocol')),
    (150, _('System Update')),
    (160, _('Identity Services')),
    #(1000, _('Node Custom Rules')),
    (2000, _('User Defined')),  # 2000 -> 8999 are for user defined rules.
    #(9000, _('Reserved')),
    (9800, _('Logging Rules')),
    (9900, _('Rejection Rules'))
)


class AbstractMachineSubset (BaseModel):

    name = models.CharField(_('Chain Set Name'), max_length=50)
    descr = models.CharField(_('Description'), max_length=500, default='', null=True, blank=True)
    notes = models.CharField(_('Notes'), max_length=4000, default='', null=True, blank=True)
    slot = models.SmallIntegerField(_('Chain Set Slot'), choices=RULE_MACHINE_SUBSET_SLOTS)
    sort_id = models.SmallIntegerField(_('Sort ID'), null=True, blank=True)
    active = models.BooleanField(_('Active'), default=False)

    class Meta:
        abstract = True


# A Bundle record is what a Node is linked to.
class Bundle (BaseModel):

    platform = models.CharField(_('Firewall Platform'), max_length=30, choices=RULE_PLATFORMS)
    name = models.CharField(_('Chain Set Name'), max_length=50)

    descr = models.CharField(_('Description'), max_length=500, default='', null=True, blank=True)
    notes = models.CharField(_('Notes'), max_length=4000, default='', null=True, blank=True)

    default = models.BooleanField(_('Default Bundle'), default=False, blank=True)

    class Meta:
        db_table = 'rule_bundle'


# The Bundle Set is where the generic rule tables link up with a specific platform
# Chain Set.
class AbstractMachineSet (BaseModel):

    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, related_name='bundle')

    class Meta:
        abstract = True
