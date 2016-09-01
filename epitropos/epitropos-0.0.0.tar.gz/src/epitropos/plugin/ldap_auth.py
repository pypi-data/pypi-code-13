# -*- coding: utf-8 -*-
import ldap

from epitropos.plugin import (
    auth_plugin,
    AuthPlugin
)
from malibu.design.brine import CachingBrineObject
from malibu.util.log import LoggingDriver

_SCOPE_MAP = {
    'sub': ldap.SCOPE_SUBTREE,
    'one': ldap.SCOPE_ONELEVEL,
    'ord': ldap.SCOPE_SUBORDINATE,
    'base': ldap.SCOPE_BASE,
}

_LOG = LoggingDriver.find_logger()


class LdapScopesCache(CachingBrineObject):

    def __init__(self):

        self.username = None
        self.scopes = set()

        super(LdapScopesCache, self).__init__(self, timestamp=True, uuid=True)


@auth_plugin(
    name='ldap'
)
class LdapAuth(AuthPlugin):
    """ Performs authentication of a user against an LDAP backend.
    """

    @classmethod
    def requirements(cls):
        """ Requirements (from pip) for using this plugin.
        """

        return [
            'pyldap == 2.4.25.1',
        ]

    def __init__(self, **options):

        super(self.__class__, self).__init__(**options)

        self.debug = False
        if 'debug' in options:
            self.debug = options.get('debug')

        self.config = self._auth_cfg.get('ldap', {})
        self.log = LoggingDriver.find_logger()

        self._connect()

    def _connect(self):
        """ Performs the LDAP connection.
        """

        self.ldap_uri = self.config.get('uri', None)
        if not self.ldap_uri:
            raise Exception('No LDAP URI! Set auth:ldap.uri in your config.')

        ldap_starttls = self.config.get_bool('starttls', False)
        ldap_binddn = self.config.get('binddn', None)
        ldap_bindpw = self.config.get('bindpw', None)
        auth_tup = (None, None,)
        if not ldap_binddn or not ldap_bindpw:
            self.log.notice('No binddn or bindpw set! Binding anonymously.')
            auth_tup = ('', '',)
        else:
            auth_tup = (ldap_binddn, ldap_bindpw,)

        self.log.debug('Initializing LDAP client: %s' % (self.ldap_uri))
        if self.debug:
            self._client = ldap.initialize(self.ldap_uri, trace_level=2)
        else:
            self._client = ldap.initialize(self.ldap_uri)

        if ldap_starttls:
            self.log.debug('Sending STARTTLS...')
            self._client.start_tls_s()
            self.log.info('TLS successfully negotiated!')

        self.log.debug('Attempting directory bind...')
        self._client.bind_s(*auth_tup)
        self._auth_tup = auth_tup

        self.log.info('Bind successful! DN: %s' % (ldap_binddn))

    def authenticate(self, username, password):
        """ Authenticates a user against the LDAP backend.
        """

        # To do this, we need to do a multi-step process.
        # 1) Ensure that the user even exists before we attempt a bind.
        # 2) Try to bind as the user.

        user_base = self.config.get('userbase', None)
        user_filter = self.config.get('userfilter', None)
        user_scope = self.config.get('userscope', 'sub')
        try:
            user_scope = _SCOPE_MAP[user_scope]
        except IndexError:
            user_scope = ldap.SCOPE_SUBTREE

        if not user_base or not user_filter:
            raise Exception('No userbase or userfilter configured')

        # 1) Search for the user.
        fmt = {
            'username': username,
        }

        result = self._client.search_s(
            user_base,
            user_scope,
            filterstr=user_filter.format(**fmt),
            attrlist=['objectClass'])

        if not result:
            return False

        if len(result) >= 1:
            # Uhm, how do we handle > 1?
            result = result[0]
            fmt.update({
                'userdn': result[0],
            })

        userdn = result[0]

        # 2) Bind as the user.
        try:
            with self._rebind_user(userdn, password) as cl:
                who = cl.whoami_s().split(':')[1]
                self.log.debug('rebind/whoami ===> %s/%s' % (userdn, who))
                if not who == userdn:
                    self.log.error('WHOAMI does not match found userdn!')
                    return False
            return True
        except ldap.error:
            # Most likely an auth error.
            return False

        return False

    def scopes(self, username):
        """ Finds all groups that the given user is a member of.

            Scope lookups will always be cached because they are relatively
            expensive.
        """

        cached = LdapScopesCache.search(username=username)
        if len(cached) == 1:
            return cached[0].scopes
        else:
            _LOG.info('Could not find cached scopes for %s' % (username))

        # This is also a multi-step process. To properly do this, we actually
        # should do several lookups, mainly because refint/memberOf can be
        # slightly sketchy.
        # 1a) Perform a username lookup to get the user's full DN.
        # 1b) Check lookup result for memberOf attributes.
        # 2) Use userdn to perform a group lookup for member attributes.

        user_base = self.config.get('userbase', None)
        user_filter = self.config.get('userfilter', None)
        user_scope = self.config.get('userscope', 'sub')

        group_base = self.config.get('groupbase', None)
        group_filter = self.config.get('groupfilter', None)
        group_scope = self.config.get('groupscope', 'sub')

        try:
            user_scope = _SCOPE_MAP[user_scope]
            group_scope = _SCOPE_MAP[group_scope]
        except IndexError:
            user_scope = ldap.SCOPE_SUBTREE
            group_scope = ldap.SCOPE_SUBTREE

        if not user_base or not user_filter:
            raise Exception('No userbase or userfilter configured')

        if not group_base or not group_filter:
            raise Exception('No groupbase or groupfilter configured')

        # Create the user's cache object.
        scopecache = LdapScopesCache()
        scopecache.username = username

        # 1) Search for the user.
        fmt = {
            'username': username,
        }

        result = self._client.search_s(
            user_base,
            user_scope,
            filterstr=user_filter.format(**fmt),
            attrlist=['memberOf'])

        if not result:
            scopecache.uncache()
            return None

        if len(result) >= 1:
            # Uhm, how do we handle > 1?
            result = result[0]
            fmt.update({
                'userdn': result[0],
            })

        userdn, userattrs = result

        usergroups = userattrs.get('memberOf', [])
        if len(usergroups) > 0:
            # Process the groupdns that were found
            usergroups = frozenset(self._strip_groupdns(usergroups))
            scopecache.scopes = usergroups
            return usergroups

        # Not found in the user query, search for groups with member={userdn}
        result = self._client.search_s(
            group_base,
            group_scope,
            filterstr=group_filter.format(**fmt),
            attrlist=['member'])

        if not result:
            scopecache.uncache()
            return None

        # This result will be > 1 if the user is in multiple groups.
        usergroups = [gr[0] for gr in result]
        if len(usergroups) > 0:
            usergroups = frozenset(self._strip_groupdns(usergroups))
            scopecache.scopes = usergroups
            return usergroups

        return None

    def ping(self):
        """ Sends a whoami query to the LDAP server as a sort of ping.
        """

        result = self._client.whoami_s()
        if result and result == 'dn:' + self._auth_tup[0]:
            return True

        return False

    def _strip_groupdns(self, groups):
        """ Takes a list of group DNs and strips them down to *only* the
            CN used to designate it.
        """

        g = set()

        for group in groups:
            cn = group.split(',')[0]
            cn = cn.split('=')[1]
            g.add(cn)

        return g

    def _rebind_user(self, userdn, password):
        """ Returns a context manager which performs rebind on the LDAP
            client. Useful for performing actions, such as a password change,
            as the user.
        """

        class _LdapRebindWithUserContext(object):

            def __init__(self, plugin, binddn, bindpw):

                self.log = LoggingDriver.find_logger()
                self.plugin = plugin
                self.binddn = binddn
                self.bindpw = bindpw

            def __enter__(self):

                self._client = self.plugin._client
                auth_tup = (self.binddn, self.bindpw,)

                try:
                    self._client.unbind_s()
                except Exception as e:
                    # TODO: Find a more graceful way to handle this.
                    raise e

                try:
                    if self.plugin.debug:
                        self._client = ldap.initialize(
                            self.plugin.ldap_uri,
                            trace_level=2)
                    else:
                        self._client = ldap.initialize(
                            self.plugin.ldap_uri)
                    self._client.bind_s(*auth_tup)
                except Exception as e:
                    # This is an auth failure.
                    raise e

                self.log.info('User bind successful! DN: %s' %
                              (self.binddn))

                return self._client

            def __exit__(self, exc_type, exc_value, traceback):

                try:
                    self._client.unbind_s()
                except Exception as e:
                    # TODO: Find a more graceful way to handle this.
                    raise e

                try:
                    self.plugin._connect()
                except Exception as e:
                    # This is an auth failure, BUT, it's a failure with the
                    # credentials used to bind the first time (from the auth
                    # configuration).
                    wrap = Exception('Auth failure with previously used '
                                     'credentials -- bug?')
                    wrap.cause = e
                    raise wrap

        return _LdapRebindWithUserContext(self, userdn, password)
