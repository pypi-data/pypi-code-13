#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT plugin for file tansfer
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

from sat.core.i18n import _, D_
from sat.core.constants import Const as C
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.core import exceptions
from sat.tools import xml_tools
from twisted.internet import defer
from twisted.words.protocols.jabber import jid
import os
import os.path
import uuid


PLUGIN_INFO = {
    "name": "File Tansfer",
    "import_name": "FILE",
    "type": C.PLUG_TYPE_MISC,
    "main": "FilePlugin",
    "handler": "no",
    "description": _("""File Tansfer Management:
This plugin manage the various ways of sending a file, and choose the best one.""")
}


SENDING = D_(u'Please select a file to send to {peer}')
SENDING_TITLE = D_(u'File sending')
CONFIRM = D_(u'{peer} wants to send the file "{name}" to you:\n{desc}\n\nThe file has a size of {size_human}\n\nDo you accept ?')
CONFIRM_TITLE = D_(u'Confirm file transfer')
CONFIRM_OVERWRITE = D_(u'File {} already exists, are you sure you want to overwrite ?')
CONFIRM_OVERWRITE_TITLE = D_(u'File exists')
SECURITY_LIMIT = 30

PROGRESS_ID_KEY = 'progress_id'


class SatFile(object):
    """A file-like object to have high level files manipulation"""
    # TODO: manage "with" statement

    def __init__(self, host, path, mode='rb', uid=None, size=None, data_cb=None, auto_end_signals=True, profile=C.PROF_KEY_NONE):
        """
        @param host: %(doc_host)s
        @param path(str): path of the file to get
        @param mode(str): same as for built-in "open" function
        @param uid(unicode, None): unique id identifing this progressing element
            This uid will be used with self.host.progressGet
            will be automaticaly generated if None
        @param size(None, int): size of the file
        @param data_cb(None, callable): method to call on each data read/write
            mainly useful to do things like calculating hash
        @param auto_end_signals(bool): if True, progressFinished and progressError signals are automatically sent
            if False, you'll have to call self.progressFinished and self.progressError yourself
            progressStarted signal is always sent automatically
        """
        self.host = host
        self.uid = uid or unicode(uuid.uuid4())
        self._file = open(path, mode)
        self.size = size
        self.data_cb = data_cb
        self.profile = profile
        self.auto_end_signals = auto_end_signals
        metadata = self.getProgressMetadata()
        self.host.registerProgressCb(self.uid, self.getProgress, metadata, profile=profile)
        self.host.bridge.progressStarted(self.uid, metadata, self.profile)

    def checkSize(self):
        """Check that current size correspond to given size

        must be used when the transfer is supposed to be finished
        @return (bool): True if the position is the same as given size
        @raise exceptions.NotFound: size has not be specified
        """
        position = self._file.tell()
        if self.size is None:
            raise exceptions.NotFound
        return position == self.size


    def close(self, progress_metadata=None, error=None):
        """Close the current file

        @param progress_metadata(None, dict): metadata to send with _onProgressFinished message
        @param error(None, unicode): set to an error message if progress was not successful
            mutually exclusive with progress_metadata
            error can happen even if error is None, if current size differ from given size
        """
        if self._file.closed:
            return # avoid double close (which is allowed) error
        if error is None:
            try:
                size_ok = self.checkSize()
            except exceptions.NotFound:
                size_ok = True
            if not size_ok:
                error = u'declared and actual size mismatch'
                log.warning(error)
                progress_metadata = None

        self._file.close()

        if self.auto_end_signals:
            if error is None:
                self.progressFinished(progress_metadata)
            else:
                assert progress_metadata is None
                self.progressError(error)

        self.host.removeProgressCb(self.uid, self.profile)

    def progressFinished(self, metadata=None):
        if metadata is None:
            metadata = {}
        self.host.bridge.progressFinished(self.uid, metadata, self.profile)

    def progressError(self, error):
        self.host.bridge.progressError(self.uid, error, self.profile)

    def flush(self):
        self._file.flush()

    def write(self, buf):
        self._file.write(buf)
        if self.data_cb is not None:
            return self.data_cb(buf)

    def read(self, size=-1):
        read = self._file.read(size)
        if self.data_cb is not None and read:
            self.data_cb(read)
        return read

    def seek(self, offset, whence=os.SEEK_SET):
        self._file.seek(offset, whence)

    def tell(self):
        return self._file.tell()

    def mode(self):
        return self._file.mode()

    def getProgressMetadata(self):
        """Return progression metadata as given to progressStarted

        @return (dict): metadata (check bridge for documentation)
        """
        metadata = {'type': C.META_TYPE_FILE}

        mode = self._file.mode
        if '+' in mode:
            pass # we have no direction in read/write modes
        elif mode in ('r', 'rb'):
            metadata['direction'] = 'out'
        elif mode in ('w', 'wb'):
            metadata['direction'] = 'in'
        elif 'U' in mode:
            metadata['direction'] = 'out'
        else:
            raise exceptions.InternalError

        metadata['name'] = self._file.name

        return metadata

    def getProgress(self, progress_id, profile):
        ret = {'position': self._file.tell()}
        if self.size:
            ret['size'] = self.size
        return ret


