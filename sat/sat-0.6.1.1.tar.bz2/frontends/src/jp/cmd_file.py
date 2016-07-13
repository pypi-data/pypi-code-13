#! /usr/bin/python
# -*- coding: utf-8 -*-

# jp: a SAT command line tool
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


import base
import sys
import os
import os.path
import tarfile
from sat.core.i18n import _
from sat_frontends.jp.constants import Const as C
from sat_frontends.tools import jid
import tempfile
import xml.etree.ElementTree as ET # FIXME: used temporarily to manage XMLUI


__commands__ = ["File"]


class Send(base.CommandBase):
    def __init__(self, host):
        super(Send, self).__init__(host, 'send', use_progress=True, use_verbose=True, help=_('Send a file to a contact'))
        self.need_loop=True

    def add_parser_options(self):
        self.parser.add_argument("files", type=str, nargs='+', metavar='file', help=_("a list of file"))
        self.parser.add_argument("jid", type=base.unicode_decoder, help=_("the destination jid"))
        self.parser.add_argument("-b", "--bz2", action="store_true", help=_("make a bzip2 tarball"))

    def start(self):
        """Send files to jabber contact"""
        self.send_files()

    def onProgressStarted(self, metadata):
        self.disp(_(u'File copy started'),2)

    def onProgressFinished(self, metadata):
        self.disp(_(u'File sent successfully'),2)

    def onProgressError(self, error_msg):
        self.disp(_(u'Error while sending file: {}').format(error_msg),error=True)

    def gotId(self, data, file_):
        """Called when a progress id has been received

        @param pid(unicode): progress id
        @param file_(str): file path
        """
        #FIXME: this show progress only for last progress_id
        self.disp(_(u"File request sent to {jid}".format(jid=self.full_dest_jid)), 1)
        try:
            self.progress_id = data['progress']
        except KeyError:
            # TODO: if 'xmlui' key is present, manage xmlui message display
            self.disp(_(u"Can't send file to {jid}".format(jid=self.full_dest_jid)), error=True)
            self.host.quit(2)

    def error(self, failure):
        self.disp(_("Error while trying to send a file: {reason}").format(reason=failure), error=True)
        self.host.quit(1)

    def send_files(self):

        for file_ in self.args.files:
            if not os.path.exists(file_):
                self.disp(_(u"file [{}] doesn't exist !").format(file_), error=True)
                self.host.quit(1)
            if not self.args.bz2 and os.path.isdir(file_):
                self.disp(_(u"[{}] is a dir ! Please send files inside or use compression").format(file_))
                self.host.quit(1)

        self.full_dest_jid = self.host.get_full_jid(self.args.jid)

        if self.args.bz2:
            with tempfile.NamedTemporaryFile('wb', delete=False) as buf:
                self.host.addOnQuitCallback(os.unlink, buf.name)
                self.disp(_(u"bz2 is an experimental option, use with caution"))
                #FIXME: check free space
                self.disp(_(u"Starting compression, please wait..."))
                sys.stdout.flush()
                bz2 = tarfile.open(mode="w:bz2", fileobj=buf)
                archive_name = u'{}.tar.bz2'.format(os.path.basename(self.args.files[0]) or u'compressed_files')
                for file_ in self.args.files:
                    self.disp(_(u"Adding {}").format(file_), 1)
                    bz2.add(file_)
                bz2.close()
                self.disp(_(u"Done !"), 1)

                self.host.bridge.fileSend(self.full_dest_jid, buf.name, archive_name, '', self.profile, callback=lambda pid, file_=buf.name: self.gotId(pid, file_), errback=self.error)
        else:
            for file_ in self.args.files:
                path = os.path.abspath(file_)
                self.host.bridge.fileSend(self.full_dest_jid, path, '', '', self.profile, callback=lambda pid, file_=file_: self.gotId(pid, file_), errback=self.error)


