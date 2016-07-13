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

from sat.core.i18n import _

from sat.core.log import getLogger
log = getLogger(__name__)

import os.path
import copy
from collections import namedtuple
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
from uuid import uuid4
from twisted.python import failure
from twisted.internet import defer, reactor, error
from twisted.words.protocols.jabber import jid
from sat.core import exceptions
from sat.core.constants import Const as C
from sat.memory.sqlite import SqliteStorage
from sat.memory.persistent import PersistentDict
from sat.memory.params import Params
from sat.memory.disco import Discovery
from sat.memory.crypto import BlockCipher
from sat.memory.crypto import PasswordHasher
from sat.tools import config as tools_config


PresenceTuple = namedtuple("PresenceTuple", ('show', 'priority', 'statuses'))
MSG_NO_SESSION = "Session id doesn't exist or is finished"

class Sessions(object):
    """Sessions are data associated to key used for a temporary moment, with optional profile checking."""
    DEFAULT_TIMEOUT = 600

    def __init__(self, timeout=None, resettable_timeout=True):
        """
        @param timeout (int): nb of seconds before session destruction
        @param resettable_timeout (bool): if True, the timeout is reset on each access
        """
        self._sessions = dict()
        self.timeout = timeout or Sessions.DEFAULT_TIMEOUT
        self.resettable_timeout = resettable_timeout

    def newSession(self, session_data=None, session_id=None, profile=None):
        """Create a new session

        @param session_data: mutable data to use, default to a dict
        @param session_id (str): force the session_id to the given string
        @param profile: if set, the session is owned by the profile,
                        and profileGet must be used instead of __getitem__
        @return: session_id, session_data
        """
        if session_id is None:
            session_id = str(uuid4())
        elif session_id in self._sessions:
            raise exceptions.ConflictError(u"Session id {} is already used".format(session_id))
        timer = reactor.callLater(self.timeout, self._purgeSession, session_id)
        if session_data is None:
            session_data = {}
        self._sessions[session_id] = (timer, session_data) if profile is None else (timer, session_data, profile)
        return session_id, session_data

    def _purgeSession(self, session_id):
        try:
            timer, session_data, profile = self._sessions[session_id]
        except ValueError:
            timer, session_data = self._sessions[session_id]
            profile = None
        try:
            timer.cancel()
        except error.AlreadyCalled:
            # if the session is time-outed, the timer has been called
            pass
        del self._sessions[session_id]
        log.debug(u"Session {} purged{}".format(session_id, u' (profile {})'.format(profile) if profile is not None else u''))

    def __len__(self):
        return len(self._sessions)

    def __contains__(self, session_id):
        return session_id in self._sessions

    def profileGet(self, session_id, profile):
        try:
            timer, session_data, profile_set = self._sessions[session_id]
        except ValueError:
            raise exceptions.InternalError("You need to use __getitem__ when profile is not set")
        except KeyError:
            raise failure.Failure(KeyError(MSG_NO_SESSION))
        if profile_set != profile:
            raise exceptions.InternalError("current profile differ from set profile !")
        if self.resettable_timeout:
            timer.reset(self.timeout)
        return session_data

    def __getitem__(self, session_id):
        try:
            timer, session_data = self._sessions[session_id]
        except ValueError:
            raise exceptions.InternalError("You need to use profileGet instead of __getitem__ when profile is set")
        except KeyError:
            raise failure.Failure(KeyError(MSG_NO_SESSION))
        if self.resettable_timeout:
            timer.reset(self.timeout)
        return session_data

    def __setitem__(self, key, value):
        raise NotImplementedError("You need do use newSession to create a session")

    def __delitem__(self, session_id):
        """ delete the session data """
        self._purgeSession(session_id)

    def keys(self):
        return self._sessions.keys()

    def iterkeys(self):
        return self._sessions.iterkeys()


class ProfileSessions(Sessions):
    """ProfileSessions extends the Sessions class, but here the profile can be
    used as the key to retrieve data or delete a session (instead of session id).
    """

    def _profileGetAllIds(self, profile):
        """Return a list of the sessions ids that are associated to the given profile.

        @param profile: %(doc_profile)s
        @return: a list containing the sessions ids
        """
        ret = []
        for session_id in self._sessions.iterkeys():
            try:
                timer, session_data, profile_set = self._sessions[session_id]
            except ValueError:
                continue
            if profile == profile_set:
                ret.append(session_id)
        return ret

    def profileGetUnique(self, profile):
        """Return the data of the unique session that is associated to the given profile.

        @param profile: %(doc_profile)s
        @return:
            - mutable data (default: dict) of the unique session
            - None if no session is associated to the profile
            - raise an error if more than one session are found
        """
        ids = self._profileGetAllIds(profile)
        if len(ids) > 1:
            raise exceptions.InternalError('profileGetUnique has been used but more than one session has been found!')
        return self.profileGet(ids[0], profile) if len(ids) == 1 else None  # XXX: timeout might be reset

    def profileDelUnique(self, profile):
        """Delete the unique session that is associated to the given profile.

        @param profile: %(doc_profile)s
        @return: None, but raise an error if more than one session are found
        """
        ids = self._profileGetAllIds(profile)
        if len(ids) > 1:
            raise exceptions.InternalError('profileDelUnique has been used but more than one session has been found!')
        if len(ids) == 1:
            del self._sessions[ids[0]]


