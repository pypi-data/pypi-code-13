#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SàT plugin for import external blogs
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
from twisted.internet import defer
from twisted.web import client as web_client
from twisted.words.xish import domish
from sat.core import exceptions
from sat.tools import xml_tools
import collections
import os
import os.path
import tempfile
import urlparse
import uuid


PLUGIN_INFO = {
    "name": "blog import",
    "import_name": "BLOG_IMPORT",
    "type": C.PLUG_TYPE_BLOG,
    "dependencies": ["XEP-0060", "XEP-0277", "TEXT-SYNTAXES", "UPLOAD"],
    "main": "BlogImportPlugin",
    "handler": "no",
    "description": _(u"""Blog import management:
This plugin manage the different blog importers which can register to it, and handler generic importing tasks.""")
}

OPT_HOST = 'host'
OPT_UPLOAD_IMAGES = 'upload_images'
OPT_UPLOAD_IGNORE_HOST = 'upload_ignore_host'
OPT_IGNORE_TLS = 'ignore_tls_errors'
URL_REDIRECT_PREFIX = 'url_redirect_'
BOOL_OPTIONS = (OPT_UPLOAD_IMAGES, OPT_IGNORE_TLS)


BlogImporter = collections.namedtuple('BlogImporter', ('callback', 'short_desc', 'long_desc'))