class FilePlugin(object):
    File=SatFile

    def __init__(self, host):
        log.info(_("plugin File initialization"))
        self.host = host
        host.bridge.addMethod("fileSend", ".plugin", in_sign='sssss', out_sign='a{ss}', method=self._fileSend, async=True)
        self._file_callbacks = []
        host.importMenu((D_("Action"), D_("send file")), self._fileSendMenu, security_limit=10, help_string=D_("Send a file"), type_=C.MENU_SINGLE)

    def _fileSend(self, peer_jid_s, filepath, name="", file_desc="", profile=C.PROF_KEY_NONE):
        return self.fileSend(jid.JID(peer_jid_s), filepath, name or None, file_desc or None, profile)

    @defer.inlineCallbacks
    def fileSend(self, peer_jid, filepath, filename=None, file_desc=None, profile=C.PROF_KEY_NONE):
        """Send a file using best available method

        @param peer_jid(jid.JID): jid of the destinee
        @param filepath(str): absolute path to the file
        @param filename(unicode, None): name to use, or None to find it from filepath
        @param file_desc(unicode, None): description of the file
        @param profile: %(doc_profile)s
        @return (dict): action dictionary, with progress id in case of success, else xmlui message
        """
        if not os.path.isfile(filepath):
            raise exceptions.DataError(u"The given path doesn't link to a file")
        if not filename:
            filename = os.path.basename(filepath) or '_'
        for namespace, callback, priority, method_name in self._file_callbacks:
            has_feature = yield self.host.hasFeature(namespace, peer_jid, profile)
            if has_feature:
                log.info(u"{name} method will be used to send the file".format(name=method_name))
                progress_id = yield defer.maybeDeferred(callback, peer_jid, filepath, filename, file_desc, profile)
                defer.returnValue({'progress': progress_id})
        msg = u"Can't find any method to send file to {jid}".format(jid=peer_jid.full())
        log.warning(msg)
        defer.returnValue({'xmlui': xml_tools.note(u"Can't transfer file", msg, C.XMLUI_DATA_LVL_WARNING).toXml()})

    def _onFileChoosed(self, peer_jid, data, profile):
        cancelled = C.bool(data.get("cancelled", C.BOOL_FALSE))
        if cancelled:
            return
        path=data['path']
        return self.fileSend(peer_jid, path, profile=profile)

    def _fileSendMenu(self, data, profile):
        """ XMLUI activated by menu: return file sending UI

        @param profile: %(doc_profile)s
        """
        try:
            jid_ = jid.JID(data['jid'])
        except RuntimeError:
            raise exceptions.DataError(_("Invalid JID"))

        file_choosed_id = self.host.registerCallback(lambda data, profile: self._onFileChoosed(jid_, data, profile), with_data=True, one_shot=True)
        xml_ui = xml_tools.XMLUI(
            C.XMLUI_DIALOG,
            dialog_opt = {
                C.XMLUI_DATA_TYPE: C.XMLUI_DIALOG_FILE,
                C.XMLUI_DATA_MESS: _(SENDING).format(peer=jid_.full())},
            title = _(SENDING_TITLE),
            submit_id = file_choosed_id)

        return {'xmlui': xml_ui.toXml()}

    def register(self, namespace, callback, priority=0, method_name=None):
        """Register a fileSending method

        @param namespace(unicode): XEP namespace
        @param callback(callable): method to call (must have the same signature as [fileSend])
        @param priority(int): pririoty of this method, the higher available will be used
        @param method_name(unicode): short name for the method, namespace will be used if None
        """
        for data in self._file_callbacks:
            if namespace == data[0]:
                raise exceptions.ConflictError(u'A method with this namespace is already registered')
        self._file_callbacks.append((namespace, callback, priority, method_name or namespace))
        self._file_callbacks.sort(key=lambda data: data[2], reverse=True)

    def unregister(self, namespace):
        for idx, data in enumerate(self._file_callbacks):
            if data[0] == namespace:
                del [idx]
                return
        raise exceptions.NotFound(u"The namespace to unregister doesn't exist")

    # Dialogs with user
    # the overwrite check is done here

    def _openFileWrite(self, file_path, transfer_data, file_data, profile):
        assert 'file_obj' not in transfer_data
        transfer_data['file_obj'] = SatFile(
            self.host,
            file_path,
            'wb',
            uid=file_data[PROGRESS_ID_KEY],
            size=file_data['size'],
            data_cb = file_data.get('data_cb'),
            profile=profile,
            )

    def _gotConfirmation(self, data, peer_jid, transfer_data, file_data, profile):
        """Called when the permission and dest path have been received

        @param peer_jid(jid.JID): jid of the file sender
        @param transfer_data(dict): same as for [self.getDestDir]
        @param file_data(dict): same as for [self.getDestDir]
        @param profile: %(doc_profile)s
        return (bool): True if copy is wanted and OK
            False if user wants to cancel
            if file exists ask confirmation and call again self._getDestDir if needed
        """
        if data.get('cancelled', False):
            return False
        path = data['path']
        file_data['file_path'] = file_path = os.path.join(path, file_data['name'])
        log.debug(u'destination file path set to {}'.format(file_path))

        # we manage case where file already exists
        if os.path.exists(file_path):
            def check_overwrite(overwrite):
                if overwrite:
                    self._openFileWrite(file_path, transfer_data, file_data, profile)
                    return True
                else:
                    return self.getDestDir(peer_jid, transfer_data, file_data, profile)

            exists_d = xml_tools.deferConfirm(
                self.host,
                _(CONFIRM_OVERWRITE).format(file_path),
                _(CONFIRM_OVERWRITE_TITLE),
                action_extra={'meta_from_jid': peer_jid.full(),
                              'meta_type': C.META_TYPE_OVERWRITE,
                              'meta_progress_id': file_data[PROGRESS_ID_KEY]
                             },
                security_limit=SECURITY_LIMIT,
                profile=profile)
            exists_d.addCallback(check_overwrite)
            return exists_d

        self._openFileWrite(file_path, transfer_data, file_data, profile)
        return True

    def getDestDir(self, peer_jid, transfer_data, file_data, profile):
        """Request confirmation and destination dir to user

        Overwrite confirmation is managed.
        if transfer is confirmed, 'file_obj' is added to transfer_data
        @param peer_jid(jid.JID): jid of the file sender
        @param filename(unicode): name of the file
        @param transfer_data(dict): data of the transfer session,
            it will be only used to store the file_obj.
            "file_obj" key *MUST NOT* exist before using getDestDir
        @param file_data(dict): information about the file to be transfered
            It MUST contain the following keys:
                - peer_jid (jid.JID): other peer jid
                - name (unicode): name of the file to trasnsfer
                    the name must not be empty or contain a "/" character
                - size (int): size of the file
                - desc (unicode): description of the file
                - progress_id (unicode): id to use for progression
            It *MUST NOT* contain the "peer" key
            It may contain:
                - data_cb (callable): method called on each data read/write
            "file_path" will be added to this dict once destination selected
            "size_human" will also be added with human readable file size
        @param profile: %(doc_profile)s
        return (defer.Deferred): True if transfer is accepted
        """
        filename = file_data['name']
        assert filename and not '/' in filename
        assert PROGRESS_ID_KEY in file_data
        # human readable size
        file_data['size_human'] = u'{:.6n} Mio'.format(float(file_data['size'])/(1024**2))
        d = xml_tools.deferDialog(self.host,
            _(CONFIRM).format(peer=peer_jid.full(), **file_data),
            _(CONFIRM_TITLE),
            type_=C.XMLUI_DIALOG_FILE,
            options={C.XMLUI_DATA_FILETYPE: C.XMLUI_DATA_FILETYPE_DIR},
            action_extra={'meta_from_jid': peer_jid.full(),
                          'meta_type': C.META_TYPE_FILE,
                          'meta_progress_id': file_data[PROGRESS_ID_KEY]
                         },
            security_limit=SECURITY_LIMIT,
            profile=profile)
        d.addCallback(self._gotConfirmation, peer_jid, transfer_data, file_data, profile)
        return d
