#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT plugin for Delayed Delivery (XEP-0334)
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

from sat.core import exceptions

from wokkel import disco, iwokkel
try:
    from twisted.words.protocols.xmlstream import XMPPHandler
except ImportError:
    from wokkel.subprotocols import XMPPHandler
from twisted.python import failure
from zope.interface import implements


NS_MPH = 'urn:xmpp:hints'

PLUGIN_INFO = {
    "name": "Message Processing Hints",
    "import_name": "XEP-0334",
    "type": "XEP",
    "protocols": ["XEP-0334"],
    "main": "XEP_0334",
    "handler": "yes",
    "description": _("""Implementation of Message Processing Hints""")
}


class XEP_0334(object):

    def __init__(self, host):
        log.info(_("Message Processing Hints plugin initialization"))
        self.host = host
        host.trigger.add("sendMessage", self.sendMessageTrigger)
        host.trigger.add("MessageReceived", self.messageReceivedTrigger)

    def getHandler(self, profile):
        return XEP_0334_handler(self, profile)

    def sendMessageTrigger(self, mess_data, pre_xml_treatments, post_xml_treatments, profile):
        """Add the hints element to the message to be sent"""
        hints = []
        for key in ('no-permanent-storage', 'no-storage', 'no-copy'):
            if mess_data['extra'].get(key, None):
                hints.append(key)

        def treatment(mess_data):
            message = mess_data['xml']
            for key in hints:
                message.addElement((NS_MPH, key))
                if key in ('no-permanent-storage', 'no-storage'):
                    mess_data['extra']['no_storage'] = True
                    # TODO: the core doesn't process this 'no_storage' info yet
                    # it will be added after the frontends refactorization
            return mess_data

        if hints:
            post_xml_treatments.addCallback(treatment)
        return True

    def messageReceivedTrigger(self, message, post_treat, profile):
        """Check for hints in the received message"""
        hints = []
        for key in ('no-permanent-storage', 'no-storage'):
            try:
                message.elements(uri=NS_MPH, name=key).next()
                hints.append(key)
            except StopIteration:
                pass

        def post_treat_hints(data):
            raise failure.Failure(exceptions.SkipHistory())

        if hints:
            post_treat.addCallback(post_treat_hints)
        return True


class XEP_0334_handler(XMPPHandler):
    implements(iwokkel.IDisco)

    def __init__(self, plugin_parent, profile):
        self.plugin_parent = plugin_parent
        self.host = plugin_parent.host
        self.profile = profile

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        return [disco.DiscoFeature(NS_MPH)]

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        return []
