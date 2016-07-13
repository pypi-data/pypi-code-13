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

from sat.core.i18n import _
from sat.core.log import getLogger
log = getLogger(__name__)
from sat_frontends.quick_frontend.quick_widgets import QuickWidget
from sat_frontends.quick_frontend.constants import Const as C
from sat_frontends.tools import jid


try:
    # FIXME: to be removed when an acceptable solution is here
    unicode('')  # XXX: unicode doesn't exist in pyjamas
except (TypeError, AttributeError):  # Error raised is not the same depending on pyjsbuild options
    # XXX: pyjamas' max doesn't support key argument, so we implement it ourself
    pyjamas_max = max

    def max(iterable, key):
        iter_cpy = list(iterable)
        iter_cpy.sort(key=key)
        return pyjamas_max(iter_cpy)


class QuickContactList(QuickWidget):
    """This class manage the visual representation of contacts"""

    def __init__(self, host, profile):
        log.debug(_("Contact List init"))
        super(QuickContactList, self).__init__(host, profile, profile)
        # bare jids as keys, resources are used in data
        self._cache = {}

        # special entities (groupchat, gateways, etc), bare jids
        self._specials = set()
        # extras are specials with full jids (e.g.: private MUC conversation)
        self._special_extras = set()

        # group data contain jids in groups and misc frontend data
        self._groups = {}  # groups to group data map

        # contacts in roster (bare jids)
        self._roster = set()

        # entities with alert(s) and their counts (usually a waiting message), dict{full jid: int)
        self._alerts = dict()

        # selected entities, full jid
        self._selected = set()

        # we keep our own jid
        self.whoami = host.profiles[profile].whoami

        # options
        self.show_disconnected = False
        self.show_empty_groups = True
        self.show_resources = False
        self.show_status = False
        # TODO: this may lead to two successive UI refresh and needs an optimization
        self.host.bridge.asyncGetParamA(C.SHOW_EMPTY_GROUPS, "General", profile_key=profile, callback=self._showEmptyGroups)
        self.host.bridge.asyncGetParamA(C.SHOW_OFFLINE_CONTACTS, "General", profile_key=profile, callback=self._showOfflineContacts)

        # FIXME: workaround for a pyjamas issue: calling hash on a class method always return a different value if that method is defined directly within the class (with the "def" keyword)
        self.presenceListener = self.onPresenceUpdate
        self.host.addListener('presence', self.presenceListener, [profile])
        self.nickListener = self.onNickUpdate
        self.host.addListener('nick', self.nickListener, [profile])

    def __contains__(self, entity):
        """Check if entity is in contact list

        @param entity (jid.JID): jid of the entity (resource is not ignored, use bare jid if needed)
        """
        if entity.resource:
            try:
                return entity.resource in self.getCache(entity.bare, C.CONTACT_RESOURCES)
            except KeyError:
                return False
        return entity in self._cache

    @property
    def roster_entities(self):
        """Return all the bare JIDs of the roster entities.

        @return: set(jid.JID)
        """
        return self._roster

    @property
    def roster_entities_connected(self):
        """Return all the bare JIDs of the roster entities that are connected.

        @return: set(jid.JID)
        """
        return set([entity for entity in self._roster if self.getCache(entity, C.PRESENCE_SHOW) is not None])

    @property
    def roster_entities_by_group(self):
        """Return a dictionary binding the roster groups to their entities bare
        JIDs. This also includes the empty group (None key).

        @return: dict{unicode: set(jid.JID)}
        """
        return {group: self._groups[group]['jids'] for group in self._groups}

    @property
    def roster_groups_by_entity(self):
        """Return a dictionary binding the entities bare JIDs to their roster
        groups. The empty group is filtered out.

        @return: dict{jid.JID: set(unicode)}
        """
        result = {}
        for group, data in self._groups.iteritems():
            if group is None:
                continue
            for entity in data['jids']:
                result.setdefault(entity, set()).add(group)
        return result

    def _gotContacts(self, contacts):
        for contact in contacts:
            self.host.newContactHandler(*contact, profile=self.profile)

    def fill(self):
        """Get all contacts from backend, and fill the widget

        Contacts will be cleared before refilling them
        """
        self.clearContacts(keep_cache=True)

        self.host.bridge.getContacts(self.profile, callback=self._gotContacts)

    def update(self):
        """Update the display when something changed"""
        raise NotImplementedError

    def getCache(self, entity, name=None):
        """Return a cache value for a contact

        @param entity(entity.entity): entity of the contact from who we want data (resource is used if given)
            if a resource specific information is requested:
                - if no resource is given (bare jid), the main resource is used, according to priority
                - if resource is given, it is used
        @param name(unicode): name the data to get, or None to get everything
        @return: full cache if no name is given, or value of "name", or None
        """
        try:
            cache = self._cache[entity.bare]
        except KeyError:
            self.setContact(entity)
            cache = self._cache[entity.bare]

        if name is None:
            return cache
        try:
            if name in ('status', C.PRESENCE_STATUSES, C.PRESENCE_PRIORITY, C.PRESENCE_SHOW):
                # these data are related to the resource
                if not entity.resource:
                    main_resource = cache[C.CONTACT_MAIN_RESOURCE]
                    cache = cache[C.CONTACT_RESOURCES][main_resource]
                else:
                    cache = cache[C.CONTACT_RESOURCES][entity.resource]

                if name == 'status':  # XXX: we get the first status for 'status' key
                    # TODO: manage main language for statuses
                    return cache[C.PRESENCE_STATUSES].get(C.PRESENCE_STATUSES_DEFAULT, '')

            return cache[name]
        except KeyError:
            return None

    def setCache(self, entity, name, value):
        """Set or update value for one data in cache

        @param entity(JID): entity to update
        @param name(unicode): value to set or update
        """
        self.setContact(entity, None, {name: value})

    def getFullJid(self, entity):
        """Get full jid from a bare jid

        @param entity(jid.JID): must be a bare jid
        @return (jid.JID): bare jid + main resource
        @raise ValueError: the entity is not bare
        """
        if entity.resource:
            raise ValueError("getFullJid must be used with a bare jid")
        main_resource = self.getCache(entity, C.CONTACT_MAIN_RESOURCE)
        return jid.JID(u"{}/{}".format(entity, main_resource))

    def setGroupData(self, group, name, value):
        """Register a data for a group

        @param group: a valid (existing) group name
        @param name: name of the data (can't be "jids")
        @param value: value to set
        """
        # FIXME: this is never used, should it be removed?
        assert name is not 'jids'
        self._groups[group][name] = value

    def getGroupData(self, group, name=None):
        """Return value associated to group data

        @param group: a valid (existing) group name
        @param name: name of the data or None to get the whole dict
        @return: registered value
        """
        if name is None:
            return self._groups[group]
        return self._groups[group][name]

    def setSpecial(self, entity, special_type):
        """Set special flag on an entity

        @param entity(jid.JID): jid of the special entity
        @param special_type: one of special type (e.g. C.CONTACT_SPECIAL_GROUP) or None to remove special flag
        """
        assert special_type in C.CONTACT_SPECIAL_ALLOWED + (None,)
        self.setCache(entity, C.CONTACT_SPECIAL, special_type)

    def getSpecials(self, special_type=None):
        """Return all the bare JIDs of the special roster entities of the type
        specified by special_type. If special_type is None, return all specials.

        @param special_type: one of special type (e.g. C.CONTACT_SPECIAL_GROUP) or None to return all specials.
        @return: set(jid.JID)
        """
        if special_type is None:
            return self._specials
        return set([entity for entity in self._specials if self.getCache(entity, C.CONTACT_SPECIAL) == special_type])

    def getSpecialExtras(self, special_type=None):
        """Return all the JIDs of the special extras entities that are related
        to a special entity of the type specified by special_type.
        If special_type is None, return all special extras.

        @param special_type: one of special type (e.g. C.CONTACT_SPECIAL_GROUP) or None to return all special extras.
        @return: set(jid.JID)
        """
        if special_type is None:
            return self._special_extras
        return set([extra for extra in self._special_extras if extra.bare in self.getSpecials(special_type)])

    def clearContacts(self, keep_cache=False):
        """Clear all the contact list

        @param keep_cache: if True, don't reset the cache
        """
        self.unselectAll()
        if not keep_cache:
            self._cache.clear()
        self._groups.clear()
        self._specials.clear()
        self._special_extras.clear()
        self._roster.clear()
        self._alerts.clear()
        self.host.updateAlertsCounter()
        self.update()

    def setContact(self, entity, groups=None, attributes=None, in_roster=False):
        """Add a contact to the list if doesn't exist, else update it.

        This method can be called with groups=None for the purpose of updating
        the contact's attributes (e.g. nickname). In that case, the groups
        attribute must not be set to the default group but ignored. If not,
        you may move your contact from its actual group(s) to the default one.

        None value for 'groups' has a different meaning than [None] which is for the default group.

        @param entity (jid.JID): entity to add or replace
        @param groups (list): list of groups or None to ignore the groups membership.
        @param attributes (dict): attibutes of the added jid or to update
        @param in_roster (bool): True if contact is from roster
        """
        if attributes is None:
            attributes = {}

        entity_bare = entity.bare

        if in_roster:
            self._roster.add(entity_bare)

        cache = self._cache.setdefault(entity_bare, {C.CONTACT_RESOURCES: {}})

        assert not C.CONTACT_DATA_FORBIDDEN.intersection(attributes) # we don't want forbidden data in attributes

        # we set groups and fill self._groups accordingly
        if groups is not None:
            if not groups:
                groups = [None]  # [None] is the default group
            if C.CONTACT_GROUPS in cache:
                # XXX: don't use set(cache[C.CONTACT_GROUPS]).difference(groups) because it won't work in Pyjamas if None is in cache[C.CONTACT_GROUPS]
                for group in [group for group in cache[C.CONTACT_GROUPS] if group not in groups]:
                    self._groups[group]['jids'].remove(entity_bare)
            cache[C.CONTACT_GROUPS] = groups
            for group in groups:
                self._groups.setdefault(group, {}).setdefault('jids', set()).add(entity_bare)

        # special entities management
        if C.CONTACT_SPECIAL in attributes:
            if attributes[C.CONTACT_SPECIAL] is None:
                del attributes[C.CONTACT_SPECIAL]
                self._specials.remove(entity_bare)
            else:
                self._specials.add(entity_bare)
                cache[C.CONTACT_MAIN_RESOURCE] = None

        # now the attribute we keep in cache
        for attribute, value in attributes.iteritems():
            cache[attribute] = value

        # we can update the display
        self.update()

    def getContacts(self):
        """Return contacts currently selected

        @return (set): set of selected entities"""
        return self._selected

    def entityToShow(self, entity, check_resource=False):
        """Tell if the contact should be showed or hidden.

        @param entity (jid.JID): jid of the contact
        @param check_resource (bool): True if resource must be significant
        @return (bool): True if that contact should be showed in the list
        """
        show = self.getCache(entity, C.PRESENCE_SHOW)

        if check_resource:
            alerts = self._alerts.keys()
            selected = self._selected
        else:
            alerts = {alert.bare for alert in self._alerts}
            selected = {selected.bare for selected in self._selected}
        return ((show is not None and show != C.PRESENCE_UNAVAILABLE)
                or self.show_disconnected
                or entity in alerts
                or entity in selected)

    def anyEntityToShow(self, entities, check_resources=False):
        """Tell if in a list of entities, at least one should be shown

        @param entities (list[jid.JID]): list of jids
        @param check_resources (bool): True if resources must be significant
        @return: bool
        """
        for entity in entities:
            if self.entityToShow(entity, check_resources):
                return True
        return False

    def isEntityInGroup(self, entity, group):
        """Tell if an entity is in a roster group

        @param entity(jid.JID): jid of the entity
        @param group(unicode): group to check
        @return (bool): True if the entity is in the group
        """
        return entity in self.getGroupData(group, "jids")

    def removeContact(self, entity, in_roster=False):
        """remove a contact from the list

        @param entity(jid.JID): jid of the entity to remove (bare jid is used)
        @param in_roster (bool): True if contact is from roster
        """
        entity_bare = entity.bare
        try:
            groups = self._cache[entity_bare].get(C.CONTACT_GROUPS, set())
        except KeyError:
            log.warning(_(u"Trying to delete an unknow entity [{}]").format(entity))
        if in_roster:
            self._roster.remove(entity_bare)
        del self._cache[entity_bare]
        for group in groups:
            self._groups[group]['jids'].remove(entity_bare)
            if not self._groups[group]['jids']:
                self._groups.pop(group)
        for iterable in (self._selected, self._alerts, self._specials, self._special_extras):
            to_remove = set()
            for set_entity in iterable:
                if set_entity.bare == entity.bare:
                    to_remove.add(set_entity)
            if isinstance(iterable, set):
                iterable.difference_update(to_remove)
            else:  # XXX: self._alerts is a dict
                for item in to_remove:
                    del iterable[item]
        self.update()

    def onPresenceUpdate(self, entity, show, priority, statuses, profile):
        """Update entity's presence status

        @param entity(jid.JID): entity updated
        @param show: availability
        @parap priority: resource's priority
        @param statuses: dict of statuses
        @param profile: %(doc_profile)s
        """
        cache = self.getCache(entity)
        if show == C.PRESENCE_UNAVAILABLE:
            if not entity.resource:
                cache[C.CONTACT_RESOURCES].clear()
                cache[C.CONTACT_MAIN_RESOURCE] = None
            else:
                try:
                    del cache[C.CONTACT_RESOURCES][entity.resource]
                except KeyError:
                    log.error(u"Presence unavailable received for an unknown resource [{}]".format(entity))
                if not cache[C.CONTACT_RESOURCES]:
                    cache[C.CONTACT_MAIN_RESOURCE] = None
        else:
            assert entity.resource
            resources_data = cache[C.CONTACT_RESOURCES]
            resource_data = resources_data.setdefault(entity.resource, {})
            resource_data[C.PRESENCE_SHOW] = show
            resource_data[C.PRESENCE_PRIORITY] = int(priority)
            resource_data[C.PRESENCE_STATUSES] = statuses

            if entity.bare not in self._specials:
                priority_resource = max(resources_data, key=lambda res: resources_data[res][C.PRESENCE_PRIORITY])
                cache[C.CONTACT_MAIN_RESOURCE] = priority_resource
        self.update()

    def onNickUpdate(self, entity, new_nick, profile):
        """Update entity's nick

        @param entity(jid.JID): entity updated
        @param new_nick(unicode): new nick of the entity
        @param profile: %(doc_profile)s
        """
        raise NotImplementedError  # Must be implemented by frontends

    def unselectAll(self):
        """Unselect all contacts"""
        self._selected.clear()
        self.update()

    def select(self, entity):
        """Select an entity

        @param entity(jid.JID): entity to select (resource is significant)
        """
        log.debug(u"select %s" % entity)
        self._selected.add(entity)
        self.update()

    def getAlerts(self, entity, use_bare_jid=False):
        """Return the number of alerts set to this entity.
        
        @param entity (jid.JID): entity
        @param use_bare_jid (bool): if True, cumulate the alerts of all the resources sharing the same bare JID
        @return int
        """
        if not use_bare_jid:
            return self._alerts.get(entity, 0)
        
        alerts = {}
        for contact in self._alerts:
            alerts.setdefault(contact.bare, 0)
            alerts[contact.bare] += self._alerts[contact]
        return alerts.get(entity.bare, 0)

    def addAlert(self, entity):
        """Increase the alerts counter for this entity (usually for a waiting message)

        @param entity(jid.JID): entity which must displayed in alert mode (resource is significant)
        """
        self._alerts.setdefault(entity, 0)
        self._alerts[entity] += 1
        self.update()
        self.host.updateAlertsCounter()

    def removeAlerts(self, entity, use_bare_jid=True):
        """Eventually remove an alert on the entity (usually for a waiting message).

        @param entity(jid.JID): entity (resource is significant)
        @param use_bare_jid (bool): if True, ignore the resource
        """
        if use_bare_jid:
            to_remove = set()
            for alert_entity in self._alerts:
                if alert_entity.bare == entity.bare:
                    to_remove.add(alert_entity)
            if not to_remove:
                return  # nothing changed
            for entity in to_remove:
                del self._alerts[entity]
        else:
            try:
                del self._alerts[entity]
            except KeyError:
                return  # nothing changed
        self.update()
        self.host.updateAlertsCounter()

    def _showOfflineContacts(self, show_str):
        self.showOfflineContacts(C.bool(show_str))

    def showOfflineContacts(self, show):
        """Tell if offline contacts should shown

        @param show(bool): True if offline contacts should be shown
        """
        assert isinstance(show, bool)
        if self.show_disconnected == show:
            return
        self.show_disconnected = show
        self.update()

    def _showEmptyGroups(self, show_str):
        self.showEmptyGroups(C.bool(show_str))

    def showEmptyGroups(self, show):
        assert isinstance(show, bool)
        if self.show_empty_groups == show:
            return
        self.show_empty_groups = show
        self.update()

    def showResources(self, show):
        assert isinstance(show, bool)
        if self.show_resources == show:
            return
        self.show_resources = show
        self.update()

    def onDelete(self):
        QuickWidget.onDelete(self)
        self.host.removeListener('presence', self.presenceListener)
