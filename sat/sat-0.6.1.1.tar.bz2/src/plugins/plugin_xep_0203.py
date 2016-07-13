#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT plugin for Delayed Delivery (XEP-0203)
# Copyright (C) 2009-2016 Jérôme Poisson (goffi@goffi.org)
# Copyright (C) 2013-2016 Adrien Cossa (souliane@mailoo.org)

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

from sat.core.i18n import _
from sat.core.log import getLogger
log = getLogger(__name__)

from calendar import timegm
from wokkel import disco, iwokkel, delay
try:
    from twisted.words.protocols.xmlstream import XMPPHandler
except ImportError:
    from wokkel.subprotocols import XMPPHandler
from zope.interface import implements


NS_DD = 'urn:xmpp:delay'

PLUGIN_INFO = {
    "name": "Delayed Delivery",
    "import_name": "XEP-0203",
    "type": "XEP",
    "protocols": ["XEP-0203"],
    "main": "XEP_0203",
    "handler": "yes",
    "description": _("""Implementation of Delayed Delivery""")
}


class XEP_0203(object):

    def __init__(self, host):
        log.info(_("Delayed Delivery plugin initialization"))
        self.host = host
        host.trigger.add("MessageReceived", self.messageReceivedTrigger)


    def getHandler(self, profile):
        return XEP_0203_handler(self, profile)

    def delay(self, stamp, sender=None, desc='', parent=None):
        """Build a delay element, eventually append it to the given parent element.

        @param stamp (datetime): offset-aware timestamp of the original sending.
        @param sender (JID): entity that originally sent or delayed the message.
        @param desc (unicode): optional natural language description.
        @param parent (domish.Element): add the delay element to this element.
        @return: the delay element (domish.Element)
        """
        elt = delay.Delay(stamp, sender).toElement()
        if desc:
            elt.addContent(desc)
        if parent:
            parent.addChild(elt)
        return elt

    def messagePostTreat(self, data, timestamp):
        """Set the timestamp of a received message.

        @param data (dict): data send by MessageReceived trigger through post_treat deferred
        @param timestamp (int): original timestamp of a delayed message
        @return: dict
        """
        data['extra']['timestamp'] = unicode(timestamp)
        return data

    def messageReceivedTrigger(self, message, post_treat, profile):
        """Process a delay element from incoming message.

        @param message (domish.Element): message element
        @param post_treat (Deferred): deferred instance to add post treatments
        """
        try:
            delay_ = delay.Delay.fromElement([elm for elm in message.elements() if elm.name == 'delay'][0])
        except IndexError:
            return True
        else:
            timestamp = timegm(delay_.stamp.utctimetuple())
            post_treat.addCallback(self.messagePostTreat, timestamp)
        return True

class XEP_0203_handler(XMPPHandler):
    implements(iwokkel.IDisco)

    def __init__(self, plugin_parent, profile):
        self.plugin_parent = plugin_parent
        self.host = plugin_parent.host
        self.profile = profile

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        return [disco.DiscoFeature(NS_DD)]

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        return []