class PasswordSessions(ProfileSessions):

    # FIXME: temporary hack for the user personal key not to be lost. The session
    # must actually be purged and later, when the personal key is needed, the
    # profile password should be asked again in order to decrypt it.
    def __init__(self, timeout=None):
        ProfileSessions.__init__(self, timeout, resettable_timeout=False)

    def _purgeSession(self, session_id):
        log.debug("FIXME: PasswordSessions should ask for the profile password after the session expired")


# XXX: tmp update code, will be removed in the future
# When you remove this, please add the default value for
# 'local_dir' in sat.core.constants.Const.DEFAULT_CONFIG
def fixLocalDir(silent=True):
    """Retro-compatibility with the previous local_dir default value.

    @param silent (boolean): toggle logging output (must be True when called from sat.sh)
    """
    user_config = SafeConfigParser()
    try:
        user_config.read(C.CONFIG_FILES)
    except:
        pass  # file is readable but its structure if wrong
    try:
        current_value = user_config.get('DEFAULT', 'local_dir')
    except (NoOptionError, NoSectionError):
        current_value = ''
    if current_value:
        return  # nothing to do
    old_default = '~/.sat'
    if os.path.isfile(os.path.expanduser(old_default) + '/' + C.SAVEFILE_DATABASE):
        if not silent:
            log.warning(_(u"A database has been found in the default local_dir for previous versions (< 0.5)"))
        tools_config.fixConfigOption('', 'local_dir', old_default, silent)