class BlogImportPlugin(object):

    def __init__(self, host):
        log.info(_("plugin Blog Import initialization"))
        self.host = host
        self._importers = {}
        self._u = host.plugins['UPLOAD']
        self._p = host.plugins['XEP-0060']
        self._m = host.plugins['XEP-0277']
        self._s = self.host.plugins['TEXT-SYNTAXES']
        host.bridge.addMethod("blogImport", ".plugin", in_sign='ssa{ss}ss', out_sign='s', method=self._blogImport, async=True)
        host.bridge.addMethod("blogImportList", ".plugin", in_sign='', out_sign='a(ss)', method=self.listImporters)
        host.bridge.addMethod("blogImportDesc", ".plugin", in_sign='s', out_sign='(ss)', method=self.getDescription)

    def getProgress(self, progress_id, profile):
        client = self.host.getClient(profile)
        return client._blogImport_progress[progress_id]

    def listImporters(self):
        importers = self._importers.keys()
        importers.sort()
        return [(name, self._importers[name].short_desc) for name in self._importers]

    def getDescription(self, name):
        """Return import short and long descriptions

        @param name(unicode): blog importer name
        @return (tuple[unicode,unicode]): short and long description
        """
        try:
            importer = self._importers[name]
        except KeyError:
            raise exceptions.NotFound(u"Blog importer not found [{}]".format(name))
        else:
            return importer.short_desc, importer.long_desc

    def _blogImport(self, name, location, options, pubsub_service='', profile=C.PROF_KEY_DEFAULT):
        client = self.host.getClient(profile)
        options = {key: unicode(value) for key, value in options.iteritems()}
        for option in BOOL_OPTIONS:
            try:
                options[option] = C.bool(options[option])
            except KeyError:
                pass
        return self.blogImport(client, unicode(name), unicode(location), options)

    @defer.inlineCallbacks
    def blogImport(self, client, name, location, options=None, pubsub_service=None):
        """Import a blog

        @param name(unicode): name of the blog importer
        @param location(unicode): location of the blog data to import
            can be an url, a file path, or anything which make sense
            check importer description for more details
        @param options(dict, None): extra options. Below are the generic options,
            blog importer can have specific ones. All options have unicode values
            generic options:
                - OPT_HOST (unicode): original host
                - OPT_UPLOAD_IMAGES (bool): upload images to XMPP server if True
                    see OPT_UPLOAD_IGNORE_HOST.
                    Default: True
                - OPT_UPLOAD_IGNORE_HOST (unicode): don't upload images from this host
                - OPT_IGNORE_TLS (bool): ignore TLS error for image upload.
                    Default: False
        @param pubsub_service(jid.JID, None): jid of the PubSub service where blog must be imported
            None to use profile's server
        @return (unicode): progress id
        """
        if options is None:
            options = {}
        else:
            for opt_name, opt_default in ((OPT_UPLOAD_IMAGES, True),
                                          (OPT_IGNORE_TLS, False)):
                # we want an filled options dict, with all empty or False values removed
                try:
                    value =options[opt_name]
                except KeyError:
                    if opt_default:
                        options[opt_name] = opt_default
                else:
                    if not value:
                        del options[opt_name]
        try:
            importer = self._importers[name]
        except KeyError:
            raise exceptions.NotFound(u"Importer [{}] not found".format(name))
        posts_data, posts_count = yield importer.callback(client, location, options)
        url_redirect = {}
        progress_id = unicode(uuid.uuid4())
        try:
            progress_data = client._blogImport_progress
        except AttributeError:
            progress_data = client._blogImport_progress = {}
        progress_data[progress_id] = {u'position': '0'}
        if posts_count is not None:
            progress_data[progress_id]['size'] = unicode(posts_count)
        metadata = {'name': u'{}: {}'.format(name, location),
                    'direction': 'out',
                    'type': 'BLOG_IMPORT'
                   }
        self.host.registerProgressCb(progress_id, self.getProgress, metadata, profile=client.profile)
        self.host.bridge.progressStarted(progress_id, metadata, client.profile)
        self._recursiveImport(client, posts_data, progress_id, options, url_redirect)
        defer.returnValue(progress_id)

    @defer.inlineCallbacks
    def _recursiveImport(self, client, posts_data, progress_id, options, url_redirect, service=None, node=None, depth=0):
        """Do the upload recursively

        @param posts_data(list): list of data as specified in [register]
        @param options(dict): import options
        @param url_redirect(dict): link between former posts and new items
        @param service(jid.JID, None): PubSub service to use
        @param node(unicode, None): PubSub node to use
        @param depth(int): level of recursion
        """
        for idx, data in enumerate(posts_data):
            # data checks/filters
            mb_data = data['blog']
            try:
                item_id = mb_data['id']
            except KeyError:
                item_id = mb_data['id'] = unicode(uuid.uuid4())

            try:
                # we keep the link between old url and new blog item
                # so the user can redirect its former blog urls
                old_uri = data['url']
            except KeyError:
                pass
            else:
                new_uri = url_redirect[old_uri] = self._p.getNodeURI(
                    service if service is not None else client.jid.userhostJID(),
                    node or self._m.namespace,
                    item_id)
                log.info(u"url link from {old} to {new}".format(
                    old=old_uri, new=new_uri))

            yield self.blogFilters(client, mb_data, options)

            # comments data
            if len(data['comments']) != 1:
                raise NotImplementedError(u"can't manage multiple comment links")
            allow_comments = C.bool(mb_data.get('allow_comments', C.BOOL_FALSE))
            if allow_comments:
                comments_service, comments_node = self._m.getCommentsService(client), self._m.getCommentsNode(item_id)
                mb_data['comments_service'] = comments_service.full()
                mb_data['comments_node'] = comments_node
            else:
                if data['comments'][0]:
                    raise exceptions.DataError(u"allow_comments set to False, but comments are there")

            # post upload
            depth or log.debug(u"uploading item [{id}]: {title}".format(id=mb_data['id'], title=mb_data.get('title','')))
            yield self._m.send(mb_data, service, node, profile=client.profile)

            # comments upload
            depth or log.debug(u"uploading comments")
            if allow_comments:
                yield self._recursiveImport(client, data['comments'][0], progress_id, options, url_redirect, service=comments_service, node=comments_node, depth=depth+1)
            if depth == 0:
                client._blogImport_progress[progress_id]['position'] = unicode(idx+1)

        if depth == 0:
            self.host.bridge.progressFinished(progress_id,
                {u'{}{}'.format(URL_REDIRECT_PREFIX, old): new for old, new in url_redirect.iteritems()},
                client.profile)
            self.host.removeProgressCb(progress_id, client.profile)
            del client._blogImport_progress[progress_id]

    @defer.inlineCallbacks
    def blogFilters(self, client, mb_data, options):
        """Apply filters according to options

        modify mb_data in place
        @param posts_data(list[dict]): data as returned by importer callback
        @param options(dict): dict as given in [blogImport]
        """
        # FIXME: blog filters don't work on text content
        # TODO: text => XHTML conversion should handler links with <a/>
        #       filters can then be used by converting text to XHTML
        if not options:
            return

        # we want only XHTML content
        for prefix in ('content',): # a tuple is use, if title need to be added in the future
            try:
                rich = mb_data['{}_rich'.format(prefix)]
            except KeyError:
                pass
            else:
                if '{}_xhtml'.format(prefix) in mb_data:
                    raise exceptions.DataError(u"importer gave {prefix}_rich and {prefix}_xhtml at the same time, this is not allowed".format(prefix=prefix))
                # we convert rich syntax to XHTML here, so we can handle filters easily
                converted = yield self._s.convert(rich, self._s.getCurrentSyntax(client.profile), safe=False)
                mb_data['{}_xhtml'.format(prefix)] = converted
                del mb_data['{}_rich'.format(prefix)]

            try:
                mb_data['txt']
            except KeyError:
                pass
            else:
                if '{}_xhtml'.format(prefix) in mb_data:
                    log.warning(u"{prefix}_text will be replaced by converted {prefix}_xhtml, so filters can be handled".format(prefix=prefix))
                    del mb_data['{}_text'.format(prefix)]
                else:
                    log.warning(u"importer gave a text {prefix}, blog filters don't work on text {prefix}".format(prefix=prefix))
                    return

        # at this point, we have only XHTML version of content
        try:
            top_elt = xml_tools.ElementParser()(mb_data['content_xhtml'], namespace=C.NS_XHTML)
        except domish.ParserError:
            # we clean the xml and try again our luck
            cleaned = yield self._s.cleanXHTML(mb_data['content_xhtml'])
            top_elt = xml_tools.ElementParser()(cleaned, namespace=C.NS_XHTML)
        opt_host = options.get(OPT_HOST)
        if opt_host:
            # we normalise the domain
            parsed_host = urlparse.urlsplit(opt_host)
            opt_host = urlparse.urlunsplit((parsed_host.scheme or 'http', parsed_host.netloc or parsed_host.path, '', '', ''))

        tmp_dir = tempfile.mkdtemp()
        try:
            # TODO: would be nice to also update the hyperlinks to these images, e.g. when you have <a href="{url}"><img src="{url}"></a>
            for img_elt in xml_tools.findAll(top_elt, ['img']):
                yield self.imgFilters(client, img_elt, options, opt_host, tmp_dir)
        finally:
            os.rmdir(tmp_dir) # XXX: tmp_dir should be empty, or something went wrong

        # we now replace the content with filtered one
        mb_data['content_xhtml'] = top_elt.toXml()

    @defer.inlineCallbacks
    def imgFilters(self, client, img_elt, options, opt_host, tmp_dir):
        """Filters handling images

        url without host are fixed (if possible)
        according to options, images are uploaded to XMPP server
        @param img_elt(domish.Element): <img/> element to handle
        @param options(dict): filters options
        @param opt_host(unicode): normalised host given in options
        @param tmp_dir(str): path to temp directory
        """
        try:
            url = img_elt['src']
            if url[0] == u'/':
                if not opt_host:
                    log.warning(u"host was not specified, we can't deal with src without host ({url}) and have to ignore the following <img/>:\n{xml}"
                        .format(url=url, xml=img_elt.toXml()))
                    return
                else:
                    url = urlparse.urljoin(opt_host, url)
            filename = url.rsplit('/',1)[-1].strip()
            if not filename:
                raise KeyError
        except (KeyError, IndexError):
            log.warning(u"ignoring invalid img element: {}".format(img_elt.toXml()))
            return

        # we change the url for the normalized one
        img_elt['src'] = url

        if options.get(OPT_UPLOAD_IMAGES, False):
            # upload is requested
            try:
                ignore_host = options[OPT_UPLOAD_IGNORE_HOST]
            except KeyError:
                pass
            else:
                # host is the ignored one, we skip
                parsed_url = urlparse.urlsplit(url)
                if ignore_host in parsed_url.hostname:
                    log.info(u"Don't upload image at {url} because of {opt} option".format(
                        url=url, opt=OPT_UPLOAD_IGNORE_HOST))
                    return

            # we download images and re-upload them via XMPP
            tmp_file = os.path.join(tmp_dir, filename).encode('utf-8')
            upload_options = {'ignore_tls_errors': options.get(OPT_IGNORE_TLS, False)}

            try:
                yield web_client.downloadPage(url.encode('utf-8'), tmp_file)
                filename = filename.replace(u'%', u'_') # FIXME: tmp workaround for a bug in prosody http upload
                dummy, download_d = yield self._u.upload(client, tmp_file, filename, options=upload_options)
                download_url = yield download_d
            except Exception as e:
                log.warning(u"can't download image at {url}: {reason}".format(url=url, reason=e))
            else:
                img_elt['src'] = download_url

            try:
                os.unlink(tmp_file)
            except OSError:
                pass

    def register(self, name, callback, short_desc='', long_desc=''):
        """Register a blogImport method

        @param name(unicode): unique importer name, should indicate the blogging software it handler and always lowercase
        @param callback(callable): method to call:
            the signature must be (client, location, options) (cf. [blogImport])
            the importer must return a tuple with (posts_data, posts_count)

            posts_data is an iterable of dict which must have the following keys:
                'blog' (dict): microblog data of the blog post (cf. http://wiki.goffi.org/wiki/Bridge_API_-_Microblogging/en)
                    the importer MUST NOT create node or call XEP-0277 plugin itself
                    'comments*' key MUST NOT be used in this microblog_data, see bellow for comments
                    It is recommanded to use a unique id in the "id" key which is constant per blog item,
                    so if the import fail, a new import will overwrite the failed items and avoid duplicates.

                'comments' (list[list[dict]],None): Dictionaries must have the same keys as main item (i.e. 'blog' and 'comments')
                    a list of list is used because XEP-0277 can handler several comments nodes,
                    but in most cases, there will we only one item it the first list (something like [[{comment1_data},{comment2_data}, ...]])
                    blog['allow_comments'] must be True if there is any comment, and False (or not present) if comments are not allowed.
                    If allow_comments is False and some comments are present, a exceptions.DataError will be raised
            the import MAY optionally have the following keys:
                'url' (unicode): former url of the post (only the path, without host part)
                    if present the association to the new path will be displayed to user, so it can make redirections if necessary

            posts_count (int, None) indicate the total number of posts (without comments)
                useful to display a progress indicator when the iterator is a generator
                use None if you can't guess the total number of blog posts
        @param short_desc(unicode): one line description of the importer
        @param long_desc(unicode): long description of the importer, its options, etc.
        """
        name = name.lower()
        if name in self._importers:
            raise exceptions.ConflictError(u"A blog importer with the name {} already exsit".format(name))
        self._importers[name] = BlogImporter(callback, short_desc, long_desc)

    def unregister(self, name):
        del self._importers[name]
