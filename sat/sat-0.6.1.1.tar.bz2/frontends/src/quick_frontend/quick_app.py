#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# helper class for making a SAT frontend
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

from sat.core.log import getLogger
log = getLogger(__name__)

from sat.core.i18n import _
from sat.core import exceptions
from sat.tools import trigger

from sat_frontends.tools import jid
from sat_frontends.quick_frontend import quick_widgets
from sat_frontends.quick_frontend import quick_menus
from sat_frontends.quick_frontend import quick_blog
from sat_frontends.quick_frontend import quick_chat, quick_games
from sat_frontends.quick_frontend.constants import Const as C

import sys
from collections import OrderedDict

try:
    # FIXME: to be removed when an acceptable solution is here
    unicode('')  # XXX: unicode doesn't exist in pyjamas
except (TypeError, AttributeError):  # Error raised is not the same depending on pyjsbuild options
    unicode = str


class ProfileManager(object):
    """Class managing all data relative to one profile, and plugging in mechanism"""
    host = None
    bridge = None
    cache_keys_to_get = ['avatar']

    def __init__(self, profile):
        self.profile = profile
        self.whoami = None
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def plug(self):
        """Plug the profile to the host"""
        # we get the essential params
        self.bridge.asyncGetParamA("JabberID", "Connection", profile_key=self.profile,
                                   callback=self._plug_profile_jid, errback=self._getParamError)

    def _plug_profile_jid(self, jid_s):
        self.whoami = jid.JID(jid_s)  # resource might change after the connection
        self.bridge.asyncGetParamA("autoconnect", "Connection", profile_key=self.profile,
                                   callback=self._plug_profile_autoconnect, errback=self._getParamError)

    def _plug_profile_autoconnect(self, value_str):
        autoconnect = C.bool(value_str)
        if autoconnect and not self.bridge.isConnected(self.profile):
            self.host.asyncConnect(self.profile, callback=lambda dummy: self._plug_profile_afterconnect())
        else:
            self._plug_profile_afterconnect()

    def _plug_profile_afterconnect(self):
        # Profile can be connected or not
        # we get cached data
        self.host.bridge.getFeatures(profile_key=self.profile, callback=self._plug_profile_getFeaturesCb, errback=self._plug_profile_getFeaturesEb)

    def _plug_profile_getFeaturesEb(self, failure):
        log.error(u"Couldn't get features: {}".format(failure))
        self._plug_profile_getFeaturesCb({})

    def _plug_profile_getFeaturesCb(self, features):
        self.host.features = features
        self.host.bridge.getEntitiesData([], ProfileManager.cache_keys_to_get, profile=self.profile, callback=self._plug_profile_gotCachedValues, errback=self._plug_profile_failedCachedValues)

    def _plug_profile_failedCachedValues(self, failure):
        log.error(u"Couldn't get cached values: {}".format(failure))
        self._plug_profile_gotCachedValues({})

    def _plug_profile_gotCachedValues(self, cached_values):
        # add the contact list and its listener
        contact_list = self.host.addContactList(self.profile)
        self.host.contact_lists[self.profile] = contact_list

        for entity, data in cached_values.iteritems():
            for key, value in data.iteritems():
                contact_list.setCache(jid.JID(entity), key, value)

        if not self.bridge.isConnected(self.profile):
            self.host.setPresenceStatus(C.PRESENCE_UNAVAILABLE, '', profile=self.profile)
        else:

            contact_list.fill()
            self.host.setPresenceStatus(profile=self.profile)

            #The waiting subscription requests
            self.bridge.getWaitingSub(self.profile, callback=self._plug_profile_gotWaitingSub)

    def _plug_profile_gotWaitingSub(self, waiting_sub):
        for sub in waiting_sub:
            self.host.subscribeHandler(waiting_sub[sub], sub, self.profile)

        self.bridge.getRoomsJoined(self.profile, callback=self._plug_profile_gotRoomsJoined)

    def _plug_profile_gotRoomsJoined(self, rooms_args):
        #Now we open the MUC window where we already are:
        for room_args in rooms_args:
            self.host.roomJoinedHandler(*room_args, profile=self.profile)

        self.bridge.getRoomsSubjects(self.profile, callback=self._plug_profile_gotRoomsSubjects)

    def _plug_profile_gotRoomsSubjects(self, subjects_args):
        for subject_args in subjects_args:
            self.host.roomNewSubjectHandler(*subject_args, profile=self.profile)

        #Presence must be requested after rooms are filled
        self.host.bridge.getPresenceStatuses(self.profile, callback=self._plug_profile_gotPresences)

    def _plug_profile_gotPresences(self, presences):
        def gotEntityData(data, contact):
            for key in ('avatar', 'nick'):
                if key in data:
                    self.host.entityDataUpdatedHandler(contact, key, data[key], self.profile)

        for contact in presences:
            for res in presences[contact]:
                jabber_id = ('%s/%s' % (jid.JID(contact).bare, res)) if res else contact
                show = presences[contact][res][0]
                priority = presences[contact][res][1]
                statuses = presences[contact][res][2]
                self.host.presenceUpdateHandler(jabber_id, show, priority, statuses, self.profile)
            self.host.bridge.getEntityData(contact, ['avatar', 'nick'], self.profile, callback=lambda data, contact=contact: gotEntityData(data, contact), errback=lambda failure, contact=contact: log.debug(u"No cache data for {}".format(contact)))

        #Finaly, we get the waiting confirmation requests
        self.bridge.getWaitingConf(self.profile, callback=self._plug_profile_gotWaitingConf)

    def _plug_profile_gotWaitingConf(self, waiting_confs):
        for confirm_id, confirm_type, data in waiting_confs:
            self.host.askConfirmationHandler(confirm_id, confirm_type, data, self.profile)

        # At this point, profile should be fully plugged
        # and we launch frontend specific method
        self.host.profilePlugged(self.profile)

    def _getParamError(self, ignore):
        log.error(_("Can't get profile parameter"))