class Memory(object):
    """This class manage all the persistent information"""

    def __init__(self, host):
        log.info(_("Memory manager init"))
        self.initialized = defer.Deferred()
        self.host = host
        self._entities_cache = {} # XXX: keep presence/last resource/other data in cache
                                  #     /!\ an entity is not necessarily in roster
                                  #     main key is bare jid, value is a dict
                                  #     where main key is resource, or None for bare jid
        self._key_signals = set() # key which need a signal to frontends when updated
        self.subscriptions = {}
        self.auth_sessions = PasswordSessions()  # remember the authenticated profiles
        self.disco = Discovery(host)
        fixLocalDir(False)  # XXX: tmp update code, will be removed in the future
        self.config = tools_config.parseMainConf()
        database_file = os.path.expanduser(os.path.join(self.getConfig('', 'local_dir'), C.SAVEFILE_DATABASE))
        self.storage = SqliteStorage(database_file, host.version)
        PersistentDict.storage = self.storage
        self.params = Params(host, self.storage)
        log.info(_("Loading default params template"))
        self.params.load_default_params()
        d = self.storage.initialized.addCallback(lambda ignore: self.load())
        self.memory_data = PersistentDict("memory")
        d.addCallback(lambda ignore: self.memory_data.load())
        d.addCallback(lambda ignore: self.disco.load())
        d.chainDeferred(self.initialized)

    ## Configuration ##

    def getConfig(self, section, name, default=None):
        """Get the main configuration option

        @param section: section of the config file (None or '' for DEFAULT)
        @param name: name of the option
        @param default: value to use if not found
        @return: str, list or dict
        """
        return tools_config.getConfig(self.config, section, name, default)

    def load_xml(self, filename):
        """Load parameters template from xml file

        @param filename (str): input file
        @return: bool: True in case of success
        """
        if not filename:
            return False
        filename = os.path.expanduser(filename)
        if os.path.exists(filename):
            try:
                self.params.load_xml(filename)
                log.debug(_(u"Parameters loaded from file: %s") % filename)
                return True
            except Exception as e:
                log.error(_(u"Can't load parameters from file: %s") % e)
        return False

    def save_xml(self, filename):
        """Save parameters template to xml file

        @param filename (str): output file
        @return: bool: True in case of success
        """
        if not filename:
            return False
        #TODO: need to encrypt files (at least passwords !) and set permissions
        filename = os.path.expanduser(filename)
        try:
            self.params.save_xml(filename)
            log.debug(_(u"Parameters saved to file: %s") % filename)
            return True
        except Exception as e:
            log.error(_(u"Can't save parameters to file: %s") % e)
        return False

    def load(self):
        """Load parameters and all memory things from db"""
        #parameters data
        return self.params.loadGenParams()

    def loadIndividualParams(self, profile):
        """Load individual parameters for a profile
        @param profile: %(doc_profile)s"""
        return self.params.loadIndParams(profile)

    ## Profiles/Sessions management ##

    def startSession(self, password, profile):
        """"Iniatialise session for a profile

        @param password(unicode): profile session password
            or empty string is no password is set
        @param profile: %(doc_profile)s
        @raise exceptions.ProfileUnknownError if profile doesn't exists
        @raise exceptions.PasswordError: the password does not match
        """
        profile = self.getProfileName(profile)

        def createSession(dummy):
            """Called once params are loaded."""
            self._entities_cache[profile] = {}
            log.info(u"[{}] Profile session started".format(profile))
            return False

        def backendInitialised(dummy):
            def doStartSession(dummy=None):
                if self.isSessionStarted(profile):
                    log.info("Session already started!")
                    return True
                try:
                    # if there is a value at this point in self._entities_cache,
                    # it is the loadIndividualParams Deferred, the session is starting
                    session_d = self._entities_cache[profile]
                except KeyError:
                    # else we do request the params
                    session_d = self._entities_cache[profile] = self.loadIndividualParams(profile)
                    session_d.addCallback(createSession)
                finally:
                    return session_d

            auth_d = self.profileAuthenticate(password, profile)
            auth_d.addCallback(doStartSession)
            return auth_d

        if self.host.initialised.called:
            return defer.succeed(None).addCallback(backendInitialised)
        else:
            return self.host.initialised.addCallback(backendInitialised)

    def stopSession(self, profile):
        """Delete a profile session

        @param profile: %(doc_profile)s
        """
        if self.host.isConnected(profile):
            log.debug(u"Disconnecting profile because of session stop")
            self.host.disconnect(profile)
        self.auth_sessions.profileDelUnique(profile)
        try:
            self._entities_cache[profile]
        except KeyError:
            log.warning(u"Profile was not in cache")

    def _isSessionStarted(self, profile_key):
        return self.isSessionStarted(self.getProfileName(profile_key))

    def isSessionStarted(self, profile):
        try:
            # XXX: if the value in self._entities_cache is a Deferred,
            #      the session is starting but not started yet
            return not isinstance(self._entities_cache[profile], defer.Deferred)
        except KeyError:
            return False

    def profileAuthenticate(self, password, profile):
        """Authenticate the profile.

        @param password (unicode): the SàT profile password
        @param profile: %(doc_profile)s
        @return (D): a deferred None in case of success, a failure otherwise.
        @raise exceptions.PasswordError: the password does not match
        """
        session_data = self.auth_sessions.profileGetUnique(profile)
        if not password and session_data:
            # XXX: this allows any frontend to connect with the empty password as soon as
            # the profile has been authenticated at least once before. It is OK as long as
            # submitting a form with empty passwords is restricted to local frontends.
            return defer.succeed(None)

        def check_result(result):
            if not result:
                log.warning(u'Authentication failure of profile {}'.format(profile))
                raise failure.Failure(exceptions.PasswordError(u"The provided profile password doesn't match."))
            if not session_data:  # avoid to create two profile sessions when password if specified
                return self.newAuthSession(password, profile)

        d = self.asyncGetParamA(C.PROFILE_PASS_PATH[1], C.PROFILE_PASS_PATH[0], profile_key=profile)
        d.addCallback(lambda sat_cipher: PasswordHasher.verify(password, sat_cipher))
        return d.addCallback(check_result)

    def newAuthSession(self, key, profile):
        """Start a new session for the authenticated profile.

        The personal key is loaded encrypted from a PersistentDict before being decrypted.

        @param key: the key to decrypt the personal key
        @param profile: %(doc_profile)s
        @return: a deferred None value
        """
        def gotPersonalKey(personal_key):
            """Create the session for this profile and store the personal key"""
            self.auth_sessions.newSession({C.MEMORY_CRYPTO_KEY: personal_key}, profile=profile)
            log.debug(u'auth session created for profile %s' % profile)

        d = PersistentDict(C.MEMORY_CRYPTO_NAMESPACE, profile).load()
        d.addCallback(lambda data: BlockCipher.decrypt(key, data[C.MEMORY_CRYPTO_KEY]))
        return d.addCallback(gotPersonalKey)

    def purgeProfileSession(self, profile):
        """Delete cache of data of profile
        @param profile: %(doc_profile)s"""
        log.info(_("[%s] Profile session purge" % profile))
        self.params.purgeProfile(profile)
        try:
            del self._entities_cache[profile]
        except KeyError:
            log.error(_(u"Trying to purge roster status cache for a profile not in memory: [%s]") % profile)

    def getProfilesList(self):
        return self.storage.getProfilesList()

    def getProfileName(self, profile_key, return_profile_keys=False):
        """Return name of profile from keyword

        @param profile_key: can be the profile name or a keyword (like @DEFAULT@)
        @param return_profile_keys: if True, return unmanaged profile keys (like "@ALL@"). This keys must be managed by the caller
        @return: requested profile name
        @raise exceptions.ProfileUnknownError if profile doesn't exists
        """
        return self.params.getProfileName(profile_key, return_profile_keys)

    def profileSetDefault(self, profile):
        """Set default profile

        @param profile: %(doc_profile)s
        """
        # we want to be sure that the profile exists
        profile = self.getProfileName(profile)

        self.memory_data['Profile_default'] = profile

    def asyncCreateProfile(self, name, password):
        """Create a new profile
        @param name (unicode): profile name
        @param password (unicode): profile password
            Can be empty to disable password
        @return: Deferred
        """
        if not name:
            raise ValueError("Empty profile name")
        if name[0] == '@':
            raise ValueError("A profile name can't start with a '@'")

        if name in self._entities_cache:
            raise exceptions.ConflictError(u"A session for this profile exists")

        d = self.params.asyncCreateProfile(name)

        def initPersonalKey(dummy):
            # be sure to call this after checking that the profile doesn't exist yet
            personal_key = BlockCipher.getRandomKey(base64=True)  # generated once for all and saved in a PersistentDict
            self.auth_sessions.newSession({C.MEMORY_CRYPTO_KEY: personal_key}, profile=name)  # will be encrypted by setParam

        def startFakeSession(dummy):
            # avoid ProfileNotConnected exception in setParam
            self._entities_cache[name] = None
            self.params.loadIndParams(name)

        def stopFakeSession(dummy):
            del self._entities_cache[name]
            self.params.purgeProfile(name)

        d.addCallback(initPersonalKey)
        d.addCallback(startFakeSession)
        d.addCallback(lambda dummy: self.setParam(C.PROFILE_PASS_PATH[1], password, C.PROFILE_PASS_PATH[0], profile_key=name))
        d.addCallback(stopFakeSession)
        d.addCallback(lambda dummy: self.auth_sessions.profileDelUnique(name))
        return d

    def asyncDeleteProfile(self, name, force=False):
        """Delete an existing profile
        @param name: Name of the profile
        @param force: force the deletion even if the profile is connected.
        To be used for direct calls only (not through the bridge).
        @return: a Deferred instance
        """
        def cleanMemory(dummy):
            self.auth_sessions.profileDelUnique(name)
            try:
                del self._entities_cache[name]
            except KeyError:
                pass
        d = self.params.asyncDeleteProfile(name, force)
        d.addCallback(cleanMemory)
        return d

    ## History ##

    def addToHistory(self, from_jid, to_jid, message, type_='chat', extra=None, timestamp=None, profile=C.PROF_KEY_NONE):
        assert profile != C.PROF_KEY_NONE
        if extra is None:
            extra = {}
        return self.storage.addToHistory(from_jid, to_jid, message, type_, extra, timestamp, profile)

    def getHistory(self, from_jid, to_jid, limit=C.HISTORY_LIMIT_NONE, between=True, search=None, profile=C.PROF_KEY_NONE):
        """Retrieve messages in history
        @param from_jid (JID): source JID (full, or bare for catchall)
        @param to_jid (JID): dest JID (full, or bare for catchall)
        @param limit (int): maximum number of messages to get:
            - 0 for no message (returns the empty list)
            - C.HISTORY_LIMIT_NONE or None for unlimited
            - C.HISTORY_LIMIT_DEFAULT to use the HISTORY_LIMIT parameter value
        @param between (bool): confound source and dest (ignore the direction)
        @param search (str): pattern to filter the history results
        @param profile (str): %(doc_profile)s
        @return: list of tuple as in http://wiki.goffi.org/wiki/Bridge_API#getHistory
        """
        assert profile != C.PROF_KEY_NONE
        if limit == C.HISTORY_LIMIT_DEFAULT:
            limit = int(self.getParamA(C.HISTORY_LIMIT, 'General', profile_key=profile))
        elif limit == C.HISTORY_LIMIT_NONE:
            limit = None
        if limit == 0:
            return defer.succeed([])
        return self.storage.getHistory(jid.JID(from_jid), jid.JID(to_jid), limit, between, search, profile)

    ## Statuses ##

    def _getPresenceStatuses(self, profile_key):
        ret = self.getPresenceStatuses(profile_key)
        return {entity.full():data for entity, data in ret.iteritems()}

    def getPresenceStatuses(self, profile_key):
        """Get all the presence statuses of a profile

        @param profile_key: %(doc_profile_key)s
        @return: presence data: key=entity JID, value=presence data for this entity
        """
        profile_cache = self._getProfileCache(profile_key)
        entities_presence = {}

        for entity_jid, entity_data in profile_cache.iteritems():
            for resource, resource_data in entity_data.iteritems():
                full_jid = copy.copy(entity_jid)
                full_jid.resource = resource
                try:
                    presence_data = self.getEntityDatum(full_jid, "presence", profile_key)
                except KeyError:
                    continue
                entities_presence.setdefault(entity_jid, {})[resource or ''] = presence_data

        return entities_presence

    def setPresenceStatus(self, entity_jid, show, priority, statuses, profile_key):
        """Change the presence status of an entity

        @param entity_jid: jid.JID of the entity
        @param show: show status
        @param priority: priority
        @param statuses: dictionary of statuses
        @param profile_key: %(doc_profile_key)s
        """
        presence_data = PresenceTuple(show, priority, statuses)
        self.updateEntityData(entity_jid, "presence", presence_data, profile_key=profile_key)
        if entity_jid.resource and show != C.PRESENCE_UNAVAILABLE:
            # If a resource is available, bare jid should not have presence information
            try:
                self.delEntityDatum(entity_jid.userhostJID(), "presence", profile_key)
            except (KeyError, exceptions.UnknownEntityError):
                pass

    ## Resources ##

    def _getAllResource(self, jid_s, profile_key):
        jid_ = jid.JID(jid_s)
        return self.getAllResources(jid_, profile_key)

    def getAllResources(self, entity_jid, profile_key):
        """Return all resource from jid for which we have had data in this session

        @param entity_jid: bare jid of the entit
        @param profile_key: %(doc_profile_key)s
        return (list[unicode]): list of resources

        @raise exceptions.UnknownEntityError: if entity is not in cache
        @raise ValueError: entity_jid has a resource
        """
        if entity_jid.resource:
            raise ValueError("getAllResources must be used with a bare jid (got {})".format(entity_jid))
        profile_cache = self._getProfileCache(profile_key)
        try:
            entity_data = profile_cache[entity_jid.userhostJID()]
        except KeyError:
            raise exceptions.UnknownEntityError(u"Entity {} not in cache".format(entity_jid))
        resources= set(entity_data.keys())
        resources.discard(None)
        return resources

    def getAvailableResources(self, entity_jid, profile_key):
        """Return available resource for entity_jid

        This method differs from getAllResources by returning only available resources
        @param entity_jid: bare jid of the entit
        @param profile_key: %(doc_profile_key)s
        return (list[unicode]): list of available resources

        @raise exceptions.UnknownEntityError: if entity is not in cache
        """
        available = []
        for resource in self.getAllResources(entity_jid, profile_key):
            full_jid = copy.copy(entity_jid)
            full_jid.resource = resource
            try:
                presence_data = self.getEntityDatum(full_jid, "presence", profile_key)
            except KeyError:
                log.debug(u"Can't get presence data for {}".format(full_jid))
            else:
                if presence_data.show != C.PRESENCE_UNAVAILABLE:
                    available.append(resource)
        return available

    def _getMainResource(self, jid_s, profile_key):
        jid_ = jid.JID(jid_s)
        return self.getMainResource(jid_, profile_key) or ""

    def getMainResource(self, entity_jid, profile_key):
        """Return the main resource used by an entity

        @param entity_jid: bare entity jid
        @param profile_key: %(doc_profile_key)s
        @return (unicode): main resource or None
        """
        if entity_jid.resource:
            raise ValueError("getMainResource must be used with a bare jid (got {})".format(entity_jid))
        try:
            if self.host.plugins["XEP-0045"].isRoom(entity_jid, profile_key):
                return None  # MUC rooms have no main resource
        except KeyError:  # plugin not found
            pass
        try:
            resources = self.getAllResources(entity_jid, profile_key)
        except exceptions.UnknownEntityError:
            log.warning(u"Entity is not in cache, we can't find any resource")
            return None
        priority_resources = []
        for resource in resources:
            full_jid = copy.copy(entity_jid)
            full_jid.resource = resource
            try:
                presence_data = self.getEntityDatum(full_jid, "presence", profile_key)
            except KeyError:
                log.debug(u"No presence information for {}".format(full_jid))
                continue
            priority_resources.append((resource, presence_data.priority))
        try:
            return max(priority_resources, key=lambda res_tuple: res_tuple[1])[0]
        except ValueError:
            log.warning(u"No resource found at all for {}".format(entity_jid))
            return None

    ## Entities data ##

    def _getProfileCache(self, profile_key):
        """Check profile validity and return its cache

        @param profile: %(doc_profile_key)_s
        @return (dict): profile cache

        @raise exceptions.ProfileUnknownError: if profile doesn't exist
        @raise exceptions.ProfileNotInCacheError: if there is no cache for this profile
        """
        profile = self.getProfileName(profile_key)
        if not profile:
            raise exceptions.ProfileUnknownError(_('Trying to get entity data for a non-existant profile'))
        try:
            profile_cache = self._entities_cache[profile]
        except KeyError:
            raise exceptions.ProfileNotInCacheError
        return profile_cache

    def setSignalOnUpdate(self, key, signal=True):
        """Set a signal flag on the key

        When the key will be updated, a signal will be sent to frontends
        @param key: key to signal
        @param signal(boolean): if True, do the signal
        """
        if signal:
            self._key_signals.add(key)
        else:
            self._key_signals.discard(key)

    def getAllEntitiesIter(self, with_bare=False, profile_key=C.PROF_KEY_NONE):
        """Return an iterator of full jids of all entities in cache

        @param with_bare: if True, include bare jids
        @param profile_key: %(doc_profile_key)s
        @return (list[unicode]): list of jids
        """
        profile_cache = self._getProfileCache(profile_key)
        # we construct a list of all known full jids (bare jid of entities x resources)
        for bare_jid, entity_data in profile_cache.iteritems():
            for resource in entity_data.iterkeys():
                if resource is None:
                    continue
                full_jid = copy.copy(bare_jid)
                full_jid.resource = resource
                yield full_jid

    def updateEntityData(self, entity_jid, key, value, silent=False, profile_key=C.PROF_KEY_NONE):
        """Set a misc data for an entity

        If key was registered with setSignalOnUpdate, a signal will be sent to frontends
        @param entity_jid: JID of the entity, C.ENTITY_ALL_RESOURCES for all resources of all entities,
                           C.ENTITY_ALL for all entities (all resources + bare jids)
        @param key: key to set (eg: "type")
        @param value: value for this key (eg: "chatroom")
        @param silent(bool): if True, doesn't send signal to frontend, even if there is a signal flag (see setSignalOnUpdate)
        @param profile_key: %(doc_profile_key)s
        """
        profile_cache = self._getProfileCache(profile_key)
        if entity_jid in (C.ENTITY_ALL_RESOURCES, C.ENTITY_ALL):
            entities = self.getAllEntitiesIter(entity_jid==C.ENTITY_ALL, profile_key)
        else:
            entities = (entity_jid,)

        for jid_ in entities:
            entity_data = profile_cache.setdefault(jid_.userhostJID(),{}).setdefault(jid_.resource, {})

            entity_data[key] = value
            if key in self._key_signals and not silent:
                if not isinstance(value, basestring):
                    log.error(u"Setting a non string value ({}) for a key ({}) which has a signal flag".format(value, key))
                else:
                    self.host.bridge.entityDataUpdated(jid_.full(), key, value, self.getProfileName(profile_key))

    def delEntityDatum(self, entity_jid, key, profile_key):
        """Delete a data for an entity

        @param entity_jid: JID of the entity, C.ENTITY_ALL_RESOURCES for all resources of all entities,
                           C.ENTITY_ALL for all entities (all resources + bare jids)
        @param key: key to delete (eg: "type")
        @param profile_key: %(doc_profile_key)s

        @raise exceptions.UnknownEntityError: if entity is not in cache
        @raise KeyError: key is not in cache
        """
        profile_cache = self._getProfileCache(profile_key)
        if entity_jid in (C.ENTITY_ALL_RESOURCES, C.ENTITY_ALL):
            entities = self.getAllEntitiesIter(entity_jid==C.ENTITY_ALL, profile_key)
        else:
            entities = (entity_jid,)

        for jid_ in entities:
            try:
                entity_data = profile_cache[jid_.userhostJID()][jid_.resource]
            except KeyError:
                raise exceptions.UnknownEntityError(u"Entity {} not in cache".format(jid_))
            try:
                del entity_data[key]
            except KeyError as e:
                if entity_jid in (C.ENTITY_ALL_RESOURCES, C.ENTITY_ALL):
                    continue # we ignore KeyError when deleting keys from several entities
                else:
                    raise e

    def _getEntitiesData(self, entities_jids, keys_list, profile_key):
        ret = self.getEntitiesData([jid.JID(jid_) for jid_ in entities_jids], keys_list, profile_key)
        return {jid_.full(): data for jid_, data in ret.iteritems()}

    def getEntitiesData(self, entities_jids, keys_list=None, profile_key=C.PROF_KEY_NONE):
        """Get a list of cached values for several entities at once

        @param entities_jids: jids of the entities, or empty list for all entities in cache
        @param keys_list (iterable,None): list of keys to get, None for everything
        @param profile_key: %(doc_profile_key)s
        @return: dict withs values for each key in keys_list.
                 if there is no value of a given key, resulting dict will
                 have nothing with that key nether
                 if an entity doesn't exist in cache, it will not appear
                 in resulting dict

        @raise exceptions.UnknownEntityError: if entity is not in cache
        """
        def fillEntityData(entity_cache_data):
            entity_data = {}
            if keys_list is None:
                entity_data = entity_cache_data
            else:
                for key in keys_list:
                    try:
                        entity_data[key] = entity_cache_data[key]
                    except KeyError:
                        continue
            return entity_data

        profile_cache = self._getProfileCache(profile_key)
        ret_data = {}
        if entities_jids:
            for entity in entities_jids:
                try:
                    entity_cache_data = profile_cache[entity.userhostJID()][entity.resource]
                except KeyError:
                    continue
                ret_data[entity.full()] = fillEntityData(entity_cache_data, keys_list)
        else:
            for bare_jid, data in profile_cache.iteritems():
                for resource, entity_cache_data in data.iteritems():
                    full_jid = copy.copy(bare_jid)
                    full_jid.resource = resource
                    ret_data[full_jid] = fillEntityData(entity_cache_data)

        return ret_data

    def getEntityData(self, entity_jid, keys_list=None, profile_key=C.PROF_KEY_NONE):
        """Get a list of cached values for entity

        @param entity_jid: JID of the entity
        @param keys_list (iterable,None): list of keys to get, None for everything
        @param profile_key: %(doc_profile_key)s
        @return: dict withs values for each key in keys_list.
                 if there is no value of a given key, resulting dict will
                 have nothing with that key nether

        @raise exceptions.UnknownEntityError: if entity is not in cache
        """
        profile_cache = self._getProfileCache(profile_key)
        try:
            entity_data = profile_cache[entity_jid.userhostJID()][entity_jid.resource]
        except KeyError:
            raise exceptions.UnknownEntityError(u"Entity {} not in cache (was requesting {})".format(entity_jid, keys_list))
        if keys_list is None:
            return entity_data

        return {key: entity_data[key] for key in keys_list if key in entity_data}

    def getEntityDatum(self, entity_jid, key, profile_key):
        """Get a datum from entity

        @param entity_jid: JID of the entity
        @param keys: key to get
        @param profile_key: %(doc_profile_key)s
        @return: requested value

        @raise exceptions.UnknownEntityError: if entity is not in cache
        @raise KeyError: if there is no value for this key and this entity
        """
        return self.getEntityData(entity_jid, (key,), profile_key)[key]

    def delEntityCache(self, entity_jid, delete_all_resources=True, profile_key=C.PROF_KEY_NONE):
        """Remove all cached data for entity

        @param entity_jid: JID of the entity to delete
        @param delete_all_resources: if True also delete all known resources from cache (a bare jid must be given in this case)
        @param profile_key: %(doc_profile_key)s

        @raise exceptions.UnknownEntityError: if entity is not in cache
        """
        profile_cache = self._getProfileCache(profile_key)

        if delete_all_resources:
            if entity_jid.resource:
                raise ValueError(_("Need a bare jid to delete all resources"))
            try:
                del profile_cache[entity_jid]
            except KeyError:
                raise exceptions.UnknownEntityError(u"Entity {} not in cache".format(entity_jid))
        else:
            try:
                del profile_cache[entity_jid.userhostJID()][entity_jid.resource]
            except KeyError:
                raise exceptions.UnknownEntityError(u"Entity {} not in cache".format(entity_jid))

    ## Encryption ##

    def encryptValue(self, value, profile):
        """Encrypt a value for the given profile. The personal key must be loaded
        already in the profile session, that should be the case if the profile is
        already authenticated.

        @param value (str): the value to encrypt
        @param profile (str): %(doc_profile)s
        @return: the deferred encrypted value
        """
        try:
            personal_key = self.auth_sessions.profileGetUnique(profile)[C.MEMORY_CRYPTO_KEY]
        except TypeError:
            raise exceptions.InternalError(_('Trying to encrypt a value for %s while the personal key is undefined!') % profile)
        return BlockCipher.encrypt(personal_key, value)

    def decryptValue(self, value, profile):
        """Decrypt a value for the given profile. The personal key must be loaded
        already in the profile session, that should be the case if the profile is
        already authenticated.

        @param value (str): the value to decrypt
        @param profile (str): %(doc_profile)s
        @return: the deferred decrypted value
        """
        try:
            personal_key = self.auth_sessions.profileGetUnique(profile)[C.MEMORY_CRYPTO_KEY]
        except TypeError:
            raise exceptions.InternalError(_('Trying to decrypt a value for %s while the personal key is undefined!') % profile)
        return BlockCipher.decrypt(personal_key, value)

    def encryptPersonalData(self, data_key, data_value, crypto_key, profile):
        """Re-encrypt a personal data (saved to a PersistentDict).

        @param data_key: key for the individual PersistentDict instance
        @param data_value: the value to be encrypted
        @param crypto_key: the key to encrypt the value
        @param profile: %(profile_doc)s
        @return: a deferred None value
        """

        def gotIndMemory(data):
            d = BlockCipher.encrypt(crypto_key, data_value)

            def cb(cipher):
                data[data_key] = cipher
                return data.force(data_key)

            return d.addCallback(cb)

        def done(dummy):
            log.debug(_(u'Personal data (%(ns)s, %(key)s) has been successfuly encrypted') %
                      {'ns': C.MEMORY_CRYPTO_NAMESPACE, 'key': data_key})

        d = PersistentDict(C.MEMORY_CRYPTO_NAMESPACE, profile).load()
        return d.addCallback(gotIndMemory).addCallback(done)

    ## Subscription requests ##

    def addWaitingSub(self, type_, entity_jid, profile_key):
        """Called when a subcription request is received"""
        profile = self.getProfileName(profile_key)
        assert profile
        if profile not in self.subscriptions:
            self.subscriptions[profile] = {}
        self.subscriptions[profile][entity_jid] = type_

    def delWaitingSub(self, entity_jid, profile_key):
        """Called when a subcription request is finished"""
        profile = self.getProfileName(profile_key)
        assert profile
        if profile in self.subscriptions and entity_jid in self.subscriptions[profile]:
            del self.subscriptions[profile][entity_jid]

    def getWaitingSub(self, profile_key):
        """Called to get a list of currently waiting subscription requests"""
        profile = self.getProfileName(profile_key)
        if not profile:
            log.error(_('Asking waiting subscriptions for a non-existant profile'))
            return {}
        if profile not in self.subscriptions:
            return {}

        return self.subscriptions[profile]

    ## Parameters ##

    def getStringParamA(self, name, category, attr="value", profile_key=C.PROF_KEY_NONE):
        return self.params.getStringParamA(name, category, attr, profile_key)

    def getParamA(self, name, category, attr="value", profile_key=C.PROF_KEY_NONE):
        return self.params.getParamA(name, category, attr, profile_key=profile_key)

    def asyncGetParamA(self, name, category, attr="value", security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        return self.params.asyncGetParamA(name, category, attr, security_limit, profile_key)

    def asyncGetParamsValuesFromCategory(self, category, security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        return self.params.asyncGetParamsValuesFromCategory(category, security_limit, profile_key)

    def asyncGetStringParamA(self, name, category, attr="value", security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        return self.params.asyncGetStringParamA(name, category, attr, security_limit, profile_key)

    def getParamsUI(self, security_limit=C.NO_SECURITY_LIMIT, app='', profile_key=C.PROF_KEY_NONE):
        return self.params.getParamsUI(security_limit, app, profile_key)

    def getParamsCategories(self):
        return self.params.getParamsCategories()

    def setParam(self, name, value, category, security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        return self.params.setParam(name, value, category, security_limit, profile_key)

    def updateParams(self, xml):
        return self.params.updateParams(xml)

    def paramsRegisterApp(self, xml, security_limit=C.NO_SECURITY_LIMIT, app=''):
        return self.params.paramsRegisterApp(xml, security_limit, app)

    def setDefault(self, name, category, callback, errback=None):
        return self.params.setDefault(name, category, callback, errback)

    ## Misc ##

    def isEntityAvailable(self, entity_jid, profile_key):
        """Tell from the presence information if the given entity is available.

        @param entity_jid (JID): the entity to check (if bare jid is used, all resources are tested)
        @param profile_key: %(doc_profile_key)s
        @return (bool): True if entity is available
        """
        if not entity_jid.resource:
            return bool(self.getAvailableResources) # is any resource is available, entity is available
        try:
            presence_data = self.getEntityDatum(entity_jid, "presence", profile_key)
        except KeyError:
            log.debug(u"No presence information for {}".format(entity_jid))
            return False
        return presence_data.show != C.PRESENCE_UNAVAILABLE
