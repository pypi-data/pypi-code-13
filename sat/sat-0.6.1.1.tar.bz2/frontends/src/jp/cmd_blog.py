#! /usr/bin/python
# -*- coding: utf-8 -*-

# jp: a SàT command line tool
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
from sat.core.i18n import _
from sat.core.constants import Const as C
from sat.tools import config
from ConfigParser import NoSectionError, NoOptionError
import json
import sys
import os.path
import os
import time
import tempfile
import subprocess
import shlex
import glob
from sat.tools.common import data_format
from sat.tools.common import regex

__commands__ = ["Blog"]

# extensions to use with known syntaxes
SYNTAX_EXT = {
    '': 'txt', # used when the syntax is not found
    "XHTML": "xhtml",
    "markdown": "md"
    }

# defaut arguments used for some known editors
VIM_SPLIT_ARGS = "-c 'vsplit|wincmd w|next|wincmd w'"
EMACS_SPLIT_ARGS = '--eval "(split-window-horizontally)"'
EDITOR_ARGS_MAGIC = {
    'vim': VIM_SPLIT_ARGS + ' {content_file} {metadata_file}',
    'gvim': VIM_SPLIT_ARGS + ' --nofork {content_file} {metadata_file}',
    'emacs': EMACS_SPLIT_ARGS + ' {content_file} {metadata_file}',
    'xemacs': EMACS_SPLIT_ARGS + ' {content_file} {metadata_file}',
    'nano': ' -F {content_file} {metadata_file}',
    }

CONF_SYNTAX_EXT = 'syntax_ext_dict'
BLOG_TMP_DIR="blog"
METADATA_SUFF = '_metadata.json'
# key to remove from metadata tmp file if they exist
KEY_TO_REMOVE_METADATA = ('id','content', 'content_xhtml', 'comments_node', 'comments_service', 'updated')

URL_REDIRECT_PREFIX = 'url_redirect_'
INOTIFY_INSTALL = '"pip install inotify"'
SECURE_UNLINK_MAX = 10 * 2 # we double value has there are 2 files per draft (content and metadata)
SECURE_UNLINK_DIR = ".backup"