class ProfilesManager(object):
    """Class managing collection of profiles"""

    def __init__(self):
        self._profiles = {}

    def __contains__(self, profile):
        return profile in self._profiles

    def __iter__(self):
        return self._profiles.iterkeys()

    def __getitem__(self, profile):
        return self._profiles[profile]

    def __len__(self):
        return len(self._profiles)

    def plug(self, profile):
        if profile in self._profiles:
            raise exceptions.ConflictError('A profile of the name [{}] is already plugged'.format(profile))
        self._profiles[profile] = ProfileManager(profile)
        self._profiles[profile].plug()

    def unplug(self, profile):
        if profile not in self._profiles:
            raise ValueError('The profile [{}] is not plugged'.format(profile))

        # remove the contact list and its listener
        host = self._profiles[profile].host
        host.contact_lists[profile].onDelete()
        del host.contact_lists[profile]

        del self._profiles[profile]

    def chooseOneProfile(self):
        return self._profiles.keys()[0]


class QuickApp(object):
    """This class contain the main methods needed for the frontend"""
    MB_HANDLE = True # Set to false if the frontend doesn't manage microblog

    def __init__(self, create_bridge, xmlui, check_options=None):
        """Create a frontend application

        @param create_bridge: method to use to create the Bridge
        @param xmlui: xmlui module
        @param check_options: method to call to check options (usually command line arguments)
        """
        self.xmlui = xmlui
        self.menus = quick_menus.QuickMenusManager(self)
        ProfileManager.host = self
        self.profiles = ProfilesManager()
        self.ready_profiles = set() # profiles which are connected and ready
        self.signals_cache = {} # used to keep signal received between start of plug_profile and when the profile is actualy ready
        self.contact_lists = {}
        self.widgets = quick_widgets.QuickWidgetsManager(self)
        if check_options is not None:
            self.options = check_options()
        else:
            self.options = None

        # widgets
        self.selected_widget = None # widget currently selected (must be filled by frontend)

        # listeners
        self._listeners = {} # key: listener type ("avatar", "selected", etc), value: list of callbacks

        # triggers
        self.trigger = trigger.TriggerManager()  # trigger are used to change the default behaviour

        ## bridge ##
        try:
            self.bridge = create_bridge()
        except exceptions.BridgeExceptionNoService:
            print(_(u"Can't connect to SàT backend, are you sure it's launched ?"))
            sys.exit(1)
        except exceptions.BridgeInitError:
            print(_(u"Can't init bridge"))
            sys.exit(1)
        ProfileManager.bridge = self.bridge
        self.registerSignal("connected")
        self.registerSignal("disconnected")
        self.registerSignal("actionNew")
        self.registerSignal("newContact")
        self.registerSignal("newMessage")
        self.registerSignal("newAlert")
        self.registerSignal("presenceUpdate")
        self.registerSignal("subscribe")
        self.registerSignal("paramUpdate")
        self.registerSignal("contactDeleted")
        self.registerSignal("entityDataUpdated")
        self.registerSignal("askConfirmation")
        self.registerSignal("actionResult")
        self.registerSignal("progressStarted")
        self.registerSignal("progressFinished")
        self.registerSignal("progressError")
        self.registerSignal("actionResultExt", self.actionResultHandler)
        self.registerSignal("roomJoined", iface="plugin")
        self.registerSignal("roomLeft", iface="plugin")
        self.registerSignal("roomUserJoined", iface="plugin")
        self.registerSignal("roomUserLeft", iface="plugin")
        self.registerSignal("roomUserChangedNick", iface="plugin")
        self.registerSignal("roomNewSubject", iface="plugin")
        self.registerSignal("chatStateReceived", iface="plugin")
        self.registerSignal("psEvent", iface="plugin")

        # FIXME: do it dynamically
        quick_games.Tarot.registerSignals(self)
        quick_games.Quiz.registerSignals(self)
        quick_games.Radiocol.registerSignals(self)

        self.current_action_ids = set() # FIXME: to be removed
        self.current_action_ids_cb = {} # FIXME: to be removed
        self.media_dir = self.bridge.getConfig('', 'media_dir')
        self.features = None

    @property
    def current_profile(self):
        """Profile that a user would expect to use"""
        try:
            return self.selected_widget.profile
        except (TypeError, AttributeError):
            return self.profiles.chooseOneProfile()

    @property
    def visible_widgets(self):
        """widgets currently visible (must be implemented by frontend)"""
        raise NotImplementedError

    @property
    def alerts_count(self):
        """Count the over whole alerts for all contact lists"""
        return sum([sum(clist._alerts.values()) for clist in self.contact_lists.values()])

    def registerSignal(self, function_name, handler=None, iface="core", with_profile=True):
        """Register a handler for a signal

        @param function_name (str): name of the signal to handle
        @param handler (instancemethod): method to call when the signal arrive, None for calling an automatically named handler (function_name + 'Handler')
        @param iface (str): interface of the bridge to use ('core' or 'plugin')
        @param with_profile (boolean): True if the signal concerns a specific profile, in that case the profile name has to be passed by the caller
        """
        if handler is None:
            handler = getattr(self, "{}{}".format(function_name, 'Handler'))
        if not with_profile:
            self.bridge.register(function_name, handler, iface)
            return

        def signalReceived(*args, **kwargs):
            profile = kwargs.get('profile')
            if profile is None:
                if not args:
                    raise exceptions.ProfileNotSetError
                profile = args[-1]
            if profile is not None:
                if not self.check_profile(profile):
                    if profile in self.profiles:
                        # profile is not ready but is in self.profiles, that's mean that it's being connecting and we need to cache the signal
                        self.signals_cache.setdefault(profile, []).append((function_name, handler, args, kwargs))
                    return  # we ignore signal for profiles we don't manage
            handler(*args, **kwargs)
        self.bridge.register(function_name, signalReceived, iface)

    def addListener(self, type_, callback, profiles_filter=None):
        """Add a listener for an event

        /!\ don't forget to remove listener when not used anymore (e.g. if you delete a widget)
        @param type_: type of event, can be:
            - avatar: called when avatar data is updated
                args: (entity, avatar file, profile)
            - nick: called when nick data is updated
                args: (entity, new_nick, profile)
            - presence: called when a presence is received
                args: (entity, show, priority, statuses, profile)
            - menu: called when a menu item is added or removed
                args: (type_, path, path_i18n, item) were values are:
                    type_: same as in [sat.core.sat_main.SAT.importMenu]
                    path: same as in [sat.core.sat_main.SAT.importMenu]
                    path_i18n: translated path (or None if the item is removed)
                    item: instance of quick_menus.MenuItemBase or None if the item is removed
            - gotMenus: called only once when menu are available (no arg)
        @param callback: method to call on event
        @param profiles_filter (set[unicode]): if set and not empty, the
            listener will be callable only by one of the given profiles.
        """
        assert type_ in C.LISTENERS
        self._listeners.setdefault(type_, OrderedDict())[callback] = profiles_filter

    def removeListener(self, type_, callback):
        """Remove a callback from listeners

        @param type_: same as for [addListener]
        @param callback: callback to remove
        """
        assert type_ in C.LISTENERS
        self._listeners[type_].pop(callback)

    def callListeners(self, type_, *args, **kwargs):
        """Call the methods which listen type_ event. If a profiles filter has
        been register with a listener and profile argument is not None, the
        listener will be called only if profile is in the profiles filter list.

        @param type_: same as for [addListener]
        @param *args: arguments sent to callback
        @param **kwargs: keywords argument, mainly used to pass "profile" when needed
        """
        assert type_ in C.LISTENERS
        try:
            listeners = self._listeners[type_]
        except KeyError:
            pass
        else:
            profile = kwargs.get("profile")
            for listener, profiles_filter in listeners.iteritems():
                if profile is None or not profiles_filter or profile in profiles_filter:
                    listener(*args, **kwargs)

    def check_profile(self, profile):
        """Tell if the profile is currently followed by the application, and ready"""
        return profile in self.ready_profiles

    def postInit(self, profile_manager):
        """Must be called after initialization is done, do all automatic task (auto plug profile)

        @param profile_manager: instance of a subclass of Quick_frontend.QuickProfileManager
        """
        if self.options and self.options.profile:
            profile_manager.autoconnect([self.options.profile])

    def profilePlugged(self, profile):
        """Method called when the profile is fully plugged, to launch frontend specific workflow

        /!\ if you override the method and don't call the parent, be sure to add the profile to ready_profiles !
            if you don't, all signals will stay in cache

        @param profile(unicode): %(doc_profile)s
        """
        self.ready_profiles.add(profile)

        # profile is ready, we can call send signals that where is cache
        cached_signals = self.signals_cache.pop(profile, [])
        for function_name, handler, args, kwargs in cached_signals:
            log.debug(u"Calling cached signal [%s] with args %s and kwargs %s" % (function_name, args, kwargs))
            handler(*args, **kwargs)

        self.callListeners('profilePlugged', profile=profile)

    def asyncConnect(self, profile, callback=None, errback=None):
        if not callback:
            callback = lambda dummy: None
        if not errback:
            def errback(failure):
                log.error(_(u"Can't connect profile [%s]") % failure)
                if failure.module.startswith('twisted.words.protocols.jabber') and failure.condition == "not-authorized":
                    self.launchAction(C.CHANGE_XMPP_PASSWD_ID, {}, profile=profile)
                else:
                    self.showDialog(failure.message, failure.fullname, 'error')
        self.bridge.asyncConnect(profile, callback=callback, errback=errback)

    def plug_profiles(self, profiles):
        """Tell application which profiles must be used

        @param profiles: list of valid profile names
        """
        self.plugging_profiles()
        for profile in profiles:
            self.profiles.plug(profile)

    def plugging_profiles(self):
        """Method to subclass to manage frontend specific things to do

        will be called when profiles are choosen and are to be plugged soon
        """
        pass

    def unplug_profile(self, profile):
        """Tell the application to not follow anymore the profile"""
        if not profile in self.profiles:
            raise ValueError("The profile [{}] is not plugged".format(profile))
        self.profiles.unplug(profile)

    def clear_profile(self):
        self.profiles.clear()

    def addContactList(self, profile):
        """Method to subclass to add a contact list widget

        will be called on each profile session build
        @return: a ContactList widget
        """
        return NotImplementedError

    def newWidget(self, widget):
        raise NotImplementedError

    def connectedHandler(self, profile, jid_s):
        """Called when the connection is made.

        @param jid_s (unicode): the JID that we were assigned by the server,
            as the resource might differ from the JID we asked for.
        """
        log.debug(_("Connected"))
        self.profiles[profile].whoami = jid.JID(jid_s)
        self.setPresenceStatus(profile=profile)
        self.contact_lists[profile].fill()

    def disconnectedHandler(self, profile):
        """called when the connection is closed"""
        log.debug(_("Disconnected"))
        self.contact_lists[profile].clearContacts()
        self.setPresenceStatus(C.PRESENCE_UNAVAILABLE, '', profile=profile)

    def actionNewHandler(self, action_data, id_, security_limit, profile):
        self.actionManager(action_data, profile=profile)

    def newContactHandler(self, jid_s, attributes, groups, profile):
        entity = jid.JID(jid_s)
        _groups = list(groups)
        self.contact_lists[profile].setContact(entity, _groups, attributes, in_roster=True)

    def newMessageHandler(self, from_jid_s, msg, type_, to_jid_s, extra, profile):
        from_jid = jid.JID(from_jid_s)
        to_jid = jid.JID(to_jid_s)
        if not self.trigger.point("newMessageTrigger", from_jid, msg, type_, to_jid, extra, profile=profile):
            return

        from_me = from_jid.bare == self.profiles[profile].whoami.bare
        target = to_jid if from_me else from_jid

        chat_type = C.CHAT_GROUP if type_ == C.MESS_TYPE_GROUPCHAT else C.CHAT_ONE2ONE
        contact_list = self.contact_lists[profile]

        chat_widget = self.widgets.getOrCreateWidget(quick_chat.QuickChat, target, type_=chat_type, on_new_widget=None, profile=profile)

        self.current_action_ids = set() # FIXME: to be removed
        self.current_action_ids_cb = {} # FIXME: to be removed

        if not from_jid in contact_list and from_jid.bare != self.profiles[profile].whoami.bare:
            #XXX: needed to show entities which haven't sent any
            #     presence information and which are not in roster
            contact_list.setContact(from_jid)

        # we display the message in the widget
        chat_widget.newMessage(from_jid, target, msg, type_, extra, profile)

        # ContactList alert
        if not from_me:
            visible = False
            for widget in self.visible_widgets:
                if isinstance(widget, quick_chat.QuickChat) and widget.manageMessage(from_jid, type_):
                    visible = True
                    break
            if visible:
                if self.isHidden():  # the window is hidden
                    self.updateAlertsCounter(extra_inc=1)
            else:
                contact_list.addAlert(from_jid.bare if type_ == C.MESS_TYPE_GROUPCHAT else from_jid)

    def sendMessage(self, to_jid, message, subject='', mess_type="auto", extra={}, callback=None, errback=None, profile_key=C.PROF_KEY_NONE):
        if callback is None:
            callback = lambda dummy=None: None # FIXME: optional argument is here because pyjamas doesn't support callback without arg with json proxy
        if errback is None:
            errback = lambda failure: self.showDialog(failure.fullname, failure.message, "error")

        if not self.trigger.point("sendMessageTrigger", to_jid, message, subject, mess_type, extra, callback, errback, profile_key=profile_key):
            return

        self.bridge.sendMessage(unicode(to_jid), message, subject, mess_type, extra, profile_key, callback=callback, errback=errback)

    def newAlertHandler(self, msg, title, alert_type, profile):
        assert alert_type in ['INFO', 'ERROR']
        self.showDialog(unicode(msg), unicode(title), alert_type.lower())

    def setPresenceStatus(self, show='', status=None, profile=C.PROF_KEY_NONE):
        raise NotImplementedError

    def presenceUpdateHandler(self, entity_s, show, priority, statuses, profile):

        log.debug(_(u"presence update for %(entity)s (show=%(show)s, priority=%(priority)s, statuses=%(statuses)s) [profile:%(profile)s]")
                  % {'entity': entity_s, C.PRESENCE_SHOW: show, C.PRESENCE_PRIORITY: priority, C.PRESENCE_STATUSES: statuses, 'profile': profile})
        entity = jid.JID(entity_s)

        if entity == self.profiles[profile].whoami:
            if show == C.PRESENCE_UNAVAILABLE:
                self.setPresenceStatus(C.PRESENCE_UNAVAILABLE, '', profile=profile)
            else:
                # FIXME: try to retrieve user language status before fallback to default
                status = statuses.get(C.PRESENCE_STATUSES_DEFAULT, None)
                self.setPresenceStatus(show, status, profile=profile)
            return

        self.callListeners('presence', entity, show, priority, statuses, profile=profile)

    def roomJoinedHandler(self, room_jid_s, room_nicks, user_nick, profile):
        """Called when a MUC room is joined"""
        log.debug(u"Room [%(room_jid)s] joined by %(profile)s, users presents:%(users)s" % {'room_jid': room_jid_s, 'profile': profile, 'users': room_nicks})
        room_jid = jid.JID(room_jid_s)
        chat_widget = self.widgets.getOrCreateWidget(quick_chat.QuickChat, room_jid, type_=C.CHAT_GROUP, profile=profile)
        chat_widget.setUserNick(unicode(user_nick))
        self.contact_lists[profile].setSpecial(room_jid, C.CONTACT_SPECIAL_GROUP)
        chat_widget.update()

    def roomLeftHandler(self, room_jid_s, profile):
        """Called when a MUC room is left"""
        log.debug(u"Room [%(room_jid)s] left by %(profile)s" % {'room_jid': room_jid_s, 'profile': profile})
        room_jid = jid.JID(room_jid_s)
        chat_widget = self.widgets.getWidget(quick_chat.QuickChat, room_jid, profile)
        if chat_widget:
            self.widgets.deleteWidget(chat_widget)
        self.contact_lists[profile].removeContact(room_jid)

    def roomUserJoinedHandler(self, room_jid_s, user_nick, user_data, profile):
        """Called when an user joined a MUC room"""
        room_jid = jid.JID(room_jid_s)
        chat_widget = self.widgets.getOrCreateWidget(quick_chat.QuickChat, room_jid, type_=C.CHAT_GROUP, profile=profile)
        chat_widget.addUser(user_nick)
        log.debug(u"user [%(user_nick)s] joined room [%(room_jid)s]" % {'user_nick': user_nick, 'room_jid': room_jid})

    def roomUserLeftHandler(self, room_jid_s, user_nick, user_data, profile):
        """Called when an user joined a MUC room"""
        room_jid = jid.JID(room_jid_s)
        chat_widget = self.widgets.getOrCreateWidget(quick_chat.QuickChat, room_jid, type_=C.CHAT_GROUP, profile=profile)
        chat_widget.removeUser(user_nick)
        log.debug(u"user [%(user_nick)s] left room [%(room_jid)s]" % {'user_nick': user_nick, 'room_jid': room_jid})

    def roomUserChangedNickHandler(self, room_jid_s, old_nick, new_nick, profile):
        """Called when an user joined a MUC room"""
        room_jid = jid.JID(room_jid_s)
        chat_widget = self.widgets.getOrCreateWidget(quick_chat.QuickChat, room_jid, type_=C.CHAT_GROUP, profile=profile)
        chat_widget.changeUserNick(old_nick, new_nick)
        log.debug(u"user [%(old_nick)s] is now known as [%(new_nick)s] in room [%(room_jid)s]" % {'old_nick': old_nick, 'new_nick': new_nick, 'room_jid': room_jid})

    def roomNewSubjectHandler(self, room_jid_s, subject, profile):
        """Called when subject of MUC room change"""
        room_jid = jid.JID(room_jid_s)
        chat_widget = self.widgets.getOrCreateWidget(quick_chat.QuickChat, room_jid, type_=C.CHAT_GROUP, profile=profile)
        chat_widget.setSubject(subject)
        log.debug(u"new subject for room [%(room_jid)s]: %(subject)s" % {'room_jid': room_jid, "subject": subject})

    def chatStateReceivedHandler(self, from_jid_s, state, profile):
        """Called when a new chat state (XEP-0085) is received.

        @param from_jid_s (unicode): JID of a contact or C.ENTITY_ALL
        @param state (unicode): new state
        @param profile (unicode): current profile
        """
        log.debug(_(u"Received new chat state {} from {} [{}]").format(state, from_jid_s, profile))
        from_jid = jid.JID(from_jid_s) if from_jid_s != C.ENTITY_ALL else C.ENTITY_ALL
        contact_list = self.contact_lists[profile]
        for widget in self.widgets.getWidgets(quick_chat.QuickChat):
            if profile != widget.profile:
                continue
            to_display = C.USER_CHAT_STATES[state] if (state and widget.type == C.CHAT_GROUP) else state
            if widget.type == C.CHAT_GROUP and from_jid_s == C.ENTITY_ALL:
                for occupant in [jid.newResource(widget.target, nick) for nick in widget.occupants]:
                    contact_list.setCache(occupant, 'chat_state', to_display)
                    widget.update(occupant)
            elif from_jid.bare == widget.target.bare:  # roster contact or MUC occupant
                contact_list.setCache(from_jid, 'chat_state', to_display)
                widget.update(from_jid)

    def psEventHandler(self, category, service_s, node, event_type, data, profile):
        """Called when a PubSub event is received.

        @param category(unicode): event category (e.g. "PEP", "MICROBLOG")
        @param service_s (unicode): pubsub service
        @param node (unicode): pubsub node
        @param event_type (unicode): event type (one of C.PUBLISH, C.RETRACT, C.DELETE)
        @param data (dict): event data
        """
        service_s = jid.JID(service_s)

        if category == C.PS_MICROBLOG and self.MB_HANDLE:
            if event_type == C.PS_PUBLISH:
                if not 'content' in data:
                    log.warning("No content found in microblog data")
                    return
                if 'groups' in data:
                    _groups = set(data['groups'].split() if data['groups'] else [])
                else:
                    _groups = None

                for wid in self.widgets.getWidgets(quick_blog.QuickBlog):
                    wid.addEntryIfAccepted(service_s, node, data, _groups, profile)

                try:
                    comments_node, comments_service = data['comments_node'], data['comments_service']
                except KeyError:
                    pass
                else:
                    self.bridge.mbGet(comments_service, comments_node, C.NO_LIMIT, [], {"subscribe":C.BOOL_TRUE}, profile=profile)
            elif event_type == C.PS_RETRACT:
                for wid in self.widgets.getWidgets(quick_blog.QuickBlog):
                    wid.deleteEntryIfPresent(service_s, node, data['id'], profile)
                pass
            else:
                log.warning("Unmanaged PubSub event type {}".format(event_type))

    def progressStartedHandler(self, pid, metadata, profile):
        log.info(u"Progress {} started".format(pid))

    def progressFinishedHandler(self, pid, metadata, profile):
        log.info(u"Progress {} finished".format(pid))

    def progressErrorHandler(self, pid, err_msg, profile):
        log.warning(u"Progress {pid} error: {err_msg}".format(pid=pid, err_msg=err_msg))

    def _subscribe_cb(self, answer, data):
        entity, profile = data
        type_ = "subscribed" if answer else "unsubscribed"
        self.bridge.subscription(type_, unicode(entity.bare), profile_key=profile)

    def subscribeHandler(self, type, raw_jid, profile):
        """Called when a subsciption management signal is received"""
        entity = jid.JID(raw_jid)
        if type == "subscribed":
            # this is a subscription confirmation, we just have to inform user
            # TODO: call self.getEntityMBlog to add the new contact blogs
            self.showDialog(_("The contact %s has accepted your subscription") % entity.bare, _('Subscription confirmation'))
        elif type == "unsubscribed":
            # this is a subscription refusal, we just have to inform user
            self.showDialog(_("The contact %s has refused your subscription") % entity.bare, _('Subscription refusal'), 'error')
        elif type == "subscribe":
            # this is a subscriptionn request, we have to ask for user confirmation
            # TODO: use sat.stdui.ui_contact_list to display the groups selector
            self.showDialog(_("The contact %s wants to subscribe to your presence.\nDo you accept ?") % entity.bare, _('Subscription confirmation'), 'yes/no', answer_cb=self._subscribe_cb, answer_data=(entity, profile))

    def showDialog(self, message, title, type="info", answer_cb=None, answer_data=None):
        raise NotImplementedError

    def showAlert(self, message):
        pass  #FIXME

    def dialogFailure(self, failure):
        log.warning(u"Failure: {}".format(failure))

    def progressIdHandler(self, progress_id, profile):
        """Callback used when an action result in a progress id"""
        log.info(u"Progress ID received: {}".format(progress_id))

    def isHidden(self):
        """Tells if the frontend window is hidden.

        @return bool
        """
        raise NotImplementedError

    def updateAlertsCounter(self, extra_inc=0):
        """Update the over whole alerts counter.

        @param extra_inc (int): extra counter
        """
        pass

    def paramUpdateHandler(self, name, value, namespace, profile):
        log.debug(_(u"param update: [%(namespace)s] %(name)s = %(value)s") % {'namespace': namespace, 'name': name, 'value': value})
        if (namespace, name) == ("Connection", "JabberID"):
            log.debug(_(u"Changing JID to %s") % value)
            self.profiles[profile].whoami = jid.JID(value)
        elif (namespace, name) == ('General', C.SHOW_OFFLINE_CONTACTS):
            self.contact_lists[profile].showOfflineContacts(C.bool(value))
        elif (namespace, name) == ('General', C.SHOW_EMPTY_GROUPS):
            self.contact_lists[profile].showEmptyGroups(C.bool(value))

    def contactDeletedHandler(self, jid_s, profile):
        target = jid.JID(jid_s)
        self.contact_lists[profile].removeContact(target, in_roster=True)

    def entityDataUpdatedHandler(self, entity_s, key, value, profile):
        entity = jid.JID(entity_s)
        if key == "nick":  # this is the roster nick, not the MUC nick
            if entity in self.contact_lists[profile]:
                self.contact_lists[profile].setCache(entity, 'nick', value)
                self.callListeners('nick', entity, value, profile=profile)
        elif key == "avatar":
            if entity in self.contact_lists[profile]:
                def gotFilename(filename):
                    self.contact_lists[profile].setCache(entity, 'avatar', filename)
                    self.callListeners('avatar', entity, filename, profile=profile)
                self.bridge.getAvatarFile(value, callback=gotFilename)

    def askConfirmationHandler(self, confirm_id, confirm_type, data, profile):
        raise NotImplementedError

    def actionResultHandler(self, type, id, data, profile):
        raise NotImplementedError

    def actionManager(self, action_data, callback=None, ui_show_cb=None, profile=C.PROF_KEY_NONE):
        """Handle backend action

        @param action_data(dict): action dict as sent by launchAction or returned by an UI action
        @param callback(None, callback): if not None, callback to use on XMLUI answer
        @param ui_show_cb(None, callback): if not None, method to call to show the XMLUI
        """
        try:
            xmlui = action_data.pop('xmlui')
        except KeyError:
            pass
        else:
            ui = self.xmlui.create(self, xml_data=xmlui, callback=callback, profile=profile)
            if ui_show_cb is None:
                ui.show()
            else:
                ui_show_cb(ui)

        try:
            progress_id = action_data.pop('progress')
        except KeyError:
            pass
        else:
            self.progressIdHandler(progress_id, profile)

        # we ignore metadata
        action_data = {k:v for k,v in action_data.iteritems() if not k.startswith("meta_")}

        if action_data:
            raise exceptions.DataError(u"Not all keys in action_data are managed ({keys})".format(keys=', '.join(action_data.keys())))

    def launchAction(self, callback_id, data=None, callback=None, profile=C.PROF_KEY_NONE):
        """ Launch a dynamic action

        @param callback_id: id of the action to launch
        @param data: data needed only for certain actions
        @param callback(callable, None): will be called with the resut
            if None, self.actionManager will be called
            else the callable will be called with the following kw parameters:
                - data: action_data
                - cb_id: callback id
                - profile: %(doc_profile)s
        @param profile: %(doc_profile)s

        """
        if data is None:
            data = dict()


        def action_cb(data):
            if callback is None:
                self.actionManager(data, profile=profile)
            else:
                callback(data=data, cb_id=callback_id, profile=profile)

        self.bridge.launchAction(callback_id, data, profile, callback=action_cb, errback=self.dialogFailure)

    def disconnect(self, profile):
        log.info("disconnecting")
        self.callListeners('disconnect', profile=profile)
        self.bridge.disconnect(profile)

    def onExit(self):
        """Must be called when the frontend is terminating"""
        to_unplug = []
        for profile in self.profiles:
            if self.bridge.isConnected(profile):
                if C.bool(self.bridge.getParamA("autodisconnect", "Connection", profile_key=profile)):
                    #The user wants autodisconnection
                    self.disconnect(profile)
            to_unplug.append(profile)
        for profile in to_unplug:
            self.unplug_profile(profile)
