#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT plugin for managing xep-0054
# Copyright (C) 2009-2016 Jérôme Poisson (goffi@goffi.org)
# Copyright (C) 2014 Emmanuel Gil Peyrot (linkmauve@linkmauve.fr)

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
from twisted.internet import threads, defer
from twisted.words.protocols.jabber import jid
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.words.xish import domish
from twisted.python.failure import Failure
import os.path

from zope.interface import implements

from wokkel import disco, iwokkel

from base64 import b64decode, b64encode
from hashlib import sha1
from sat.core import exceptions
from sat.memory import persistent
try:
    from PIL import Image
except:
    raise exceptions.MissingModule(u"Missing module pillow, please download/install it from https://python-pillow.github.io")
from cStringIO import StringIO

try:
    from twisted.words.protocols.xmlstream import XMPPHandler
except ImportError:
    from wokkel.subprotocols import XMPPHandler

AVATAR_PATH = "avatars"
AVATAR_DIM = (64, 64)

IQ_GET = '/iq[@type="get"]'
NS_VCARD = 'vcard-temp'
VCARD_REQUEST = IQ_GET + '/vCard[@xmlns="' + NS_VCARD + '"]'  # TODO: manage requests

PRESENCE = '/presence'
NS_VCARD_UPDATE = 'vcard-temp:x:update'
VCARD_UPDATE = PRESENCE + '/x[@xmlns="' + NS_VCARD_UPDATE + '"]'

CACHED_DATA = {'avatar', 'nick'}

PLUGIN_INFO = {
    "name": "XEP 0054 Plugin",
    "import_name": "XEP-0054",
    "type": "XEP",
    "protocols": ["XEP-0054", "XEP-0153"],
    "dependencies": [],
    "recommendations": ["XEP-0045"],
    "main": "XEP_0054",
    "handler": "yes",
    "description": _("""Implementation of vcard-temp""")
}