class BlogCommon(object):

    def __init__(self, host):
        self.host = host

    def getTmpDir(self, sat_conf, sub_dir=None):
        """Return directory used to store temporary files

        @param sat_conf(ConfigParser.ConfigParser): instance opened on sat configuration
        @param sub_dir(str): sub directory where data need to be put
            profile can be used here, or special directory name
            sub_dir will be escaped to be usable in path (use regex.pathUnescape to find
            initial str)
        @return (str): path to the dir
        """
        local_dir = config.getConfig(sat_conf, '', 'local_dir', Exception)
        path = [local_dir, BLOG_TMP_DIR]
        if sub_dir is not None:
            path.append(regex.pathEscape(sub_dir))
        return os.path.join(*path)

    def getCurrentFile(self, sat_conf, profile):
        """Get most recently edited file

        @param sat_conf(ConfigParser.ConfigParser): instance opened on sat configuration
        @param profile(unicode): profile linked to the blog draft
        @return(str): full path of current file
        """
        # we guess the blog item currently edited by choosing
        # the most recent file corresponding to temp file pattern
        # in tmp_dir, excluding metadata files
        tmp_dir = self.getTmpDir(sat_conf, profile.encode('utf-8'))
        available = [path for path in glob.glob(os.path.join(tmp_dir, 'blog_*')) if not path.endswith(METADATA_SUFF)]
        if not available:
            self.disp(u"Counldn't find any content draft in {path}".format(path=tmp_dir), error=True)
            self.host.quit(1)
        return max(available, key=lambda path: os.stat(path).st_mtime)

    def secureUnlink(self, sat_conf, path):
        """Unlink given path after keeping it for a while

        This method is used to prevent accidental deletion of a blog draft
        If there are more file in SECURE_UNLINK_DIR than SECURE_UNLINK_MAX,
        older file are deleted
        @param sat_conf(ConfigParser.ConfigParser): instance opened on sat configuration
        @param path(str): file to unlink
        """
        if not os.path.isfile(path):
            raise OSError(u"path must link to a regular file")
        if not path.startswith(self.getTmpDir(sat_conf)):
            self.disp(u"File {} is not in blog temporary hierarchy, we do not remove it".format(path.decode('utf-8')), 2)
            return
        backup_dir = self.getTmpDir(sat_conf, SECURE_UNLINK_DIR)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        filename = os.path.basename(path)
        backup_path = os.path.join(backup_dir, filename)
        # we move file to backup dir
        self.host.disp(u"Backuping file {src} to {dst}".format(
            src=path.decode('utf-8'), dst=backup_path.decode('utf-8')), 1)
        os.rename(path, backup_path)
        # and if we exceeded the limit, we remove older file
        backup_files = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir)]
        if len(backup_files) > SECURE_UNLINK_MAX:
            backup_files.sort(key=lambda path: os.stat(path).st_mtime)
            for path in backup_files[:len(backup_files)  - SECURE_UNLINK_MAX]:
                self.host.disp(u"Purging backup file {}".format(path.decode('utf-8')), 2)
                os.unlink(path)

    def guessSyntaxFromPath(self, sat_conf, path):
        """Return syntax guessed according to filename extension

        @param sat_conf(ConfigParser.ConfigParser): instance opened on sat configuration
        @param path(str): path to the content file
        @return(unicode): syntax to use
        """
        # we first try to guess syntax with extension
        ext = os.path.splitext(path)[1][1:] # we get extension without the '.'
        if ext:
            for k,v in SYNTAX_EXT.iteritems():
                if k and ext == v:
                    return k

        # if not found, we use current syntax
        return self.host.bridge.getParamA("Syntax", "Composition", "value", self.profile)

    def parse_args(self, cmd_line, **format_kw):
        """Parse command arguments

        @param cmd_line(unicode): command line as found in sat.conf
        @param format_kw: keywords used for formmating
        @return (list(unicode)): list of arguments to pass to subprocess function
        """
        try:
            # we split the arguments and add the known fields
            # we split arguments first to avoid escaping issues in file names
            return [a.format(**format_kw) for a in shlex.split(cmd_line)]
        except ValueError as e:
            self.disp(u"Couldn't parse editor cmd [{cmd}]: {reason}".format(cmd=cmd_line, reason=e))
            return []


