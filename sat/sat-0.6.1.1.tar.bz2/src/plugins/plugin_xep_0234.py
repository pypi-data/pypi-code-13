#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT plugin for Jingle File Transfer (XEP-0234)
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
from sat.core.constants import Const as C
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.core import exceptions
from wokkel import disco, iwokkel
from zope.interface import implements
from sat.tools import utils
import os.path
from twisted.words.xish import domish
from twisted.words.protocols.jabber import jid
from twisted.python import failure
from twisted.words.protocols.jabber.xmlstream import XMPPHandler
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import error as internet_error


NS_JINGLE_FT = 'urn:xmpp:jingle:apps:file-transfer:4'

PLUGIN_INFO = {
    "name": "Jingle File Transfer",
    "import_name": "XEP-0234",
    "type": "XEP",
    "protocols": ["XEP-0234"],
    "dependencies": ["XEP-0166", "XEP-0300", "FILE"],
    "main": "XEP_0234",
    "handler": "yes",
    "description": _("""Implementation of Jingle File Transfer""")
}


class XEP_0234(object):
    # TODO: assure everything is closed when file is sent or session terminate is received
    # TODO: call self._f.unregister when unloading order will be managing (i.e. when dependencies will be unloaded at the end)

    def __init__(self, host):
        log.info(_("plugin Jingle File Transfer initialization"))
        self.host = host
        self._j = host.plugins["XEP-0166"] # shortcut to access jingle
        self._j.registerApplication(NS_JINGLE_FT, self)
        self._f = host.plugins["FILE"]
        self._f.register(NS_JINGLE_FT, self.fileJingleSend, priority = 10000, method_name=u"Jingle")
        self._hash = self.host.plugins["XEP-0300"]
        host.bridge.addMethod("fileJingleSend", ".plugin", in_sign='sssss', out_sign='', method=self._fileJingleSend)

    def getHandler(self, profile):
        return XEP_0234_handler()

    def _getProgressId(self, session, content_name):
        """Return a unique progress ID

        @param session(dict): jingle session
        @param content_name(unicode): name of the content
        @return (unicode): unique progress id
        """
        return u'{}_{}'.format(session['id'], content_name)

    def _fileJingleSend(self, peer_jid, filepath, name="", file_desc="", profile=C.PROF_KEY_NONE):
        return self.fileJingleSend(jid.JID(peer_jid), filepath, name or None, file_desc or None, profile)

    def fileJingleSend(self, peer_jid, filepath, name, file_desc=None, profile=C.PROF_KEY_NONE):
        """Send a file using jingle file transfer

        @param peer_jid(jid.JID): destinee jid
        @param filepath(str): absolute path of the file
        @param name(unicode, None): name of the file
        @param file_desc(unicode, None): description of the file
        @param profile: %(doc_profile)s
        @return (D(unicode)): progress id
        """
        progress_id_d = defer.Deferred()
        self._j.initiate(peer_jid,
                         [{'app_ns': NS_JINGLE_FT,
                           'senders': self._j.ROLE_INITIATOR,
                           'app_kwargs': {'filepath': filepath,
                                          'name': name,
                                          'file_desc': file_desc,
                                          'progress_id_d': progress_id_d},
                         }],
                         profile=profile)
        return progress_id_d

    # jingle callbacks

    def jingleSessionInit(self, session, content_name, filepath, name, file_desc, progress_id_d, profile=C.PROF_KEY_NONE):
        progress_id_d.callback(self._getProgressId(session, content_name))
        content_data = session['contents'][content_name]
        application_data = content_data['application_data']
        assert 'file_path' not in application_data
        application_data['file_path'] = filepath
        file_data = application_data['file_data'] = {}
        file_data['date'] = utils.xmpp_date()
        file_data['desc'] = file_desc or ''
        file_data['media-type'] = "application/octet-stream" # TODO
        file_data['name'] = os.path.basename(filepath) if name is None else name
        file_data['size'] = os.path.getsize(filepath)
        desc_elt = domish.Element((NS_JINGLE_FT, 'description'))
        file_elt = desc_elt.addElement("file")
        for name in ('date', 'desc', 'media-type', 'name', 'size'):
            file_elt.addElement(name, content=unicode(file_data[name]))
        file_elt.addElement("range") # TODO
        file_elt.addChild(self._hash.buildHashElt())
        return desc_elt

    def jingleRequestConfirmation(self, action, session, content_name, desc_elt, profile):
        """This method request confirmation for a jingle session"""
        content_data = session['contents'][content_name]
        if content_data['senders'] not in (self._j.ROLE_INITIATOR, self._j.ROLE_RESPONDER):
            log.warning(u"Bad sender, assuming initiator")
            content_data['senders'] = self._j.ROLE_INITIATOR
        # first we grab file informations
        try:
            file_elt = desc_elt.elements(NS_JINGLE_FT, 'file').next()
        except StopIteration:
            raise failure.Failure(exceptions.DataError)
        file_data = {'progress_id': self._getProgressId(session, content_name)}
        for name in ('date', 'desc', 'media-type', 'name', 'range', 'size'):
            try:
                file_data[name] = unicode(file_elt.elements(NS_JINGLE_FT, name).next())
            except StopIteration:
                file_data[name] = ''

        try:
            hash_algo, file_data['hash_given'] = self._hash.parseHashElt(file_elt)
        except exceptions.NotFound:
            raise failure.Failure(exceptions.DataError)

        if hash_algo is not None:
            file_data['hash_algo'] = hash_algo
            file_data['hash_hasher'] = hasher = self._hash.getHasher(hash_algo)
            file_data['data_cb'] = lambda data: hasher.update(data)

        try:
            file_data['size'] = int(file_data['size'])
        except ValueError:
            raise failure.Failure(exceptions.DataError)

        name = file_data['name']
        if '/' in name or '\\' in name:
            log.warning(u"File name contain path characters, we replace them: {}".format(name))
            file_data['name'] = name.replace('/', '_').replace('\\', '_')

        content_data['application_data']['file_data'] = file_data

        # now we actualy request permission to user
        def gotConfirmation(confirmed):
            if confirmed:
                finished_d = content_data['finished_d'] = defer.Deferred()
                args = [session, content_name, content_data, profile]
                finished_d.addCallbacks(self._finishedCb, self._finishedEb, args, None, args)
            return confirmed

        d = self._f.getDestDir(session['peer_jid'], content_data, file_data, profile)
        d.addCallback(gotConfirmation)
        return d

    def jingleHandler(self, action, session, content_name, desc_elt, profile):
        content_data = session['contents'][content_name]
        application_data = content_data['application_data']
        if action in (self._j.A_ACCEPTED_ACK,):
            pass
        elif action == self._j.A_SESSION_INITIATE:
            file_elt = desc_elt.elements(NS_JINGLE_FT, 'file').next()
            try:
                file_elt.elements(NS_JINGLE_FT, 'range').next()
            except StopIteration:
                # initiator doesn't manage <range>, but we do so we advertise it
                log.debug("adding <range> element")
                file_elt.addElement('range')
        elif action == self._j.A_SESSION_ACCEPT:
            assert not 'file_obj' in content_data
            file_data = application_data['file_data']
            file_path = application_data['file_path']
            size = file_data['size']
            # XXX: hash security is not critical here, so we just take the higher mandatory one
            hasher = file_data['hash_hasher'] = self._hash.getHasher('sha-256')
            content_data['file_obj'] = self._f.File(self.host,
                                       file_path,
                                       uid=self._getProgressId(session, content_name),
                                       size=size,
                                       data_cb=lambda data: hasher.update(data),
                                       profile=profile
                                       )
            finished_d = content_data['finished_d'] = defer.Deferred()
            args = [session, content_name, content_data, profile]
            finished_d.addCallbacks(self._finishedCb, self._finishedEb, args, None, args)
        else:
            log.warning(u"FIXME: unmanaged action {}".format(action))
        return desc_elt

    def jingleSessionInfo(self, action, session, content_name, jingle_elt, profile):
        """Called on session-info action

        manage checksum, and ignore <received/> element
        """
        # TODO: manage <received/> element
        content_data = session['contents'][content_name]
        elts = [elt for elt in jingle_elt.elements() if elt.uri == NS_JINGLE_FT]
        if not elts:
            return
        for elt in elts:
            if elt.name == 'received':
                pass
            elif elt.name == 'checksum':
                # we have received the file hash, we need to parse it
                if content_data['senders'] == session['role']:
                    log.warning(u"unexpected checksum received while we are the file sender")
                    raise exceptions.DataError
                info_content_name = elt['name']
                if info_content_name != content_name:
                    # it was for an other content...
                    return
                file_data = content_data['application_data']['file_data']
                try:
                    file_elt = elt.elements((NS_JINGLE_FT, 'file')).next()
                except StopIteration:
                    raise exceptions.DataError
                algo, file_data['hash_given'] = self._hash.parseHashElt(file_elt)
                if algo != file_data.get('hash_algo'):
                    log.warning(u"Hash algorithm used in given hash ({peer_algo}) doesn't correspond to the one we have used ({our_algo})"
                        .format(peer_algo=algo, our_algo=file_data.get('hash_algo')))
                else:
                    self._receiverTryTerminate(session, content_name, content_data, profile=profile)
            else:
                raise NotImplementedError

    def _sendCheckSum(self, session, content_name, content_data, profile):
        """Send the session-info with the hash checksum"""
        file_data = content_data['application_data']['file_data']
        hasher = file_data['hash_hasher']
        hash_ = hasher.hexdigest()
        log.debug(u"Calculated hash: {}".format(hash_))
        iq_elt, jingle_elt = self._j.buildSessionInfo(session, profile)
        checksum_elt = jingle_elt.addElement((NS_JINGLE_FT, 'checksum'))
        checksum_elt['creator'] = content_data['creator']
        checksum_elt['name'] = content_name
        file_elt = checksum_elt.addElement('file')
        file_elt.addChild(self._hash.buildHashElt(hash_))
        iq_elt.send()

    def _receiverTryTerminate(self, session, content_name, content_data, last_try=False, profile=C.PROF_KEY_NONE):
        """Try to terminate the session

        This method must only be used by the receiver.
        It check if transfer is finished, and hash available,
        if everything is OK, it check hash and terminate the session
        @param last_try(bool): if True this mean than session must be terminated even given hash is not available
        @return (bool): True if session was terminated
        """
        if not content_data.get('transfer_finished', False):
            return False
        file_data = content_data['application_data']['file_data']
        hash_given = file_data.get('hash_given')
        if hash_given is None:
            if last_try:
                log.warning(u"sender didn't sent hash checksum, we can't check the file")
                self._j.delayedContentTerminate(session, content_name, profile=profile)
                content_data['file_obj'].close()
                return True
            return False
        hasher = file_data['hash_hasher']
        hash_ = hasher.hexdigest()

        if hash_ == hash_given:
            log.info(u"Hash checked, file was successfully transfered: {}".format(hash_))
            progress_metadata = {'hash': hash_,
                                 'hash_algo': file_data['hash_algo'],
                                 'hash_verified': C.BOOL_TRUE
                                }
            error = None
        else:
            log.warning(u"Hash mismatch, the file was not transfered correctly")
            progress_metadata=None
            error = u"Hash mismatch: given={algo}:{given}, calculated={algo}:{our}".format(
                algo = file_data['hash_algo'],
                given = hash_given,
                our = hash_)

        self._j.delayedContentTerminate(session, content_name, profile=profile)
        content_data['file_obj'].close(progress_metadata, error)
        # we may have the last_try timer still active, so we try to cancel it
        try:
            content_data['last_try_timer'].cancel()
        except (KeyError, internet_error.AlreadyCalled):
            pass
        return True

    def _finishedCb(self, dummy, session, content_name, content_data, profile):
        log.info(u"File transfer terminated")
        if content_data['senders'] != session['role']:
            # we terminate the session only if we are the receiver,
            # as recommanded in XEP-0234 §2 (after example 6)
            content_data['transfer_finished'] = True
            if not self._receiverTryTerminate(session, content_name, content_data, profile=profile):
                # we have not received the hash yet, we wait 5 more seconds
                content_data['last_try_timer'] = reactor.callLater(
                    5, self._receiverTryTerminate, session, content_name, content_data, last_try=True, profile=profile)
        else:
            # we are the sender, we send the checksum
            self._sendCheckSum(session, content_name, content_data, profile)
            content_data['file_obj'].close()

    def _finishedEb(self, failure, session, content_name, content_data, profile):
        log.warning(u"Error while streaming file: {}".format(failure))
        content_data['file_obj'].close()
        self._j.contentTerminate(session, content_name, reason=self._j.REASON_FAILED_TRANSPORT, profile=profile)


class XEP_0234_handler(XMPPHandler):
    implements(iwokkel.IDisco)

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        return [disco.DiscoFeature(NS_JINGLE_FT)]

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        return []