class Receive(base.CommandAnswering):

    def __init__(self, host):
        super(Receive, self).__init__(host, 'receive', use_progress=True, use_verbose=True, help=_('Wait for a file to be sent by a contact'))
        self._overwrite_refused = False # True when one overwrite as already been refused
        self.action_callbacks = {C.META_TYPE_FILE: self.onFileAction,
                                 C.META_TYPE_OVERWRITE: self.onOverwriteAction}

    def onProgressStarted(self, metadata):
        self.disp(_(u'File copy started'),2)

    def onProgressFinished(self, metadata):
        self.disp(_(u'File received successfully'),2)
        if metadata.get('hash_verified', False):
            try:
                self.disp(_(u'hash checked: {algo}:{checksum}').format(
                    algo=metadata['hash_algo'],
                    checksum=metadata['hash']),
                    1)
            except KeyError:
                self.disp(_(u'hash is checked but hash value is missing', 1), error=True)
        else:
            self.disp(_(u"hash can't be verified"), 1)

    def onProgressError(self, error_msg):
        self.disp(_(u'Error while receiving file: {}').format(error_msg),error=True)

    def getXmluiId(self, action_data):
        # FIXME: we temporarily use ElementTree, but a real XMLUI managing module
        #        should be available in the futur
        # TODO: XMLUI module
        try:
            xml_ui = action_data['xmlui']
        except KeyError:
            self.disp(_(u"Action has no XMLUI"), 1)
        else:
            ui = ET.fromstring(xml_ui.encode('utf-8'))
            xmlui_id = ui.get('submit')
            if not xmlui_id:
                self.disp(_(u"Invalid XMLUI received"), error=True)
            return xmlui_id

    def onFileAction(self, action_data, action_id, security_limit, profile):
        xmlui_id = self.getXmluiId(action_data)
        if xmlui_id is None:
            return self.host.quitFromSignal(1)
        try:
            from_jid = jid.JID(action_data['meta_from_jid'])
        except KeyError:
            self.disp(_(u"Ignoring action without from_jid data"), 1)
            return
        try:
            progress_id = action_data['meta_progress_id']
        except KeyError:
            self.disp(_(u"ignoring action without progress id"), 1)
            return

        if not self.bare_jids or from_jid.bare in self.bare_jids:
            if self._overwrite_refused:
                self.disp(_(u"File refused because overwrite is needed"), error=True)
                self.host.bridge.launchAction(xmlui_id, {'cancelled': C.BOOL_TRUE}, profile_key=profile)
                return self.host.quitFromSignal(2)
            self.progress_id = progress_id
            xmlui_data = {'path': self.path}
            self.host.bridge.launchAction(xmlui_id, xmlui_data, profile_key=profile)

    def onOverwriteAction(self, action_data, action_id, security_limit, profile):
        xmlui_id = self.getXmluiId(action_data)
        if xmlui_id is None:
            return self.host.quitFromSignal(1)
        try:
            progress_id = action_data['meta_progress_id']
        except KeyError:
            self.disp(_(u"ignoring action without progress id"), 1)
            return
        self.disp(_(u"Overwriting needed"), 1)

        if progress_id == self.progress_id:
            if self.args.force:
                self.disp(_(u"Overwrite accepted"), 2)
            else:
                self.disp(_(u"Refused to overwrite"), 2)
                self._overwrite_refused = True

            xmlui_data = {'answer': C.boolConst(self.args.force)}
            self.host.bridge.launchAction(xmlui_id, xmlui_data, profile_key=profile)

    def add_parser_options(self):
        self.parser.add_argument("jids", type=base.unicode_decoder, nargs="*", help=_(u'JIDs accepted (accept everything if none is specified)'))
        self.parser.add_argument("-m", "--multiple", action="store_true", help=_(u"accept multiple files (you'll have to stop manually)"))
        self.parser.add_argument("-f", "--force", action="store_true", help=_(u"force overwritting of existing files (/!\\ name is choosed by sended)"))
        self.parser.add_argument("--path", default='.', metavar='DIR', help=_(u"destination path (default: working directory)"))

    def start(self):
        self.bare_jids = [jid.JID(jid_).bare for jid_ in self.args.jids]
        self.path = os.path.abspath(self.args.path)
        if not os.path.isdir(self.path):
            self.disp(_(u"Given path is not a directory !", error=True))
            self.host.quit(2)
        if self.args.multiple:
            self.host.quit_on_progress_end = False
        self.disp(_(u"waiting for incoming file request"),2)


class Upload(base.CommandBase):

    def __init__(self, host):
        super(Upload, self).__init__(host, 'upload', use_progress=True, use_verbose=True, help=_('Upload a file'))
        self.need_loop=True

    def add_parser_options(self):
        self.parser.add_argument("file", type=str, help=_("file to upload"))
        self.parser.add_argument("jid", type=base.unicode_decoder, nargs='?',  help=_("jid of upload component (nothing to autodetect)"))
        self.parser.add_argument("--ignore-tls-errors", action="store_true", help=_("ignore invalide TLS certificate"))

    def onProgressStarted(self, metadata):
        self.disp(_(u'File upload started'),2)

    def onProgressFinished(self, metadata):
        self.disp(_(u'File uploaded successfully'),2)
        try:
            url = metadata['url']
        except KeyError:
            self.disp(u'download URL not found in metadata')
        else:
            self.disp(_(u'URL to retrieve the file:'),1)
            # XXX: url is display alone on a line to make parsing easier
            self.disp(url)

    def onProgressError(self, error_msg):
        self.disp(_(u'Error while uploading file: {}').format(error_msg),error=True)

    def gotId(self, data, file_):
        """Called when a progress id has been received

        @param pid(unicode): progress id
        @param file_(str): file path
        """
        try:
            self.progress_id = data['progress']
        except KeyError:
            # TODO: if 'xmlui' key is present, manage xmlui message display
            self.disp(_(u"Can't upload file"), error=True)
            self.host.quit(2)

    def error(self, failure):
        self.disp(_("Error while trying to upload a file: {reason}").format(reason=failure), error=True)
        self.host.quit(1)

    def start(self):
        file_ = self.args.file
        if not os.path.exists(file_):
            self.disp(_(u"file [{}] doesn't exist !").format(file_), error=True)
            self.host.quit(1)
        if os.path.isdir(file_):
            self.disp(_(u"[{}] is a dir! Can't upload a dir").format(file_))
            self.host.quit(1)

        self.full_dest_jid = self.host.get_full_jid(self.args.jid) if self.args.jid is not None else ''
        options = {}
        if self.args.ignore_tls_errors:
            options['ignore_tls_errors'] = C.BOOL_TRUE

        path = os.path.abspath(file_)
        self.host.bridge.fileUpload(path, '', self.full_dest_jid, options, self.profile, callback=lambda pid, file_=file_: self.gotId(pid, file_), errback=self.error)


class File(base.CommandBase):
    subcommands = (Send, Receive, Upload)

    def __init__(self, host):
        super(File, self).__init__(host, 'file', use_profile=False, help=_('File sending/receiving'))