class Edit(base.CommandBase, BlogCommon):

    def __init__(self, host):
        base.CommandBase.__init__(self, host, 'edit', use_verbose=True, help=_(u'edit an existing or new blog post'))
        BlogCommon.__init__(self, self.host)

    def add_parser_options(self):
        self.parser.add_argument("item", type=base.unicode_decoder, nargs='?', default=u'new', help=_(u"URL of the item to edit, or keyword"))
        self.parser.add_argument("-P", "--preview", action="store_true", help=_(u"launch a blog preview in parallel"))
        self.parser.add_argument("-T", '--title', type=base.unicode_decoder, help=_(u"title of the item"))
        self.parser.add_argument("-t", '--tag', type=base.unicode_decoder, action='append', help=_(u"tag (category) of your item"))
        self.parser.add_argument("--no-comment", action='store_true', help=_(u"disable comments"))

    def getTmpFile(self, sat_conf, tmp_suff):
        """Create a temporary file to received blog item body

        @param sat_conf(ConfigParser.ConfigParser): instance opened on sat configuration
        @param tmp_suff (str): suffix to use for the filename
        @return (tuple(file, str)): opened (w+b) file object and file path
        """
        tmp_dir = self.getTmpDir(sat_conf, self.profile.encode('utf-8'))
        if not os.path.exists(tmp_dir):
            try:
                os.makedirs(tmp_dir)
            except OSError as e:
                self.disp(u"Can't create {path} directory: {reason}".format(
                    path=tmp_dir, reason=e), error=True)
                self.host.quit(1)
        try:
            fd, path = tempfile.mkstemp(suffix=tmp_suff,
                prefix=time.strftime('blog_%Y-%m-%d_%H:%M:%S_'),
                dir=tmp_dir, text=True)
            return os.fdopen(fd, 'w+b'), path
        except OSError as e:
            self.disp(u"Can't create temporary file: {reason}".format(reason=e), error=True)
            self.host.quit(1)

    def buildMetadataFile(self, content_file_path, mb_data=None):
        """Build a metadata file using json

        The file is named after content_file_path, with extension replaced by _metadata.json
        @param content_file_path(str): path to the temporary file which will contain the body
        @param mb_data(dict, None): microblog metadata (for existing items)
        @return (tuple[dict, str]): merged metadata put originaly in metadata file
            and path to temporary metadata file
        """
        # we first construct metadata from edited item ones and CLI argumments
        # or re-use the existing one if it exists
        meta_file_path = os.path.splitext(content_file_path)[0] + METADATA_SUFF
        if os.path.exists(meta_file_path):
            self.disp(u"Metadata file already exists, we re-use it")
            try:
                with open(meta_file_path, 'rb') as f:
                    mb_data = json.load(f)
            except (OSError, IOError, ValueError) as e:
                self.disp(u"Can't read existing metadata file at {path}, aborting: {reason}".format(
                    path=meta_file_path, reason=e), error=True)
                self.host.quit(1)
        else:
            mb_data = {} if mb_data is None else mb_data.copy()

        # in all cases, we want to remove unwanted keys
        for key in KEY_TO_REMOVE_METADATA:
            try:
                del mb_data[key]
            except KeyError:
                pass
        # and override metadata with command-line arguments
        mb_data['allow_comments'] = C.boolConst(not self.args.no_comment)
        if self.args.tag:
            data_format.iter2dict('tag', self.args.tag, mb_data, check_conflict=False)
        if self.args.title is not None:
            mb_data['title'] = self.args.title

        # then we create the file and write metadata there, as JSON dict
        # XXX: if we port jp one day on Windows, O_BINARY may need to be added here
        with os.fdopen(os.open(meta_file_path, os.O_RDWR | os.O_CREAT | os.O_TRUNC,0o600), 'w+b') as f:
            # we need to use an intermediate unicode buffer to write to the file unicode without escaping characters
            unicode_dump = json.dumps(mb_data, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True)
            f.write(unicode_dump.encode('utf-8'))

        return mb_data, meta_file_path

    def edit(self, sat_conf, content_file_path, content_file_obj,
             pubsub_service, pubsub_node, mb_data=None):
        """Edit the file contening the content using editor, and publish it"""
        item_ori_mb_data = mb_data
        # we first create metadata file
        meta_ori, meta_file_path = self.buildMetadataFile(content_file_path, item_ori_mb_data)

        # then we calculate hashes to check for modifications
        import hashlib
        content_file_obj.seek(0)
        tmp_ori_hash = hashlib.sha1(content_file_obj.read()).digest()
        content_file_obj.close()

        # do we need a preview ?
        if self.args.preview:
            self.disp(u"Preview requested, launching it", 1)
            # we redirect outputs to /dev/null to avoid console pollution in editor
            # if user wants to see messages, (s)he can call "blog preview" directly
            DEVNULL = open(os.devnull, 'wb')
            subprocess.Popen([sys.argv[0], "blog", "preview", "--inotify", "true", "-p", self.profile, content_file_path], stdout=DEVNULL, stderr=subprocess.STDOUT)

        # then we launch editor
        editor = config.getConfig(sat_conf, 'jp', 'editor') or os.getenv('EDITOR', 'vi')
        try:
            # is there custom arguments in sat.conf ?
            editor_args = config.getConfig(sat_conf, 'jp', 'blog_editor_args', Exception)
        except (NoOptionError, NoSectionError):
            # no, we check if we know the editor and have special arguments
            editor_args = EDITOR_ARGS_MAGIC.get(os.path.basename(editor), '')
        args = self.parse_args(editor_args, content_file=content_file_path, metadata_file=meta_file_path)
        if not args:
            args = [content_file_path]
        editor_exit = subprocess.call([editor] + args)

        # we send the file if edition was a success
        if editor_exit != 0:
            self.disp(u"Editor exited with an error code, so temporary file has not be deleted, and blog item is not published.\nTou can find temporary file at {path}".format(
                path=content_file_path), error=True)
        else:
            try:
                with open(content_file_path, 'rb') as f:
                    content = f.read()
                with open(meta_file_path, 'rb') as f:
                    mb_data = json.load(f)
            except (OSError, IOError):
                self.disp(u"Can read files at {content_path} and/or {meta_path}, have they been deleted?\nCancelling edition".format(
                    content_path=content_file_path, meta_path=meta_file_path), error=True)
                self.host.quit(1)
            except ValueError:
                self.disp(u"Can't parse metadata, please check it is correct JSON format. Cancelling edition.\n" +
                    "You can find tmp file at {content_path} and temporary meta file at {meta_path}.".format(
                    content_path=content_file_path, meta_path=meta_file_path), error=True)
                self.host.quit(1)

            if not C.bool(mb_data.get('publish', "true")):
                self.disp(u'Publication blocked by "publish" key in metadata, cancelling edition.\n\n' +
                    "temporary file path:\t{content_path}\nmetadata file path:\t{meta_path}".format(
                    content_path=content_file_path, meta_path=meta_file_path), error=True)
                self.host.quit(0)

            if len(content) == 0:
                self.disp(u"Content is empty, cancelling the blog edition")
                if not content_file_path.startswith(self.getTmpDir(sat_conf)):
                    self.disp(u"File are not in blog temporary hierarchy, we do not remove it", 2)
                    self.host.quit()
                self.disp(u"Deletion of {}".format(content_file_path.decode('utf-8')), 2)
                os.unlink(content_file_path)
                self.disp(u"Deletion of {}".format(meta_file_path.decode('utf-8')), 2)
                os.unlink(meta_file_path)
                self.host.quit()

            # time to re-check the hash
            elif (tmp_ori_hash == hashlib.sha1(content).digest() and
                  meta_ori == mb_data):
                self.disp(u"The content has not been modified, cancelling the blog edition")

            else:
                # we can now send the blog
                mb_data['content_rich'] =  content.decode('utf-8-sig') # we use utf-8-sig to avoid BOM

                if item_ori_mb_data is not None:
                    mb_data['id'] = item_ori_mb_data['id']

                try:
                    self.host.bridge.mbSend(pubsub_service, pubsub_node, mb_data, self.profile)
                except Exception as e:
                    self.disp(u"Error while sending your blog, the temporary files have been kept at {content_path} and {meta_path}: {reason}".format(
                        content_path=content_file_path, meta_path=meta_file_path, reason=e), error=True)
                    self.host.quit(1)
                else:
                    self.disp(u"Blog item published")

            self.secureUnlink(sat_conf, content_file_path)
            self.secureUnlink(sat_conf, meta_file_path)

    def start(self):
        command = self.args.item.lower()
        sat_conf = config.parseMainConf()
        # if there are user defined extension, we use them
        SYNTAX_EXT.update(config.getConfig(sat_conf, 'jp', CONF_SYNTAX_EXT, {}))
        current_syntax = None
        pubsub_service = pubsub_node = ''
        pubsub_item = None

        if command not in ('new', 'last', 'current'):
            # we have probably an URL, we try to parse it
            import urlparse
            url = self.args.item
            parsed_url = urlparse.urlsplit(url)
            if parsed_url.scheme.startswith('http'):
                self.disp(u"{} URL found, trying to find associated xmpp: URI".format(parsed_url.scheme.upper()),1)
                # HTTP URL, we try to find xmpp: links
                try:
                    from lxml import etree
                except ImportError:
                    self.disp(u"lxml module must be installed to use http(s) scheme, please install it with \"pip install lxml\"", error=True)
                    self.host.quit(1)
                parser = etree.HTMLParser()
                root = etree.parse(url, parser)
                links = root.xpath("//link[@rel='alternate' and starts-with(@href, 'xmpp:')]")
                if not links:
                    self.disp(u'Could not find alternate "xmpp:" URI, can\'t find associated XMPP PubSub node/item', error=True)
                    self.host.quit(1)
                url = links[0].get('href')
                parsed_url = urlparse.urlsplit(url)

            if parsed_url.scheme == 'xmpp':
                self.disp(u"XMPP URI used: {}".format(url),2)
                # XXX: if we have not xmpp: URI here, we'll take the data as a file path
                pubsub_service = parsed_url.path
                pubsub_data = urlparse.parse_qs(parsed_url.query)
                try:
                    pubsub_node = pubsub_data['node'][0]
                except KeyError:
                    self.disp(u'No node found in xmpp: URI, can\'t retrieve item', error=True)
                    self.host.quit(1)
                pubsub_item = pubsub_data.get('item',[None])[0]
                if pubsub_item is not None:
                    command = 'edit' # XXX: edit command is only used internaly, it similar to last, but with the item given in the URL
                else:
                    command = 'new'

        if command in ('new', 'last', 'edit'):
            # we get current syntax to determine file extension
            current_syntax = self.host.bridge.getParamA("Syntax", "Composition", "value", self.profile)
            # we now create a temporary file
            tmp_suff = '.' + SYNTAX_EXT.get(current_syntax, SYNTAX_EXT[''])
            content_file_obj, content_file_path = self.getTmpFile(sat_conf, tmp_suff)
            if command == 'new':
                self.disp(u'Editing a new blog item', 2)
                mb_data = None
            elif command in ('last', 'edit'):
                self.disp(u'Editing requested published item', 2)
                try:
                    items_ids = [pubsub_item] if pubsub_item is not None else []
                    mb_data = self.host.bridge.mbGet(pubsub_service, pubsub_node, 1, items_ids, {}, self.profile)[0][0]
                except Exception as e:
                    self.disp(u"Error while retrieving last item: {}".format(e))
                    self.host.quit(1)

                content = mb_data['content_xhtml']
                if content and current_syntax != 'XHTML':
                    content = self.host.bridge.syntaxConvert(content, 'XHTML', current_syntax, False, self.profile)
                content_file_obj.write(content.encode('utf-8'))
                content_file_obj.seek(0)
        else:
            mb_data = None
            if command == 'current':
                # use wants to continue current draft
                content_file_path = self.getCurrentFile(sat_conf, self.profile)
                self.disp(u'Continuing edition of current draft', 2)
            else:
                # we consider the item as a file path
                content_file_path = os.path.expanduser(self.args.item)
            content_file_obj = open(content_file_path, 'r+b')
            current_syntax = self.guessSyntaxFromPath(sat_conf, content_file_path)

        self.disp(u"Syntax used: {}".format(current_syntax), 1)
        self.edit(sat_conf, content_file_path, content_file_obj, pubsub_service, pubsub_node, mb_data=mb_data)


