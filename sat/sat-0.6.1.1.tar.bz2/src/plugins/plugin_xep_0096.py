#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT plugin for managing xep-0096
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
from twisted.words.xish import domish
from twisted.words.protocols.jabber import jid
from twisted.words.protocols.jabber import error
import os


NS_SI_FT = "http://jabber.org/protocol/si/profile/file-transfer"
IQ_SET = '/iq[@type="set"]'
SI_PROFILE_NAME = "file-transfer"
SI_PROFILE = "http://jabber.org/protocol/si/profile/" + SI_PROFILE_NAME

PLUGIN_INFO = {
    "name": "XEP-0096 Plugin",
    "import_name": "XEP-0096",
    "type": "XEP",
    "protocols": ["XEP-0096"],
    "dependencies": ["XEP-0020", "XEP-0095", "XEP-0065", "XEP-0047", "FILE"],
    "main": "XEP_0096",
    "handler": "no",
    "description": _("""Implementation of SI File Transfer""")
}


class XEP_0096(object):
    # TODO: call self._f.unregister when unloading order will be managing (i.e. when depenencies will be unloaded at the end)

    def __init__(self, host):
        log.info(_("Plugin XEP_0096 initialization"))
        self.host = host
        self.managed_stream_m = [self.host.plugins["XEP-0065"].NAMESPACE,
                                 self.host.plugins["XEP-0047"].NAMESPACE]  # Stream methods managed
        self._f = self.host.plugins["FILE"]
        self._f.register(NS_SI_FT, self.sendFile, priority=0, method_name=u"Stream Initiation")
        self._si = self.host.plugins["XEP-0095"]
        self._si.registerSIProfile(SI_PROFILE_NAME, self._transferRequest)
        host.bridge.addMethod("siSendFile", ".plugin", in_sign='sssss', out_sign='s', method=self._sendFile)

    def unload(self):
        self._si.unregisterSIProfile(SI_PROFILE_NAME)

    def _badRequest(self, iq_elt, message=None, profile=C.PROF_KEY_NONE):
        """Send a bad-request error

        @param iq_elt(domish.Element): initial <IQ> element of the SI request
        @param message(None, unicode): informational message to display in the logs
        @param profile: %(doc_profile)s
        """
        if message is not None:
            log.warning(message)
        self._si.sendError(iq_elt, 'bad-request', profile)

    def _parseRange(self, parent_elt, file_size):
        """find and parse <range/> element

        @param parent_elt(domish.Element): direct parent of the <range/> element
        @return (tuple[bool, int, int]): a tuple with
            - True if range is required
            - range_offset
            - range_length
        """
        try:
            range_elt = parent_elt.elements(NS_SI_FT, 'range').next()
        except StopIteration:
            range_ = False
            range_offset = None
            range_length = None
        else:
            range_ = True

            try:
                range_offset = int(range_elt['offset'])
            except KeyError:
                range_offset = 0

            try:
                range_length = int(range_elt['length'])
            except KeyError:
                range_length = file_size

            if range_offset != 0 or range_length != file_size:
                raise NotImplementedError # FIXME

        return range_, range_offset, range_length

    def _transferRequest(self, iq_elt, si_id, si_mime_type, si_elt, profile):
        """Called when a file transfer is requested

        @param iq_elt(domish.Element): initial <IQ> element of the SI request
        @param si_id(unicode): Stream Initiation session id
        @param si_mime_type("unicode"): Mime type of the file (or default "application/octet-stream" if unknown)
        @param si_elt(domish.Element): request
        @param profile: %(doc_profile)s
        """
        log.info(_("XEP-0096 file transfer requested"))
        peer_jid = jid.JID(iq_elt['from'])

        try:
            file_elt = si_elt.elements(NS_SI_FT, "file").next()
        except StopIteration:
            return self._badRequest(iq_elt, "No <file/> element found in SI File Transfer request", profile)

        try:
            feature_elt = self.host.plugins["XEP-0020"].getFeatureElt(si_elt)
        except exceptions.NotFound:
            return self._badRequest(iq_elt, "No <feature/> element found in SI File Transfer request", profile)

        try:
            filename = file_elt["name"]
            file_size = int(file_elt["size"])
        except (KeyError, ValueError):
            return self._badRequest(iq_elt, "Malformed SI File Transfer request", profile)

        file_date = file_elt.getAttribute("date")
        file_hash = file_elt.getAttribute("hash")

        log.info(u"File proposed: name=[{name}] size={size}".format(name=filename, size=file_size))

        try:
            file_desc = unicode(file_elt.elements(NS_SI_FT, 'desc').next())
        except StopIteration:
            file_desc = ''

        try:
            range_, range_offset, range_length = self._parseRange(file_elt, file_size)
        except ValueError:
            return self._badRequest(iq_elt, "Malformed SI File Transfer request", profile)

        try:
            stream_method = self.host.plugins["XEP-0020"].negotiate(feature_elt, 'stream-method', self.managed_stream_m, namespace=None)
        except KeyError:
            return self._badRequest(iq_elt, "No stream method found", profile)

        if stream_method:
            if stream_method == self.host.plugins["XEP-0065"].NAMESPACE:
                plugin = self.host.plugins["XEP-0065"]
            elif stream_method == self.host.plugins["XEP-0047"].NAMESPACE:
                plugin = self.host.plugins["XEP-0047"]
            else:
                log.error(u"Unknown stream method, this should not happen at this stage, cancelling transfer")
        else:
            log.warning(u"Can't find a valid stream method")
            self._si.sendError(iq_elt, 'not-acceptable', profile)
            return

        #if we are here, the transfer can start, we just need user's agreement
        data = {"name": filename, "peer_jid": peer_jid, "size": file_size, "date": file_date, "hash": file_hash, "desc": file_desc,
                "range": range_, "range_offset": range_offset, "range_length": range_length,
                "si_id": si_id, "progress_id": si_id, "stream_method": stream_method, "stream_plugin": plugin}

        d = self._f.getDestDir(peer_jid, data, data, profile)
        d.addCallback(self.confirmationCb, iq_elt, data, profile)

    def _getFileObject(self, dest_path, can_range=False):
        """Open file, put file pointer to the end if the file if needed
        @param dest_path: path of the destination file
        @param can_range: True if the file pointer can be moved
        @return: File Object"""
        return open(dest_path, "ab" if can_range else "wb")

    def confirmationCb(self, accepted, iq_elt, data, profile):
        """Called on confirmation answer

        @param accepted(bool): True if file transfer is accepted
        @param iq_elt(domish.Element): initial SI request
        @param data(dict): session data
        @param profile: %(doc_profile)s
        """
        if not accepted:
            log.info(u"File transfer declined")
            self._si.sendError(iq_elt, 'forbidden', profile)
            return
        # data, timeout, stream_method, failed_methods = client._xep_0096_waiting_for_approval[sid]
        # can_range = data['can_range'] == "True"
        # range_offset = 0
        # if timeout.active():
        #     timeout.cancel()
        # try:
        #     dest_path = frontend_data['dest_path']
        # except KeyError:
        #     log.error(_('dest path not found in frontend_data'))
        #     del client._xep_0096_waiting_for_approval[sid]
        #     return
        # if stream_method == self.host.plugins["XEP-0065"].NAMESPACE:
        #     plugin = self.host.plugins["XEP-0065"]
        # elif stream_method == self.host.plugins["XEP-0047"].NAMESPACE:
        #     plugin = self.host.plugins["XEP-0047"]
        # else:
        #     log.error(_("Unknown stream method, this should not happen at this stage, cancelling transfer"))
        #     del client._xep_0096_waiting_for_approval[sid]
        #     return

        # file_obj = self._getFileObject(dest_path, can_range)
        # range_offset = file_obj.tell()
        d = data['stream_plugin'].createSession(data['file_obj'], data['peer_jid'], data['si_id'], profile=profile)
        d.addCallback(self._transferCb, data, profile)
        d.addErrback(self._transferEb, data, profile)

        #we can send the iq result
        feature_elt = self.host.plugins["XEP-0020"].chooseOption({'stream-method': data['stream_method']}, namespace=None)
        misc_elts = []
        misc_elts.append(domish.Element((SI_PROFILE, "file")))
        # if can_range:
        #     range_elt = domish.Element((None, "range"))
        #     range_elt['offset'] = str(range_offset)
        #     #TODO: manage range length
        #     misc_elts.append(range_elt)
        self._si.acceptStream(iq_elt, feature_elt, misc_elts, profile)

    def _transferCb(self, dummy, data, profile):
        """Called by the stream method when transfer successfuly finished

        @param data: session data
        @param profile: %(doc_profile)s
        """
        #TODO: check hash
        data['file_obj'].close()
        log.info(u'Transfer {si_id} successfuly finished'.format(**data))

    def _transferEb(self, failure, data, profile):
        """Called when something went wrong with the transfer

        @param id: stream id
        @param data: session data
        @param profile: %(doc_profile)s
        """
        log.warning(u'Transfer {si_id} failed: {reason}'.format(reason=unicode(failure.value), **data))
        data['file_obj'].close()

    def _sendFile(self, peer_jid_s, filepath, name, desc, profile=C.PROF_KEY_NONE):
        return self.sendFile(jid.JID(peer_jid_s), filepath, name or None, desc or None, profile)

    def sendFile(self, peer_jid, filepath, name=None, desc=None, profile=C.PROF_KEY_NONE):
        """Send a file using XEP-0096

        @param peer_jid(jid.JID): recipient
        @param filepath(str): absolute path to the file to send
        @param name(unicode): name of the file to send
            name must not contain "/" characters
        @param desc: description of the file
        @param profile: %(doc_profile)s
        @return: an unique id to identify the transfer
        """
        client = self.host.getClient(profile)
        feature_elt = self.host.plugins["XEP-0020"].proposeFeatures({'stream-method': self.managed_stream_m}, namespace=None)

        file_transfer_elts = []

        statinfo = os.stat(filepath)
        file_elt = domish.Element((SI_PROFILE, 'file'))
        file_elt['name'] = name or os.path.basename(filepath)
        assert '/' not in file_elt['name']
        size = statinfo.st_size
        file_elt['size'] = str(size)
        if desc:
            file_elt.addElement('desc', content=desc)
        file_transfer_elts.append(file_elt)

        file_transfer_elts.append(domish.Element((None, 'range')))

        sid, offer_d = self._si.proposeStream(peer_jid, SI_PROFILE, feature_elt, file_transfer_elts, profile=client.profile)
        args = [filepath, sid, size, client]
        offer_d.addCallbacks(self._fileCb, self._fileEb, args, None, args)
        return sid

    def _fileCb(self, result_tuple, filepath, sid, size, client):
        iq_elt, si_elt = result_tuple

        try:
            feature_elt = self.host.plugins["XEP-0020"].getFeatureElt(si_elt)
        except exceptions.NotFound:
            log.warning(u"No <feature/> element found in result while expected")
            return

        choosed_options = self.host.plugins["XEP-0020"].getChoosedOptions(feature_elt, namespace=None)
        try:
            stream_method = choosed_options["stream-method"]
        except KeyError:
            log.warning(u"No stream method choosed")
            return

        try:
            file_elt = si_elt.elements(NS_SI_FT, "file").next()
        except StopIteration:
            pass
        else:
            range_, range_offset, range_length = self._parseRange(file_elt, size)

        if stream_method == self.host.plugins["XEP-0065"].NAMESPACE:
            plugin = self.host.plugins["XEP-0065"]
        elif stream_method == self.host.plugins["XEP-0047"].NAMESPACE:
            plugin = self.host.plugins["XEP-0047"]
        else:
            log.warning(u"Invalid stream method received")
            return

        file_obj = self._f.File(self.host,
                                filepath,
                                uid=sid,
                                size=size,
                                profile=client.profile
                                )
        d = plugin.startStream(file_obj, jid.JID(iq_elt['from']), sid, profile=client.profile)
        d.addCallback(self._sendCb, sid, file_obj, client.profile)
        d.addErrback(self._sendEb, sid, file_obj, client.profile)

    def _fileEb(self, failure, filepath, sid, size, client):
        if failure.check(error.StanzaError):
            stanza_err = failure.value
            if stanza_err.code == '403' and stanza_err.condition == 'forbidden':
                from_s = stanza_err.stanza['from']
                log.info(u"File transfer refused by {}".format(from_s))
                self.host.bridge.newAlert(_("The contact {} has refused your file").format(from_s), _("File refused"), "INFO", client.profile)
            else:
                log.warning(_(u"Error during file transfer"))
                self.host.bridge.newAlert(_(u"Something went wrong during the file transfer session initialisation: {reason}").format(reason=unicode(stanza_err)), _("File transfer error"), "ERROR", client.profile)
        elif failure.check(exceptions.DataError):
            log.warning(u'Invalid stanza received')
        else:
            log.error(u'Error while proposing stream: {}'.format(failure))

    def _sendCb(self, dummy, sid, file_obj, profile):
        log.info(_(u'transfer {sid} successfuly finished [{profile}]').format(
            sid=sid,
            profile=profile))
        file_obj.close()

    def _sendEb(self, failure, sid, file_obj, profile):
        log.warning(_(u'transfer {sid} failed [{profile}]: {reason}').format(
            sid=sid,
            profile=profile,
            reason=unicode(failure.value),
            ))
        file_obj.close()
