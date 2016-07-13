#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT: a jabber client
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

import sat
from sat.core.i18n import _, languageSwitch
from twisted.application import service
from twisted.internet import defer
from twisted.words.protocols.jabber import jid
from twisted.words.xish import domish
from twisted.internet import reactor
from wokkel.xmppim import RosterItem
from sat.bridge.DBus import DBusBridge
from sat.core import xmpp
from sat.core import exceptions
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.core.constants import Const as C
from sat.memory.memory import Memory
from sat.tools import trigger
from sat.tools import utils
from sat.stdui import ui_contact_list, ui_profile_manager
from glob import glob
from uuid import uuid4
import sys
import os.path
import uuid

try:
    from collections import OrderedDict # only available from python 2.7
except ImportError:
    from ordereddict import OrderedDict


class SAT(service.Service):

    def __init__(self):
        self._cb_map = {}  # map from callback_id to callbacks
        self._menus = OrderedDict()  # dynamic menus. key: callback_id, value: menu data (dictionnary)
        self.__private_data = {}  # used for internal callbacks (key = id) FIXME: to be removed
        self.initialised = defer.Deferred()
        self.profiles = {}
        self.plugins = {}

        self.memory = Memory(self)
        self.trigger = trigger.TriggerManager()  # trigger are used to change SàT behaviour

        try:
            self.bridge = DBusBridge()
        except exceptions.BridgeInitError:
            log.error(u"Bridge can't be initialised, can't start SàT core")
            sys.exit(1)
        self.bridge.register("getReady", lambda: self.initialised)
        self.bridge.register("getVersion", lambda: self.full_version)
        self.bridge.register("getFeatures", self.getFeatures)
        self.bridge.register("getProfileName", self.memory.getProfileName)
        self.bridge.register("getProfilesList", self.memory.getProfilesList)
        self.bridge.register("getEntityData", lambda jid_, keys, profile: self.memory.getEntityData(jid.JID(jid_), keys, profile))
        self.bridge.register("getEntitiesData", self.memory._getEntitiesData)
        self.bridge.register("asyncCreateProfile", self.memory.asyncCreateProfile)
        self.bridge.register("asyncDeleteProfile", self.memory.asyncDeleteProfile)
        self.bridge.register("profileStartSession", self.memory.startSession)
        self.bridge.register("profileIsSessionStarted", self.memory._isSessionStarted)
        self.bridge.register("profileSetDefault", self.memory.profileSetDefault)
        self.bridge.register("asyncConnect", self._asyncConnect)
        self.bridge.register("disconnect", self.disconnect)
        self.bridge.register("getContacts", self.getContacts)
        self.bridge.register("getContactsFromGroup", self.getContactsFromGroup)
        self.bridge.register("getMainResource", self.memory._getMainResource)
        self.bridge.register("getPresenceStatuses", self.memory._getPresenceStatuses)
        self.bridge.register("getWaitingSub", self.memory.getWaitingSub)
        self.bridge.register("getWaitingConf", self.getWaitingConf)
        self.bridge.register("sendMessage", self._sendMessage)
        self.bridge.register("getConfig", self._getConfig)
        self.bridge.register("setParam", self.setParam)
        self.bridge.register("getParamA", self.memory.getStringParamA)
        self.bridge.register("asyncGetParamA", self.memory.asyncGetStringParamA)
        self.bridge.register("asyncGetParamsValuesFromCategory", self.memory.asyncGetParamsValuesFromCategory)
        self.bridge.register("getParamsUI", self.memory.getParamsUI)
        self.bridge.register("getParamsCategories", self.memory.getParamsCategories)
        self.bridge.register("paramsRegisterApp", self.memory.paramsRegisterApp)
        self.bridge.register("getHistory", self.memory.getHistory)
        self.bridge.register("setPresence", self._setPresence)
        self.bridge.register("subscription", self.subscription)
        self.bridge.register("addContact", self._addContact)
        self.bridge.register("updateContact", self._updateContact)
        self.bridge.register("delContact", self._delContact)
        self.bridge.register("isConnected", self.isConnected)
        self.bridge.register("launchAction", self.launchCallback)
        self.bridge.register("actionsGet", self.actionsGet)
        self.bridge.register("confirmationAnswer", self.confirmationAnswer)
        self.bridge.register("progressGet", self._progressGet)
        self.bridge.register("progressGetAll", self._progressGetAll)
        self.bridge.register("getMenus", self.getMenus)
        self.bridge.register("getMenuHelp", self.getMenuHelp)
        self.bridge.register("discoInfos", self.memory.disco._discoInfos)
        self.bridge.register("discoItems", self.memory.disco._discoItems)
        self.bridge.register("saveParamsTemplate", self.memory.save_xml)
        self.bridge.register("loadParamsTemplate", self.memory.load_xml)

        self.memory.initialized.addCallback(self._postMemoryInit)

    @property
    def version(self):
        """Return the short version of SàT"""
        return C.APP_VERSION

    @property
    def full_version(self):
        """Return the full version of SàT (with extra data when in development mode)"""
        version = self.version
        if version[-1] == 'D':
            # we are in debug version, we add extra data
            try:
                return self._version_cache
            except AttributeError:
                self._version_cache = u"{} ({})".format(version, utils.getRepositoryData(sat))
                return self._version_cache
        else:
            return version

    def _postMemoryInit(self, ignore):
        """Method called after memory initialization is done"""
        log.info(_("Memory initialised"))
        self._import_plugins()
        ui_contact_list.ContactList(self)
        ui_profile_manager.ProfileManager(self)
        self.initialised.callback(None)
        log.info(_("Backend is ready"))

    def _import_plugins(self):
        """Import all plugins found in plugins directory"""
        import sat.plugins
        plugins_path = os.path.dirname(sat.plugins.__file__)
        plug_lst = [os.path.splitext(plugin)[0] for plugin in map(os.path.basename, glob(os.path.join(plugins_path, "plugin*.py")))]
        plugins_to_import = {}  # plugins we still have to import
        for plug in plug_lst:
            plugin_path = 'sat.plugins.' + plug
            try:
                __import__(plugin_path)
            except exceptions.MissingModule as e:
                try:
                    del sys.modules[plugin_path]
                except KeyError:
                    pass
                log.warning(u"Can't import plugin [{path}] because of an unavailale third party module:\n{msg}".format(
                    path=plugin_path, msg=e))
                continue
            except Exception as e:
                import traceback
                log.error(_(u"Can't import plugin [{path}]:\n{error}").format(path=plugin_path, error=traceback.format_exc()))
                continue
            mod = sys.modules[plugin_path]
            plugin_info = mod.PLUGIN_INFO
            import_name = plugin_info['import_name']
            if import_name in plugins_to_import:
                log.error(_(u"Name conflict for import name [{import_name}], can't import plugin [{name}]").format(**plugin_info))
                continue
            plugins_to_import[import_name] = (plugin_path, mod, plugin_info)
        while True:
            try:
                self._import_plugins_from_dict(plugins_to_import)
            except ImportError:
                pass
            if not plugins_to_import:
                break

    def _import_plugins_from_dict(self, plugins_to_import, import_name=None, optional=False):
        """Recursively import and their dependencies in the right order

        @param plugins_to_import(dict): key=import_name and values=(plugin_path, module, plugin_info)
        @param import_name(unicode, None): name of the plugin to import as found in PLUGIN_INFO['import_name']
        @param optional(bool): if False and plugin is not found, an ImportError exception is raised
        """
        if import_name in self.plugins:
            log.debug(u'Plugin {} already imported, passing'.format(import_name))
            return
        if not import_name:
            import_name, (plugin_path, mod, plugin_info) = plugins_to_import.popitem()
        else:
            if not import_name in plugins_to_import:
                if optional:
                    log.warning(_(u"Recommended plugin not found: {}").format(import_name))
                    return
                msg = u"Dependency not found: {}".format(import_name)
                log.error(msg)
                raise ImportError(msg)
            plugin_path, mod, plugin_info = plugins_to_import.pop(import_name)
        dependencies = plugin_info.setdefault("dependencies", [])
        recommendations = plugin_info.setdefault("recommendations", [])
        for to_import in dependencies + recommendations:
            if to_import not in self.plugins:
                log.debug(u'Recursively import dependency of [%s]: [%s]' % (import_name, to_import))
                try:
                    self._import_plugins_from_dict(plugins_to_import, to_import, to_import not in dependencies)
                except ImportError as e:
                    log.warning(_(u"Can't import plugin {name}: {error}").format(name=plugin_info['name'], error=e))
                    if optional:
                        return
                    raise e
        log.info("importing plugin: {}".format(plugin_info['name']))
        # we instanciate the plugin here
        try:
            self.plugins[import_name] = getattr(mod, plugin_info['main'])(self)
        except Exception as e:
            log.warning(u'Error while loading plugin "{name}", ignoring it: {error}'
                .format(name=plugin_info['name'], error=e))
            if optional:
                return
            raise ImportError(u"Error during initiation")
        if 'handler' in plugin_info and plugin_info['handler'] == 'yes':
            self.plugins[import_name].is_handler = True
        else:
            self.plugins[import_name].is_handler = False
        #TODO: test xmppclient presence and register handler parent

    def pluginsUnload(self):
        """Call unload method on every loaded plugin, if exists

        @return (D): A deferred which return None when all method have been called
        """
        # TODO: in the futur, it should be possible to hot unload a plugin
        #       pluging depending on the unloaded one should be unloaded too
        #       for now, just a basic call on plugin.unload is done
        defers_list = []
        for plugin in self.plugins.itervalues():
            try:
                unload = plugin.unload
            except AttributeError:
                continue
            else:
                defers_list.append(defer.maybeDeferred(unload))
        return defers_list

    def _asyncConnect(self, profile_key, password=''):
        profile = self.memory.getProfileName(profile_key)
        return self.asyncConnect(profile, password)

    def asyncConnect(self, profile, password='', max_retries=C.XMPP_MAX_RETRIES):
        """Retrieve the individual parameters, authenticate the profile
        and initiate the connection to the associated XMPP server.

        @param profile: %(doc_profile)s
        @param password (string): the SàT profile password
        @param max_retries (int): max number of connection retries
        @return (D(bool)):
            - True if the XMPP connection was already established
            - False if the XMPP connection has been initiated (it may still fail)
        @raise exceptions.PasswordError: Profile password is wrong
        """
        def connectXMPPClient(dummy=None):
            if self.isConnected(profile):
                log.info(_("already connected !"))
                return True
            d = self._connectXMPPClient(profile, max_retries)
            return d.addCallback(lambda dummy: False)

        d = self.memory.startSession(password, profile)
        d.addCallback(connectXMPPClient)
        return d

    @defer.inlineCallbacks
    def _connectXMPPClient(self, profile, max_retries):
        """This part is called from asyncConnect when we have loaded individual parameters from memory"""
        try:
            port = int(self.memory.getParamA(C.FORCE_PORT_PARAM, "Connection", profile_key=profile))
        except ValueError:
            log.debug(_("Can't parse port value, using default value"))
            port = None  # will use default value 5222 or be retrieved from a DNS SRV record

        password = yield self.memory.asyncGetParamA("Password", "Connection", profile_key=profile)
        current = self.profiles[profile] = xmpp.SatXMPPClient(self, profile,
            jid.JID(self.memory.getParamA("JabberID", "Connection", profile_key=profile)),
            password, self.memory.getParamA(C.FORCE_SERVER_PARAM, "Connection", profile_key=profile),
            port, max_retries)

        current.messageProt = xmpp.SatMessageProtocol(self)
        current.messageProt.setHandlerParent(current)

        current.roster = xmpp.SatRosterProtocol(self)
        current.roster.setHandlerParent(current)

        current.presence = xmpp.SatPresenceProtocol(self)
        current.presence.setHandlerParent(current)

        current.fallBack = xmpp.SatFallbackHandler(self)
        current.fallBack.setHandlerParent(current)

        current.versionHandler = xmpp.SatVersionHandler(C.APP_NAME_FULL,
                                                        self.full_version)
        current.versionHandler.setHandlerParent(current)

        current.identityHandler = xmpp.SatIdentityHandler()
        current.identityHandler.setHandlerParent(current)

        log.debug(_("setting plugins parents"))

        plugin_conn_cb = []
        for plugin in self.plugins.iteritems():
            if plugin[1].is_handler:
                plugin[1].getHandler(profile).setHandlerParent(current)
            connected_cb = getattr(plugin[1], "profileConnected", None) # profile connected is called after client is ready and roster is got
            if connected_cb:
                plugin_conn_cb.append((plugin[0], connected_cb))
            try:
                yield plugin[1].profileConnecting(profile) # profile connecting is called before actually starting client
            except AttributeError:
                pass

        current.startService()

        yield current.getConnectionDeferred()
        yield current.roster.got_roster  # we want to be sure that we got the roster

        # Call profileConnected callback for all plugins, and print error message if any of them fails
        conn_cb_list = []
        for dummy, callback in plugin_conn_cb:
            conn_cb_list.append(defer.maybeDeferred(callback, profile))
        list_d = defer.DeferredList(conn_cb_list)

        def logPluginResults(results):
            all_succeed = all([success for success, result in results])
            if not all_succeed:
                log.error(_(u"Plugins initialisation error"))
                for idx, (success, result) in enumerate(results):
                    if not success:
                        log.error(u"error (plugin %(name)s): %(failure)s" %
                                  {'name': plugin_conn_cb[idx][0], 'failure': result})

        yield list_d.addCallback(logPluginResults) # FIXME: we should have a timeout here, and a way to know if a plugin freeze
        # TODO: mesure launch time of each plugin

    def disconnect(self, profile_key):
        """disconnect from jabber server"""
        if not self.isConnected(profile_key):
            log.info(_("not connected !"))
            return
        profile = self.memory.getProfileName(profile_key)
        log.info(_("Disconnecting..."))
        self.profiles[profile].stopService()
        for plugin in self.plugins.iteritems():
            disconnected_cb = getattr(plugin[1], "profileDisconnected", None)
            if disconnected_cb:
                disconnected_cb(profile)

    def getFeatures(self, profile_key=C.PROF_KEY_NONE):
        """Get available features

        Return list of activated plugins and plugin specific data
        @param profile_key: %(doc_profile_key)s
            C.PROF_KEY_NONE can be used to have general plugins data (i.e. not profile dependent)
        @return (dict)[Deferred]: features data where:
            - key is plugin import name, present only for activated plugins
            - value is a an other dict, when meaning is specific to each plugin.
                this dict is return by plugin's getFeature method.
                If this method doesn't exists, an empty dict is returned.
        """
        try:
            # FIXME: there is no method yet to check profile session
            #        as soon as one is implemented, it should be used here
            self.getClient(profile_key)
        except KeyError:
            log.warning("Requesting features for a profile outside a session")
            profile_key = C.PROF_KEY_NONE
        except exceptions.ProfileNotSetError:
            pass

        features = []
        for import_name, plugin in self.plugins.iteritems():
            try:
                features_d = defer.maybeDeferred(plugin.getFeatures, profile_key)
            except AttributeError:
                features_d = defer.succeed({})
            features.append(features_d)

        d_list = defer.DeferredList(features)
        def buildFeatures(result, import_names):
            assert len(result) == len(import_names)
            ret = {}
            for name, (success, data) in zip (import_names, result):
                if success:
                    ret[name] = data
                else:
                    log.warning(u"Error while getting features for {name}: {failure}".format(
                        name=name, failure=data))
                    ret[name] = {}
            return ret

        d_list.addCallback(buildFeatures, self.plugins.keys())
        return d_list

    def getContacts(self, profile_key):
        client = self.getClient(profile_key)
        def got_roster(dummy):
            ret = []
            for item in client.roster.getItems():  # we get all items for client's roster
                # and convert them to expected format
                attr = client.roster.getAttributes(item)
                ret.append([item.jid.userhost(), attr, item.groups])
            return ret

        return client.roster.got_roster.addCallback(got_roster)

    def getContactsFromGroup(self, group, profile_key):
        client = self.getClient(profile_key)
        return [jid_.full() for jid_ in client.roster.getJidsFromGroup(group)]

    def purgeClient(self, profile):
        """Remove reference to a profile client and purge cache
        the garbage collector can then free the memory"""
        try:
            del self.profiles[profile]
        except KeyError:
            log.error(_("Trying to remove reference to a client not referenced"))
        self.memory.purgeProfileSession(profile)

    def startService(self):
        log.info(u"Salut à toi ô mon frère !")

    def stopService(self):
        log.info(u"Salut aussi à Rantanplan")
        return self.pluginsUnload()

    def run(self):
        log.debug(_("running app"))
        reactor.run()

    def stop(self):
        log.debug(_("stopping app"))
        reactor.stop()

    ## Misc methods ##

    def getJidNStream(self, profile_key):
        """Convenient method to get jid and stream from profile key
        @return: tuple (jid, xmlstream) from profile, can be None"""
        # TODO: deprecate this method (getClient is enough)
        profile = self.memory.getProfileName(profile_key)
        if not profile or not self.profiles[profile].isConnected():
            return (None, None)
        return (self.profiles[profile].jid, self.profiles[profile].xmlstream)

    def getClient(self, profile_key):
        """Convenient method to get client from profile key

        @return: client or None if it doesn't exist
        @raise exceptions.ProfileKeyUnknown: the profile or profile key doesn't exist
        @raise exceptions.NotFound: client is not available
            This happen if profile has not been use yet
        """
        profile = self.memory.getProfileName(profile_key)
        if not profile:
            raise exceptions.ProfileKeyUnknown
        try:
            return self.profiles[profile]
        except KeyError:
            raise exceptions.NotFound

    def getClients(self, profile_key):
        """Convenient method to get list of clients from profile key (manage list through profile_key like C.PROF_KEY_ALL)

        @param profile_key: %(doc_profile_key)s
        @return: list of clients
        """
        try:
            profile = self.memory.getProfileName(profile_key, True)
        except exceptions.ProfileUnknownError:
            return []
        if profile == C.PROF_KEY_ALL:
            return self.profiles.values()
        elif profile.count('@') > 1:
            raise exceptions.ProfileKeyUnknown
        return [self.profiles[profile]]

    def _getConfig(self, section, name):
        """Get the main configuration option

        @param section: section of the config file (None or '' for DEFAULT)
        @param name: name of the option
        @return: unicode representation of the option
        """
        return unicode(self.memory.getConfig(section, name, ''))

    ## Client management ##

    def setParam(self, name, value, category, security_limit, profile_key):
        """set wanted paramater and notice observers"""
        self.memory.setParam(name, value, category, security_limit, profile_key)

    def isConnected(self, profile_key):
        """Return connection status of profile
        @param profile_key: key_word or profile name to determine profile name
        @return: True if connected
        """
        profile = self.memory.getProfileName(profile_key)
        if not profile:
            log.error(_('asking connection status for a non-existant profile'))
            raise exceptions.ProfileUnknownError(profile_key)
        if profile not in self.profiles:
            return False
        return self.profiles[profile].isConnected()


    ## XMPP methods ##

    def getWaitingConf(self, profile_key=None):
        assert(profile_key)
        client = self.getClient(profile_key)
        ret = []
        for conf_id in client._waiting_conf:
            conf_type, data = client._waiting_conf[conf_id][:2]
            ret.append((conf_id, conf_type, data))
        return ret

    def generateMessageXML(self, mess_data):
        mess_data['xml'] = domish.Element((None, 'message'))
        mess_data['xml']["to"] = mess_data["to"].full()
        mess_data['xml']["from"] = mess_data['from'].full()
        mess_data['xml']["type"] = mess_data["type"]
        mess_data['xml']['id'] = str(uuid4())
        if mess_data["subject"]:
            mess_data['xml'].addElement("subject", None, mess_data['subject'])
        if mess_data["message"]: # message without body are used to send chat states
            mess_data['xml'].addElement("body", None, mess_data["message"])
        return mess_data

    def _sendMessage(self, to_s, msg, subject=None, mess_type='auto', extra={}, profile_key=C.PROF_KEY_NONE):
        to_jid = jid.JID(to_s)
        #XXX: we need to use the dictionary comprehension because D-Bus return its own types, and pickle can't manage them. TODO: Need to find a better way
        return self.sendMessage(to_jid, msg, subject, mess_type, {unicode(key): unicode(value) for key, value in extra.items()}, profile_key=profile_key)

    def sendMessage(self, to_jid, msg, subject=None, mess_type='auto', extra={}, no_trigger=False, profile_key=C.PROF_KEY_NONE):
        #FIXME: check validity of recipient
        profile = self.memory.getProfileName(profile_key)
        assert profile
        client = self.profiles[profile]
        if extra is None:
            extra = {}
        mess_data = {  # we put data in a dict, so trigger methods can change them
            "to": to_jid,
            "from": client.jid,
            "message": msg,
            "subject": subject,
            "type": mess_type,
            "extra": extra,
        }
        pre_xml_treatments = defer.Deferred() # XXX: plugin can add their pre XML treatments to this deferred
        post_xml_treatments = defer.Deferred() # XXX: plugin can add their post XML treatments to this deferred

        if mess_data["type"] == "auto":
            # we try to guess the type
            if mess_data["subject"]:
                mess_data["type"] = 'normal'
            elif not mess_data["to"].resource:  # if to JID has a resource, the type is not 'groupchat'
                # we may have a groupchat message, we check if the we know this jid
                try:
                    entity_type = self.memory.getEntityData(mess_data["to"], ['type'], profile)["type"]
                    #FIXME: should entity_type manage resources ?
                except (exceptions.UnknownEntityError, KeyError):
                    entity_type = "contact"

                if entity_type == "chatroom":
                    mess_data["type"] = 'groupchat'
                else:
                    mess_data["type"] = 'chat'
            else:
                mess_data["type"] == 'chat'
            mess_data["type"] == "chat" if mess_data["subject"] else "normal"

        send_only = mess_data['extra'].get('send_only', None)

        if not no_trigger and not send_only:
            if not self.trigger.point("sendMessage", mess_data, pre_xml_treatments, post_xml_treatments, profile):
                return defer.succeed(None)

        log.debug(_(u"Sending message (type {type}, to {to})").format(type=mess_data["type"], to=to_jid.full()))

        def cancelErrorTrap(failure):
            """A message sending can be cancelled by a plugin treatment"""
            failure.trap(exceptions.CancelError)

        pre_xml_treatments.addCallback(lambda dummy: self.generateMessageXML(mess_data))
        pre_xml_treatments.chainDeferred(post_xml_treatments)
        post_xml_treatments.addCallback(self._sendMessageToStream, client)
        if send_only:
            log.debug(_("Triggers, storage and echo have been inhibited by the 'send_only' parameter"))
        else:
            post_xml_treatments.addCallback(self._storeMessage, client)
            post_xml_treatments.addCallback(self.sendMessageToBridge, client)
            post_xml_treatments.addErrback(cancelErrorTrap)
        pre_xml_treatments.callback(mess_data)
        return pre_xml_treatments

    def _sendMessageToStream(self, mess_data, client):
        """Actualy send the message to the server

        @param mess_data: message data dictionnary
        @param client: profile's client
        """
        client.xmlstream.send(mess_data['xml'])
        return mess_data

    def _storeMessage(self, mess_data, client):
        """Store message into database (for local history)

        @param mess_data: message data dictionnary
        @param client: profile's client
        """
        if mess_data["type"] != "groupchat":
            # we don't add groupchat message to history, as we get them back
            # and they will be added then
            if mess_data['message']: # we need a message to save something
                self.memory.addToHistory(client.jid, mess_data['to'],
                                     unicode(mess_data["message"]),
                                     unicode(mess_data["type"]),
                                     mess_data['extra'],
                                     profile=client.profile)
            else:
               log.warning(_("No message found")) # empty body should be managed by plugins before this point
        return mess_data

    def sendMessageToBridge(self, mess_data, client):
        """Send message to bridge, so frontends can display it

        @param mess_data: message data dictionnary
        @param client: profile's client
        """
        if mess_data["type"] != "groupchat":
            # we don't send groupchat message back to bridge, as we get them back
            # and they will be added the
            if mess_data['message']: # we need a message to save something
                # We send back the message, so all clients are aware of it
                self.bridge.newMessage(mess_data['from'].full(),
                                       unicode(mess_data["message"]),
                                       mess_type=mess_data["type"],
                                       to_jid=mess_data['to'].full(),
                                       extra=mess_data['extra'],
                                       profile=client.profile)
            else:
               log.warning(_("No message found"))
        return mess_data

    def _setPresence(self, to="", show="", statuses=None, profile_key=C.PROF_KEY_NONE):
        return self.setPresence(jid.JID(to) if to else None, show, statuses, profile_key)

    def setPresence(self, to_jid=None, show="", statuses=None, profile_key=C.PROF_KEY_NONE):
        """Send our presence information"""
        if statuses is None:
            statuses = {}
        profile = self.memory.getProfileName(profile_key)
        assert profile
        priority = int(self.memory.getParamA("Priority", "Connection", profile_key=profile))
        self.profiles[profile].presence.available(to_jid, show, statuses, priority)
        #XXX: FIXME: temporary fix to work around openfire 3.7.0 bug (presence is not broadcasted to generating resource)
        if '' in statuses:
            statuses[C.PRESENCE_STATUSES_DEFAULT] = statuses.pop('')
        self.bridge.presenceUpdate(self.profiles[profile].jid.full(), show,
                                   int(priority), statuses, profile)

    def subscription(self, subs_type, raw_jid, profile_key):
        """Called to manage subscription
        @param subs_type: subsciption type (cf RFC 3921)
        @param raw_jid: unicode entity's jid
        @param profile_key: profile"""
        profile = self.memory.getProfileName(profile_key)
        assert profile
        to_jid = jid.JID(raw_jid)
        log.debug(_(u'subsciption request [%(subs_type)s] for %(jid)s') % {'subs_type': subs_type, 'jid': to_jid.full()})
        if subs_type == "subscribe":
            self.profiles[profile].presence.subscribe(to_jid)
        elif subs_type == "subscribed":
            self.profiles[profile].presence.subscribed(to_jid)
        elif subs_type == "unsubscribe":
            self.profiles[profile].presence.unsubscribe(to_jid)
        elif subs_type == "unsubscribed":
            self.profiles[profile].presence.unsubscribed(to_jid)

    def _addContact(self, to_jid_s, profile_key):
        return self.addContact(jid.JID(to_jid_s), profile_key)

    def addContact(self, to_jid, profile_key):
        """Add a contact in roster list"""
        profile = self.memory.getProfileName(profile_key)
        assert profile
        # presence is sufficient, as a roster push will be sent according to RFC 6121 §3.1.2
        self.profiles[profile].presence.subscribe(to_jid)

    def _updateContact(self, to_jid_s, name, groups, profile_key):
        return self.updateContact(jid.JID(to_jid_s), name, groups, profile_key)

    def updateContact(self, to_jid, name, groups, profile_key):
        """update a contact in roster list"""
        profile = self.memory.getProfileName(profile_key)
        assert profile
        groups = set(groups)
        roster_item = RosterItem(to_jid)
        roster_item.name = name or None
        roster_item.groups = set(groups)
        return self.profiles[profile].roster.setItem(roster_item)

    def _delContact(self, to_jid_s, profile_key):
        return self.delContact(jid.JID(to_jid_s), profile_key)

    def delContact(self, to_jid, profile_key):
        """Remove contact from roster list"""
        profile = self.memory.getProfileName(profile_key)
        assert profile
        self.profiles[profile].presence.unsubscribe(to_jid)  # is not asynchronous
        return self.profiles[profile].roster.removeItem(to_jid)

    ## Discovery ##
    # discovery methods are shortcuts to self.memory.disco
    # the main difference with client.disco is that self.memory.disco manage cache

    def hasFeature(self, *args, **kwargs):
        return self.memory.disco.hasFeature(*args, **kwargs)

    def checkFeature(self, *args, **kwargs):
        return self.memory.disco.checkFeature(*args, **kwargs)

    def checkFeatures(self, *args, **kwargs):
        return self.memory.disco.checkFeatures(*args, **kwargs)

    def getDiscoInfos(self, *args, **kwargs):
        return self.memory.disco.getInfos(*args, **kwargs)

    def getDiscoItems(self, *args, **kwargs):
        return self.memory.disco.getItems(*args, **kwargs)

    def findServiceEntities(self, *args, **kwargs):
        return self.memory.disco.findServiceEntities(*args, **kwargs)

    def findFeaturesSet(self, *args, **kwargs):
        return self.memory.disco.findFeaturesSet(*args, **kwargs)


    ## Generic HMI ##

    def actionResult(self, action_id, action_type, data, profile):
        """Send the result of an action
        @param action_id: same action_id used with action
        @param action_type: result action_type ("PARAM", "SUCCESS", "ERROR", "XMLUI")
        @param data: dictionary
        """
        self.bridge.actionResult(action_type, action_id, data, profile)

    def actionResultExt(self, action_id, action_type, data, profile):
        """Send the result of an action, extended version
        @param action_id: same action_id used with action
        @param action_type: result action_type /!\ only "DICT_DICT" for this method
        @param data: dictionary of dictionaries
        """
        if action_type != "DICT_DICT":
            log.error(_("action_type for actionResultExt must be DICT_DICT, fixing it"))
            action_type = "DICT_DICT"
        self.bridge.actionResultExt(action_type, action_id, data, profile)

    def askConfirmation(self, conf_id, conf_type, data, cb, profile):
        """Add a confirmation callback
        @param conf_id: conf_id used to get answer
        @param conf_type: confirmation conf_type ("YES/NO", "FILE_TRANSFER")
        @param data: data (depend of confirmation conf_type)
        @param cb: callback called with the answer
        """
        # FIXME: use XMLUI and *callback methods for dialog
        client = self.getClient(profile)
        if conf_id in client._waiting_conf:
            log.error(_("Attempt to register two callbacks for the same confirmation"))
        else:
            client._waiting_conf[conf_id] = (conf_type, data, cb)
            self.bridge.askConfirmation(conf_id, conf_type, data, profile)

    def confirmationAnswer(self, conf_id, accepted, data, profile):
        """Called by frontends to answer confirmation requests"""
        client = self.getClient(profile)
        log.debug(_(u"Received confirmation answer for conf_id [%(conf_id)s]: %(success)s") % {'conf_id': conf_id, 'success': _("accepted") if accepted else _("refused")})
        if conf_id not in client._waiting_conf:
            log.error(_(u"Received an unknown confirmation (%(id)s for %(profile)s)") % {'id': conf_id, 'profile': profile})
        else:
            cb = client._waiting_conf[conf_id][-1]
            del client._waiting_conf[conf_id]
            cb(conf_id, accepted, data, profile)

    def _killAction(self, keep_id, client):
        log.debug(u"Killing action {} for timeout".format(keep_id))
        client.actions[keep_id]

    def actionNew(self, action_data, security_limit=C.NO_SECURITY_LIMIT, keep_id=None, profile=C.PROF_KEY_NONE):
        """Shortcut to bridge.actionNew which generate and id and keep for retrieval

        @param action_data(dict): action data (see bridge documentation)
        @param security_limit: %(doc_security_limit)s
        @param keep_id(None, unicode): if not None, used to keep action for differed retrieval
            must be set to the callback_id
            action will be deleted after 30 min.
        @param profile: %(doc_profile)s
        """
        id_ = unicode(uuid.uuid4())
        if keep_id is not None:
            client = self.getClient(profile)
            action_timer = reactor.callLater(60*30, self._killAction, keep_id, client)
            client.actions[keep_id] = (action_data, id_, security_limit, action_timer)

        self.bridge.actionNew(action_data, id_, security_limit, profile)

    def actionsGet(self, profile):
        """Return current non answered actions

        @param profile: %(doc_profile)s
        """
        client = self.getClient(profile)
        return [action_tuple[:-1] for action_tuple in client.actions.itervalues()]

    def registerProgressCb(self, progress_id, callback, metadata=None, profile=C.PROF_KEY_NONE):
        """Register a callback called when progress is requested for id"""
        if metadata is None:
            metadata = {}
        client = self.getClient(profile)
        if progress_id in client._progress_cb:
            raise exceptions.ConflictError(u"Progress ID is not unique !")
        client._progress_cb[progress_id] = (callback, metadata)

    def removeProgressCb(self, progress_id, profile):
        """Remove a progress callback"""
        client = self.getClient(profile)
        try:
            del client._progress_cb[progress_id]
        except KeyError:
            log.error(_(u"Trying to remove an unknow progress callback"))

    def _progressGet(self, progress_id, profile):
        data = self.progressGet(progress_id, profile)
        return {k: unicode(v) for k,v in data.iteritems()}

    def progressGet(self, progress_id, profile):
        """Return a dict with progress information

        @param progress_id(unicode): unique id of the progressing element
        @param profile: %(doc_profile)s
        @return (dict): data with the following keys:
            'position' (int): current possition
            'size' (int): end_position
            if id doesn't exists (may be a finished progression), and empty dict is returned
        """
        client = self.getClient(profile)
        try:
            data = client._progress_cb[progress_id][0](progress_id, profile)
        except KeyError:
            data = {}
        return data

    def _progressGetAll(self, profile_key):
        progress_all = self.progressGetAll(profile_key)
        for profile, progress_dict in progress_all.iteritems():
            for progress_id, data in progress_dict.iteritems():
                for key, value in data.iteritems():
                    data[key] = unicode(value)
        return progress_all

    def progressGetAllMetadata(self, profile_key):
        """Return all progress metadata at once

        @param profile_key: %(doc_profile)s
            if C.PROF_KEY_ALL is used, all progress metadata from all profiles are returned
        @return (dict[dict[dict]]): a dict which map profile to progress_dict
            progress_dict map progress_id to progress_data
            progress_metadata is the same dict as sent by [progressStarted]
        """
        clients = self.getClients(profile_key)
        progress_all = {}
        for client in clients:
            profile = client.profile
            progress_dict = {}
            progress_all[profile] = progress_dict
            for progress_id, (dummy, progress_metadata) in client._progress_cb.iteritems():
                progress_dict[progress_id] = progress_metadata
        return progress_all

    def progressGetAll(self, profile_key):
        """Return all progress status at once

        @param profile_key: %(doc_profile)s
            if C.PROF_KEY_ALL is used, all progress status from all profiles are returned
        @return (dict[dict[dict]]): a dict which map profile to progress_dict
            progress_dict map progress_id to progress_data
            progress_data is the same dict as returned by [progressGet]
        """
        clients = self.getClients(profile_key)
        progress_all = {}
        for client in clients:
            profile = client.profile
            progress_dict = {}
            progress_all[profile] = progress_dict
            for progress_id, (progress_cb, dummy) in client._progress_cb.iteritems():
                progress_dict[progress_id] = progress_cb(progress_id, profile)
        return progress_all

    def registerCallback(self, callback, *args, **kwargs):
        """Register a callback.

        Use with_data=True in kwargs if the callback use the optional data dict
        use force_id=id to avoid generated id. Can lead to name conflict, avoid if possible
        use one_shot=True to delete callback once it have been called
        @param callback: any callable
        @return: id of the registered callback
        """
        callback_id = kwargs.pop('force_id', None)
        if callback_id is None:
            callback_id = str(uuid4())
        else:
            if callback_id in self._cb_map:
                raise exceptions.ConflictError(_(u"id already registered"))
        self._cb_map[callback_id] = (callback, args, kwargs)

        if "one_shot" in kwargs: # One Shot callback are removed after 30 min
            def purgeCallback():
                try:
                    self.removeCallback(callback_id)
                except KeyError:
                    pass
            reactor.callLater(1800, purgeCallback)

        return callback_id

    def removeCallback(self, callback_id):
        """ Remove a previously registered callback
        @param callback_id: id returned by [registerCallback] """
        log.debug("Removing callback [%s]" % callback_id)
        del self._cb_map[callback_id]

    def launchCallback(self, callback_id, data=None, profile_key=C.PROF_KEY_NONE):
        """Launch a specific callback
        @param callback_id: id of the action (callback) to launch
        @param data: optional data
        @profile_key: %(doc_profile_key)s
        @return: a deferred which fire a dict where key can be:
            - xmlui: a XMLUI need to be displayed
            - validated: if present, can be used to launch a callback, it can have the values
                - C.BOOL_TRUE
                - C.BOOL_FALSE
        """
        try:
            client = self.getClient(profile_key)
        except exceptions.NotFound:
            # client is not available yet
            profile = self.memory.getProfileName(profile_key)
            if not profile:
                raise exceptions.ProfileUnknownError(_('trying to launch action with a non-existant profile'))
        else:
            profile = client.profile
            # we check if the action is kept, and remove it
            try:
                action_tuple = client.actions[callback_id]
            except KeyError:
                pass
            else:
                action_tuple[-1].cancel() # the last item is the action timer
                del client.actions[callback_id]

        try:
            callback, args, kwargs = self._cb_map[callback_id]
        except KeyError:
            raise exceptions.DataError(u"Unknown callback id {}".format(callback_id))

        if kwargs.get("with_data", False):
            if data is None:
                raise exceptions.DataError("Required data for this callback is missing")
            args,kwargs=list(args)[:],kwargs.copy() # we don't want to modify the original (kw)args
            args.insert(0, data)
            kwargs["profile"] = profile
            del kwargs["with_data"]

        if kwargs.pop('one_shot', False):
            self.removeCallback(callback_id)

        return defer.maybeDeferred(callback, *args, **kwargs)

    #Menus management

    def importMenu(self, path, callback, security_limit=C.NO_SECURITY_LIMIT, help_string="", type_=C.MENU_GLOBAL):
        """register a new menu for frontends
        @param path: path to go to the menu (category/subcategory/.../item), must be an iterable (e.g.: ("File", "Open"))
            /!\ use D_() instead of _() for translations (e.g. (D_("File"), D_("Open")))
        @param callback: method to be called when menuitem is selected, callable or a callback id (string) as returned by [registerCallback]
        @param security_limit: %(doc_security_limit)s
            /!\ security_limit MUST be added to data in launchCallback if used #TODO
        @param help_string: string used to indicate what the menu do (can be show as a tooltip).
            /!\ use D_() instead of _() for translations
        @param type: one of:
            - C.MENU_GLOBAL: classical menu, can be shown in a menubar on top (e.g. something like File/Open)
            - C.MENU_ROOM: like a global menu, but only shown in multi-user chat
                menu_data must contain a "room_jid" data
            - C.MENU_SINGLE: like a global menu, but only shown in one2one chat
                menu_data must contain a "jid" data
            - C.MENU_JID_CONTEXT: contextual menu, used with any jid (e.g.: ad hoc commands, jid is already filled)
                menu_data must contain a "jid" data
            - C.MENU_ROSTER_JID_CONTEXT: like JID_CONTEXT, but restricted to jids in roster.
                menu_data must contain a "room_jid" data
            - C.MENU_ROSTER_GROUP_CONTEXT: contextual menu, used with group (e.g.: publish microblog, group is already filled)
                menu_data must contain a "group" data
        @return: menu_id (same as callback_id)
        """

        if callable(callback):
            callback_id = self.registerCallback(callback, with_data=True)
        elif isinstance(callback, basestring):
            # The callback is already registered
            callback_id = callback
            try:
                callback, args, kwargs = self._cb_map[callback_id]
            except KeyError:
                raise exceptions.DataError("Unknown callback id")
            kwargs["with_data"] = True # we have to be sure that we use extra data
        else:
            raise exceptions.DataError("Unknown callback type")

        for menu_data in self._menus.itervalues():
            if menu_data['path'] == path and menu_data['type'] == type_:
                raise exceptions.ConflictError(_("A menu with the same path and type already exists"))

        menu_data = {'path': path,
                     'security_limit': security_limit,
                     'help_string': help_string,
                     'type': type_
                    }

        self._menus[callback_id] = menu_data

        return callback_id

    def getMenus(self, language='', security_limit=C.NO_SECURITY_LIMIT):
        """Return all menus registered

        @param language: language used for translation, or empty string for default
        @param security_limit: %(doc_security_limit)s
        @return: array of tuple with:
            - menu id (same as callback_id)
            - menu type
            - raw menu path (array of strings)
            - translated menu path
            - extra (dict(unicode, unicode)): extra data where key can be:
                - icon: name of the icon to use (TODO)
                - help_url: link to a page with more complete documentation (TODO)
        """
        ret = []
        for menu_id, menu_data in self._menus.iteritems():
            type_ = menu_data['type']
            path = menu_data['path']
            menu_security_limit = menu_data['security_limit']
            if security_limit!=C.NO_SECURITY_LIMIT and (menu_security_limit==C.NO_SECURITY_LIMIT or menu_security_limit>security_limit):
                continue
            languageSwitch(language)
            path_i18n = [_(elt) for elt in path]
            languageSwitch()
            extra = {} # TODO: manage extra data like icon
            ret.append((menu_id, type_, path, path_i18n, extra))

        return ret

    def getMenuHelp(self, menu_id, language=''):
        """
        return the help string of the menu
        @param menu_id: id of the menu (same as callback_id)
        @param language: language used for translation, or empty string for default
        @param return: translated help

        """
        try:
            menu_data = self._menus[menu_id]
        except KeyError:
            raise exceptions.DataError("Trying to access an unknown menu")
        languageSwitch(language)
        help_string = _(menu_data['help_string'])
        languageSwitch()
        return help_string