class Preview(base.CommandBase, BlogCommon):

    def __init__(self, host):
        base.CommandBase.__init__(self, host, 'preview', use_verbose=True, help=_(u'preview a blog content'))
        BlogCommon.__init__(self, self.host)

    def add_parser_options(self):
        self.parser.add_argument("--inotify", type=str, choices=('auto', 'true', 'false'), default=u'auto', help=_(u"use inotify to handle preview"))
        self.parser.add_argument("file", type=base.unicode_decoder, nargs='?', default=u'current', help=_(u"path to the content file"))

    def showPreview(self):
        # we implement showPreview here so we don't have to import webbroser and urllib
        # when preview is not used
        url = 'file:{}'.format(self.urllib.quote(self.preview_file_path))
        self.webbrowser.open_new_tab(url)

    def _launchPreviewExt(self, cmd_line, opt_name):
        url = 'file:{}'.format(self.urllib.quote(self.preview_file_path))
        args = self.parse_args(cmd_line, url=url, preview_file=self.preview_file_path)
        if not args:
            self.disp(u"Couln't find command in \"{name}\", abording".format(name=opt_name), error=True)
            self.host.quit(1)
        subprocess.Popen(args)

    def openPreviewExt(self):
        self._launchPreviewExt(self.open_cb_cmd, "blog_preview_open_cmd")

    def updatePreviewExt(self):
        self._launchPreviewExt(self.update_cb_cmd, "blog_preview_update_cmd")

    def updateContent(self):
        with open(self.content_file_path, 'rb') as f:
            content = f.read().decode('utf-8-sig')
            if content and self.syntax != 'XHTML':
                # we use safe=True because we want to have a preview as close as possible to what the
                # people will see
                content = self.host.bridge.syntaxConvert(content, self.syntax, 'XHTML', True, self.profile)

        xhtml = (u'<html xmlns="http://www.w3.org/1999/xhtml">' +
                 u'<head><meta http-equiv="Content-Type" content="text/html;charset=utf-8" /></head>'+
                 '<body>{}</body>' +
                 u'</html>').format(content)

        with open(self.preview_file_path, 'wb') as f:
            f.write(xhtml.encode('utf-8'))

    def start(self):
        import webbrowser
        import urllib
        self.webbrowser, self.urllib = webbrowser, urllib

        if self.args.inotify != 'false':
            try:
                import inotify.adapters
                import inotify.constants
                from inotify.calls import InotifyError
            except ImportError:
                if self.args.inotify == 'auto':
                    inotify = None
                    self.disp(u'inotify module not found, deactivating feature. You can install it with {install}'.format(install=INOTIFY_INSTALL))
                else:
                    self.disp(u"inotify not found, can't activate the feature! Please install it with {install}".format(install=INOTIFY_INSTALL), error=True)
                    self.host.quit(1)
            else:
                # we deactivate logging in inotify, which is quite annoying
                try:
                    inotify.adapters._LOGGER.setLevel(40)
                except AttributeError:
                    self.disp(u"Logger doesn't exists, inotify may have chanded", error=True)
        else:
            inotify=None

        sat_conf = config.parseMainConf()
        SYNTAX_EXT.update(config.getConfig(sat_conf, 'jp', CONF_SYNTAX_EXT, {}))

        try:
            self.open_cb_cmd = config.getConfig(sat_conf, 'jp', "blog_preview_open_cmd", Exception)
        except (NoOptionError, NoSectionError):
            self.open_cb_cmd = None
            open_cb = self.showPreview
        else:
            open_cb = self.openPreviewExt

        self.update_cb_cmd = config.getConfig(sat_conf, 'jp', "blog_preview_update_cmd", self.open_cb_cmd)
        if self.update_cb_cmd is None:
            update_cb = self.showPreview
        else:
            update_cb = self.updatePreviewExt

        # which file do we need to edit?
        if self.args.file == 'current':
            self.content_file_path = self.getCurrentFile(sat_conf, self.profile)
        else:
            self.content_file_path = os.path.abspath(self.args.file)

        self.syntax = self.guessSyntaxFromPath(sat_conf, self.content_file_path)


        # at this point the syntax is converted, we can display the preview
        preview_file = tempfile.NamedTemporaryFile(suffix='.xhtml', delete=False)
        self.preview_file_path = preview_file.name
        preview_file.close()
        self.updateContent()

        if inotify is None:
            # XXX: we don't delete file automatically because browser need it (and webbrowser.open can return before it is read)
            self.disp(u'temporary file created at {}\nthis file will NOT BE DELETED AUTOMATICALLY, please delete it yourself when you have finished'.format(self.preview_file_path))
            open_cb()
        else:
            open_cb()
            i = inotify.adapters.Inotify(block_duration_s=60) # no need for 1 s duraction, inotify drive actions here

            def add_watch():
                i.add_watch(self.content_file_path, mask=inotify.constants.IN_CLOSE_WRITE |
                                                         inotify.constants.IN_DELETE_SELF |
                                                         inotify.constants.IN_MOVE_SELF)
            add_watch()

            try:
                for event in i.event_gen():
                    if event is not None:
                        self.disp(u"Content updated", 1)
                        if {"IN_DELETE_SELF", "IN_MOVE_SELF"}.intersection(event[1]):
                            self.disp(u"{} event catched, changing the watch".format(", ".join(event[1])), 2)
                            try:
                                add_watch()
                            except InotifyError:
                                # if the new file is not here yet we can have an error
                                # as a workaround, we do a little rest
                                time.sleep(1)
                                add_watch()
                        self.updateContent()
                        update_cb()
            except InotifyError:
                self.disp(u"Can't catch inotify events, as the file been deleted?", error=True)
            finally:
                os.unlink(self.preview_file_path)
                try:
                    i.remove_watch(self.content_file_path)
                except InotifyError:
                    pass


