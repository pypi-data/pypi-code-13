#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT plugin for Jingle (XEP-0261)
# Copyright (C) 2009-2016 Jérôme Poisson (goffi@goffi.org)

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
from wokkel import disco, iwokkel
from zope.interface import implements
from twisted.words.xish import domish
import uuid

try:
    from twisted.words.protocols.xmlstream import XMPPHandler
except ImportError:
    from wokkel.subprotocols import XMPPHandler


NS_JINGLE_IBB = 'urn:xmpp:jingle:transports:ibb:1'

PLUGIN_INFO = {
    "name": "Jingle In-Band Bytestreams",
    "import_name": "XEP-0261",
    "type": "XEP",
    "protocols": ["XEP-0261"],
    "dependencies": ["XEP-0166", "XEP-0047"],
    "main": "XEP_0261",
    "handler": "yes",
    "description": _("""Implementation of Jingle In-Band Bytestreams""")
}


class XEP_0261(object):
    NAMESPACE = NS_JINGLE_IBB # used by XEP-0260 plugin for transport-replace

    def __init__(self, host):
        log.info(_("plugin Jingle In-Band Bytestreams"))
        self.host = host
        self._j = host.plugins["XEP-0166"] # shortcut to access jingle
        self._ibb = host.plugins["XEP-0047"] # and in-band bytestream
        self._j.registerTransport(NS_JINGLE_IBB, self._j.TRANSPORT_STREAMING, self, -10000) # must be the lowest priority

    def getHandler(self, profile):
        return XEP_0261_handler()

    def jingleSessionInit(self, session, content_name, profile):
        transport_elt = domish.Element((NS_JINGLE_IBB, "transport"))
        content_data = session['contents'][content_name]
        transport_data = content_data['transport_data']
        transport_data['block_size'] = self._ibb.BLOCK_SIZE
        transport_elt['block-size'] = unicode(transport_data['block_size'])
        transport_elt['sid'] = transport_data['sid'] = unicode(uuid.uuid4())
        return transport_elt

    def jingleHandler(self, action, session, content_name, transport_elt, profile):
        content_data = session['contents'][content_name]
        transport_data = content_data['transport_data']
        if action in (self._j.A_SESSION_ACCEPT,
                      self._j.A_ACCEPTED_ACK,
                      self._j.A_TRANSPORT_ACCEPT):
            pass
        elif action in (self._j.A_SESSION_INITIATE, self._j.A_TRANSPORT_REPLACE):
            transport_data['sid'] = transport_elt['sid']
        elif action in (self._j.A_START, self._j.A_PREPARE_RESPONDER):
            peer_jid = session['peer_jid']
            sid = transport_data['sid']
            file_obj = content_data['file_obj']
            if action == self._j.A_START:
                block_size = transport_data['block_size']
                d = self._ibb.startStream(file_obj, peer_jid, sid, block_size, profile)
                d.chainDeferred(content_data['finished_d'])
            else:
                d = self._ibb.createSession(file_obj, peer_jid, sid, profile)
                d.chainDeferred(content_data['finished_d'])
        else:
            log.warning(u"FIXME: unmanaged action {}".format(action))
        return transport_elt


class XEP_0261_handler(XMPPHandler):
    implements(iwokkel.IDisco)

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        return [disco.DiscoFeature(NS_JINGLE_IBB)]

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        return []