class XEP_0054(object):
    #TODO: - check that nickname is ok
    #      - refactor the code/better use of Wokkel
    #      - get missing values

    def __init__(self, host):
        log.info(_("Plugin XEP_0054 initialization"))
        self.host = host
        self.avatar_path = os.path.join(self.host.memory.getConfig('', 'local_dir'), AVATAR_PATH)
        if not os.path.exists(self.avatar_path):
            os.makedirs(self.avatar_path)
        self.cache = {}
        host.bridge.addMethod("getCard", ".plugin", in_sign='ss', out_sign='s', method=self._getCard)
        host.bridge.addMethod("getAvatarFile", ".plugin", in_sign='s', out_sign='s', method=self.getAvatarFile)
        host.bridge.addMethod("setAvatar", ".plugin", in_sign='ss', out_sign='', method=self.setAvatar, async=True)
        host.trigger.add("presence_available", self.presenceAvailableTrigger)
        host.memory.setSignalOnUpdate("avatar")
        host.memory.setSignalOnUpdate("nick")

    def getHandler(self, profile):
        return XEP_0054_handler(self)

    def presenceAvailableTrigger(self, presence_elt, client):
        if client.jid.userhost() in self.cache[client.profile]:
            try:
                avatar_hash = self.cache[client.profile][client.jid.userhost()]['avatar']
            except KeyError:
                log.info(u"No avatar in cache for {}".format(client.jid.userhost()))
                return True
            x_elt = domish.Element((NS_VCARD_UPDATE, 'x'))
            x_elt.addElement('photo', content=avatar_hash)
            presence_elt.addChild(x_elt)

        return True

    def isInRoom(self, entity_jid, profile):
        """Tell if an full jid is a member of a room

        @param entity_jid(jid.JID): full jid of the entity
        @return (bool): True if the bare jid of the entity is a room jid
        """
        try:
            return self.host.plugins['XEP-0045'].isRoom(entity_jid.userhostJID(), profile_key=profile)
        except KeyError:
            return False

    def _fillCachedValues(self, profile):
        #FIXME: this is really suboptimal, need to be reworked
        #       the current naive approach keeps a map between all jids of all profiles
        #       in persistent cache, then put avatar hashs in memory.
        #       Hashes should be shared between profiles
        for jid_s, data in self.cache[profile].iteritems():
            jid_ = jid.JID(jid_s)
            for name in CACHED_DATA:
                try:
                    self.host.memory.updateEntityData(jid_, name, data[name], silent=True, profile_key=profile)
                except KeyError:
                    pass

    @defer.inlineCallbacks
    def profileConnecting(self, profile):
        self.cache[profile] = persistent.PersistentBinaryDict(NS_VCARD, profile)
        yield self.cache[profile].load()
        self._fillCachedValues(profile)

    def profileDisconnected(self, profile):
        log.debug(u"Deleting profile cache for avatars")
        del self.cache[profile]

    def updateCache(self, jid_, name, value, profile):
        """update cache value

        save value in memory in case of change
        @param jid_(jid.JID): jid of the owner of the vcard
        @param name(str): name of the item which changed
        @param value(unicode): new value of the item
        @param profile(unicode): profile which received the update
        """
        if jid_.resource:
            if not self.isInRoom(jid_, profile):
                # VCard are retrieved with bare jid
                # but MUC room is a special case
                jid_ = jid.userhostJID()

        self.host.memory.updateEntityData(jid_, name, value, profile_key=profile)
        if name in CACHED_DATA:
            jid_s = jid_.userhost()
            self.cache[profile].setdefault(jid_s, {})[name] = value
            self.cache[profile].force(jid_s)

    def getCache(self, entity_jid, name, profile):
        """return cached value for jid

        @param entity_jid: target contact
        @param name: name of the value ('nick' or 'avatar')
        @param profile: %(doc_profile)s
        @return: wanted value or None"""
        if entity_jid.resource:
            if not self.isInRoom(entity_jid, profile):
                # VCard are retrieved with bare jid
                # but MUC room is a special case
                entity_jid = jid.userhostJID()
        try:
            data = self.host.memory.getEntityData(entity_jid, [name], profile)
        except exceptions.UnknownEntityError:
            return None
        return data.get(name)

    def _getFilename(self, hash_):
        """Get filename from hash

        @param hash_: hash of the avatar
        @return (str): absolute filename of the avatar
        """
        return os.path.join(self.avatar_path, hash_)

    def saveAvatarFile(self, data, hash_):
        """Save the avatar picture if it doesn't already exists

        @param data(str): binary image of the avatar
        @param hash_(str): hash of the binary data (will be used for the filename)
        """
        filename = self._getFilename(hash_)
        if not os.path.exists(filename):
            with open(filename, 'wb') as file_:
                file_.write(data)
            log.debug(_(u"file saved to %s") % hash_)
        else:
            log.debug(_(u"file [%s] already in cache") % hash_)

    def savePhoto(self, photo_xml):
        """Parse a <PHOTO> elem and save the picture"""
        for elem in photo_xml.elements():
            if elem.name == 'TYPE':
                log.debug(_(u'Photo of type [%s] found') % str(elem))
            if elem.name == 'BINVAL':
                log.debug(_('Decoding binary'))
                decoded = b64decode(str(elem))
                image_hash = sha1(decoded).hexdigest()
                self.saveAvatarFile(decoded, image_hash)
                return image_hash

    @defer.inlineCallbacks
    def vCard2Dict(self, vcard, target, profile):
        """Convert a VCard to a dict, and save binaries"""
        log.debug(_("parsing vcard"))
        dictionary = {}

        for elem in vcard.elements():
            if elem.name == 'FN':
                dictionary['fullname'] = unicode(elem)
            elif elem.name == 'NICKNAME':
                dictionary['nick'] = unicode(elem)
                self.updateCache(target, 'nick', dictionary['nick'], profile)
            elif elem.name == 'URL':
                dictionary['website'] = unicode(elem)
            elif elem.name == 'EMAIL':
                dictionary['email'] = unicode(elem)
            elif elem.name == 'BDAY':
                dictionary['birthday'] = unicode(elem)
            elif elem.name == 'PHOTO':
                dictionary["avatar"] = yield threads.deferToThread(self.savePhoto, elem)
                if not dictionary["avatar"]:  # can happen in case of e.g. empty photo elem
                    del dictionary['avatar']
                else:
                    self.updateCache(target, 'avatar', dictionary['avatar'], profile)
            else:
                log.info(_('FIXME: [%s] VCard tag is not managed yet') % elem.name)

        # if a data in cache doesn't exist anymore, we need to reset it
        # so we check CACHED_DATA no gotten (i.e. not in dictionary keys)
        # and we reset them
        for datum in CACHED_DATA.difference(dictionary.keys()):
            log.debug(u"reseting vcard datum [{datum}] for {entity}".format(datum=datum, entity=target.full()))
            self.updateCache(target, datum, '', profile)

        defer.returnValue(dictionary)

    def _VCardCb(self, answer, profile):
        """Called after the first get IQ"""
        log.debug(_("VCard found"))

        if answer.firstChildElement().name == "vCard":
            _jid, steam = self.host.getJidNStream(profile)
            try:
                from_jid = jid.JID(answer["from"])
            except KeyError:
                from_jid = _jid.userhostJID()
            d = self.vCard2Dict(answer.firstChildElement(), from_jid, profile)
            d.addCallback(lambda data: self.host.bridge.actionResult("RESULT", answer['id'], data, profile))
        else:
            log.error(_("FIXME: vCard not found as first child element"))
            self.host.bridge.actionResult("SUPPRESS", answer['id'], {}, profile)  # FIXME: maybe an error message would be better

    def _VCardEb(self, failure, profile):
        """Called when something is wrong with registration"""
        try:
            self.host.bridge.actionResult("SUPPRESS", failure.value.stanza['id'], {}, profile)  # FIXME: maybe an error message would be better
            log.warning(_(u"Can't find VCard of %s") % failure.value.stanza['from'])
            self.updateCache(jid.JID(failure.value.stanza['from']), "avatar", '', profile)
        except (AttributeError, KeyError):
            # 'ConnectionLost' object has no attribute 'stanza' + sometimes 'from' key doesn't exist
            log.warning(_(u"Can't find VCard: %s") % failure.getErrorMessage())

    def _getCard(self, target_s, profile_key=C.PROF_KEY_NONE):
        return self.getCard(jid.JID(target_s), profile_key)

    def getCard(self, target, profile_key=C.PROF_KEY_NONE):
        """Ask server for VCard

        @param target(jid.JID): jid from which we want the VCard
        @result: id to retrieve the profile
        """
        current_jid, xmlstream = self.host.getJidNStream(profile_key)
        if not xmlstream:
            raise exceptions.ProfileUnknownError('Asking vcard for a non-existant or not connected profile ({})'.format(profile_key))
        profile = self.host.memory.getProfileName(profile_key)
        to_jid = target.userhostJID()
        log.debug(_(u"Asking for %s's VCard") % to_jid.userhost())
        reg_request = IQ(xmlstream, 'get')
        reg_request["from"] = current_jid.full()
        reg_request["to"] = to_jid.userhost()
        reg_request.addElement('vCard', NS_VCARD)
        reg_request.send(to_jid.userhost()).addCallbacks(self._VCardCb, self._VCardEb, callbackArgs=[profile], errbackArgs=[profile])
        return reg_request["id"]

    def getAvatarFile(self, avatar_hash):
        """Give the full path of avatar from hash
        @param hash: SHA1 hash
        @return full_path
        """
        filename = self.avatar_path + '/' + avatar_hash
        if not os.path.exists(filename):
            log.error(_(u"Asking for an uncached avatar [%s]") % avatar_hash)
            return ""
        return filename

    def _buildSetAvatar(self, vcard_set, filepath):
        try:
            img = Image.open(filepath)
        except IOError:
            return Failure(exceptions.DataError("Can't open image"))

        if img.size != AVATAR_DIM:
            img.thumbnail(AVATAR_DIM, Image.ANTIALIAS)
            if img.size[0] != img.size[1]:  # we need to crop first
                left, upper = (0, 0)
                right, lower = img.size
                offset = abs(right - lower) / 2
                if right == min(img.size):
                    upper += offset
                    lower -= offset
                else:
                    left += offset
                    right -= offset
                img = img.crop((left, upper, right, lower))
        img_buf = StringIO()
        img.save(img_buf, 'PNG')

        vcard_elt = vcard_set.addElement('vCard', NS_VCARD)
        photo_elt = vcard_elt.addElement('PHOTO')
        photo_elt.addElement('TYPE', content='image/png')
        photo_elt.addElement('BINVAL', content=b64encode(img_buf.getvalue()))
        img_hash = sha1(img_buf.getvalue()).hexdigest()
        self.saveAvatarFile(img_buf.getvalue(), img_hash)
        return (vcard_set, img_hash)

    def setAvatar(self, filepath, profile_key=C.PROF_KEY_NONE):
        """Set avatar of the profile
        @param filepath: path of the image of the avatar"""
        #TODO: This is a temporary way of setting the avatar, as other VCard information is not managed.
        #      A proper full VCard management should be done (and more generaly a public/private profile)
        client = self.host.getClient(profile_key)

        vcard_set = IQ(client.xmlstream, 'set')
        d = threads.deferToThread(self._buildSetAvatar, vcard_set, filepath)

        def elementBuilt(result):
            """Called once the image is at the right size/format, and the vcard set element is build"""
            set_avatar_elt, img_hash = result
            self.updateCache(client.jid.userhostJID(), 'avatar', img_hash, client.profile)
            return set_avatar_elt.send().addCallback(lambda ignore: client.presence.available()) # FIXME: should send the current presence, not always "available" !

        d.addCallback(elementBuilt)

        return d