class Import(base.CommandAnswering):
    def __init__(self, host):
        super(Import, self).__init__(host, 'import', use_progress=True, help=_(u'import an external blog'))
        self.need_loop=True

    def add_parser_options(self):
        self.parser.add_argument("importer", type=base.unicode_decoder, nargs='?', help=_(u"importer name, nothing to display importers list"))
        self.parser.add_argument('--host', type=base.unicode_decoder, help=_(u"original blog host"))
        self.parser.add_argument('--no-images-upload', action='store_true', help=_(u"do *NOT* upload images (default: do upload images)"))
        self.parser.add_argument('--upload-ignore-host', help=_(u"do not upload images from this host (default: upload all images)"))
        self.parser.add_argument("--ignore-tls-errors", action="store_true", help=_("ignore invalide TLS certificate for uploads"))
        self.parser.add_argument('-o', '--option', action='append', nargs=2, default=[], metavar=(u'NAME', u'VALUE'),
            help=_(u"importer specific options (see importer description)"))
        self.parser.add_argument('--service', type=base.unicode_decoder, default=u'', metavar=u'PUBSUB_SERVICE',
            help=_(u"PubSub service where the items must be uploaded (default: server)"))
        self.parser.add_argument("location", type=base.unicode_decoder, nargs='?',
            help=_(u"importer data location (see importer description), nothing to show importer description"))

    def onProgressStarted(self, metadata):
        self.disp(_(u'Blog upload started'),2)

    def onProgressFinished(self, metadata):
        self.disp(_(u'Blog uploaded successfully'),2)
        redirections = {k[len(URL_REDIRECT_PREFIX):]:v for k,v in metadata.iteritems()
            if k.startswith(URL_REDIRECT_PREFIX)}
        if redirections:
            conf = u'\n'.join([
                u'url_redirections_profile = {}'.format(self.profile),
                u"url_redirections_dict = {}".format(
                # we need to add ' ' before each new line and to double each '%' for ConfigParser
                u'\n '.join(json.dumps(redirections, indent=1, separators=(',',': ')).replace(u'%', u'%%').split(u'\n'))),
                ])
            self.disp(_(u'\nTo redirect old URLs to new ones, put the following lines in your sat.conf file, in [libervia] section:\n\n{conf}'.format(conf=conf)))

    def onProgressError(self, error_msg):
        self.disp(_(u'Error while uploading blog: {}').format(error_msg),error=True)

    def error(self, failure):
        self.disp(_("Error while trying to upload a blog: {reason}").format(reason=failure), error=True)
        self.host.quit(1)

    def start(self):
        if self.args.location is None:
            for name in ('option', 'service', 'no_images_upload'):
                if getattr(self.args, name):
                    self.parser.error(_(u"{name} argument can't be used without location argument").format(name=name))
            if self.args.importer is None:
                print u'\n'.join([u'{}: {}'.format(name, desc) for name, desc in self.host.bridge.blogImportList()])
            else:
                try:
                    short_desc, long_desc = self.host.bridge.blogImportDesc(self.args.importer)
                except Exception as e:
                    msg = [l for l in unicode(e).split('\n') if l][-1] # we only keep the last line
                    print msg
                    self.host.quit(1)
                else:
                    print u"{name}: {short_desc}\n\n{long_desc}".format(name=self.args.importer, short_desc=short_desc, long_desc=long_desc)
            self.host.quit()
        else:
            # we have a location, an import is requested
            options = {key: value for key, value in self.args.option}
            if self.args.host:
                options['host'] = self.args.host
            if self.args.ignore_tls_errors:
                options['ignore_tls_errors'] = C.BOOL_TRUE
            if self.args.no_images_upload:
                options['upload_images'] = C.BOOL_FALSE
                if self.args.upload_ignore_host:
                    self.parser.error(u"upload-ignore-host option can't be used when no-images-upload is set")
            elif self.args.upload_ignore_host:
                options['upload_ignore_host'] = self.args.upload_ignore_host
            def gotId(id_):
                self.progress_id = id_
            self.host.bridge.blogImport(self.args.importer, self.args.location, options, self.args.service, self.profile,
                callback=gotId, errback=self.error)


class Blog(base.CommandBase):
    subcommands = (Edit, Preview, Import)

    def __init__(self, host):
        super(Blog, self).__init__(host, 'blog', use_profile=False, help=_('blog/microblog management'))