class XEP_0054_handler(XMPPHandler):
    implements(iwokkel.IDisco)

    def __init__(self, plugin_parent):
        self.plugin_parent = plugin_parent
        self.host = plugin_parent.host

    def connectionInitialized(self):
        self.xmlstream.addObserver(VCARD_UPDATE, self.update)

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        return [disco.DiscoFeature(NS_VCARD)]

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        return []

    def update(self, presence):
        """Called on <presence/> stanza with vcard data

        Check for avatar information, and get VCard if needed
        @param presend(domish.Element): <presence/> stanza
        """
        from_jid = jid.JID(presence['from'])
        if from_jid.resource and not self.plugin_parent.isInRoom(from_jid, self.parent.profile):
            from_jid = from_jid.userhostJID()
        #FIXME: wokkel's data_form should be used here
        try:
            x_elt = presence.elements(NS_VCARD_UPDATE, 'x').next()
        except StopIteration:
            return

        try:
            photo_elt = x_elt.elements(NS_VCARD_UPDATE, 'photo').next()
        except StopIteration:
            return

        hash_ = str(photo_elt)
        if not hash_:
            return
        old_avatar = self.plugin_parent.getCache(from_jid, 'avatar', self.parent.profile)
        filename = self.plugin_parent._getFilename(hash_)
        if not old_avatar or old_avatar != hash_:
            if os.path.exists(filename):
                log.debug(u"New avatar found for [{}], it's already in cache, we use it".format(from_jid.full()))
                self.plugin_parent.updateCache(from_jid, 'avatar', hash_, self.parent.profile)
            else:
                log.debug(u'New avatar found for [{}], requesting vcard'.format(from_jid.full()))
                self.plugin_parent.getCard(from_jid, self.parent.profile)
        else:
            if os.path.exists(filename):
                log.debug(u"avatar for {} already in cache".format(from_jid.full()))
            else:
                log.error(u"Avatar for [{}] should be in cache but it is not ! We get it".format(from_jid.full()))
                self.plugin_parent.getCard(from_jid, self.parent.profile)

