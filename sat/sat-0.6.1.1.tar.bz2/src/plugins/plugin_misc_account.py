#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT plugin for account creation (experimental)
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
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.core import exceptions
from sat.tools import xml_tools
from sat.memory.memory import Sessions
from sat.memory.crypto import PasswordHasher
from sat.core.constants import Const as C
import ConfigParser
from twisted.internet import reactor, defer, protocol
from twisted.python.procutils import which
from twisted.python.failure import Failure
from twisted.mail.smtp import sendmail
from os.path import join, dirname
from email.mime.text import MIMEText

import random


PLUGIN_INFO = {
    "name": "Account Plugin",
    "import_name": "MISC-ACCOUNT",
    "type": "MISC",
    "protocols": [],
    "dependencies": [],
    "recommendations": ['GROUPBLOG'],
    "main": "MiscAccount",
    "handler": "no",
    "description": _(u"""SàT account creation""")
}

CONFIG_SECTION = "plugin account"

# You need do adapt the following consts to your server
# all theses values (key=option name, value=default) can (and should) be overriden in sat.conf
# in section CONFIG_SECTION

default_conf = {"email_from": "NOREPLY@example.net",
                "email_server": "localhost",
                "email_sender_domain": "",
                "email_port": 25,
                "email_username": "",
                "email_password": "",
                "email_starttls": "false",
                "email_auth": "false",
                "email_admins_list": [],
                "admin_email": "",
                "new_account_server": "localhost",
                "new_account_domain": "example.net",
                "prosody_path": None, # prosody path (where prosodyctl will be executed from), or None to automaticaly find it
                "prosodyctl": "prosodyctl",
                "reserved_list": ['libervia'] # profiles which can't be used
               }


class PasswordsMatchingError(Exception):
    pass


class ProsodyRegisterProtocol(protocol.ProcessProtocol):
    """ Try to register an account with prosody """

    def __init__(self, password=None, deferred=None):
        """
        @param password: new user password
        @param deferred
        """
        self.password = password
        self.deferred = deferred
        self.data = ''

    def connectionMade(self):
        if self.password is None:
            return
        self.transport.write("%s\n%s" % ((self.password.encode('utf-8'),) * 2))
        self.transport.closeStdin()

    def outReceived(self, data):
        self.data += data

    def errReceived(self, data):
        self.data += data

    def processEnded(self, reason):
        if (reason.value.exitCode == 0):
            log.info(_('Prosody command succeed'))
            self.deferred.callback(None)
        else:
            log.error(_(u"Can't complete Prosody command (error code: %(code)d): %(message)s") % {'code': reason.value.exitCode, 'message': self.data})
            self.deferred.errback(Failure(exceptions.InternalError))

    @classmethod
    def prosodyctl(cls, plugin, command, password=None, profile=None):
        """Create a new ProsodyRegisterProtocol and execute the given prosodyctl command.

        @param plugin: instance of MiscAccount
        @param command: the command to execute: "adduser", "passwd" or "deluser"
        @param password: the user new password (leave to None for "deluser" command)
        @param profile: the user profile
        @return: a Deferred instance
        """
        d = defer.Deferred()
        prosody_reg = ProsodyRegisterProtocol(password, d)
        prosody_exe = join(plugin._prosody_path, plugin.getConfig('prosodyctl'))
        # TODO delete account which are not on the same host
        reactor.spawnProcess(prosody_reg, prosody_exe, [prosody_exe, command, "%s@%s" % (profile, plugin.getConfig('new_account_domain'))], path=plugin._prosody_path)
        return d


class MiscAccount(object):
    """Account plugin: create a SàT + Prosody account, used by Libervia"""
    #XXX: This plugin is a Q&D one used for the demo. Something more generic (and not
    #     only focused on Prosody) is planed

    def __init__(self, host):
        log.info(_(u"Plugin Account initialization"))
        self.host = host
        host.bridge.addMethod("registerSatAccount", ".plugin", in_sign='sss', out_sign='', method=self._registerAccount, async=True)
        host.bridge.addMethod("getNewAccountDomain", ".plugin", in_sign='', out_sign='s', method=self.getNewAccountDomain, async=False)
        host.bridge.addMethod("getAccountDialogUI", ".plugin", in_sign='s', out_sign='s', method=self._getAccountDialogUI, async=False)
        host.bridge.addMethod("asyncConnectWithXMPPCredentials", ".plugin", in_sign='ss', out_sign='b', method=self.asyncConnectWithXMPPCredentials, async=True)
        self._prosody_path = self.getConfig('prosody_path')
        if self._prosody_path is None:
            paths = which(self.getConfig('prosodyctl'))
            if not paths:
                log.error(_(u"Can't find %s") % (self.getConfig('prosodyctl'),))
            else:
                self._prosody_path = dirname(paths[0])
                log.info(_(u'Prosody path found: %s') % (self._prosody_path,))

        self.fixEmailAdmins()
        self._sessions = Sessions()

        self.__account_cb_id = host.registerCallback(self._accountDialogCb, with_data=True)
        self.__change_password_id = host.registerCallback(self.__changePasswordCb, with_data=True)

        def deleteBlogCallback(posts, comments):
            return lambda data, profile: self.__deleteBlogPostsCb(posts, comments, data, profile)

        self.__delete_posts_id = host.registerCallback(deleteBlogCallback(True, False), with_data=True)
        self.__delete_comments_id = host.registerCallback(deleteBlogCallback(False, True), with_data=True)
        self.__delete_posts_comments_id = host.registerCallback(deleteBlogCallback(True, True), with_data=True)

        self.__delete_account_id = host.registerCallback(self.__deleteAccountCb, with_data=True)


    # FIXME: remove this after some time, when the deprecated parameter is really abandoned
    def fixEmailAdmins(self):
        """Handle deprecated config option "admin_email" to fix the admin emails list"""
        admin_email = self.getConfig('admin_email')
        if not admin_email:
            return
        log.warning(u"admin_email parameter is deprecated, please use email_admins_list instead")
        param_name = "email_admins_list"
        try:
            section = ""
            value = self.host.memory.getConfig(section, param_name, Exception)
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            section = CONFIG_SECTION
            value = self.host.memory.getConfig(section, param_name, default_conf[param_name])

        value = set(value)
        value.add(admin_email)
        self.host.memory.config.set(section, param_name, ",".join(value))

    def getConfig(self, name):
        if name.startswith("email_"):
            # XXX: email_ parameters were first in [plugin account] section
            #      but as it make more sense to have them in common with other plugins,
            #      they can now be in [DEFAULT] section
            try:
                value = self.host.memory.getConfig(None, name, Exception)
            except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
                pass
            else:
                return value

        return self.host.memory.getConfig(CONFIG_SECTION, name, default_conf[name])

    def generatePassword(self):
        """Generate a password with random characters.

        @return unicode
        """
        random.seed()
        #charset = [chr(i) for i in range(0x21,0x7F)] #XXX: this charset seems to have some issues with openfire
        charset = [chr(i) for i in range(0x30,0x3A) + range(0x41,0x5B) + range (0x61,0x7B)]
        return ''.join([random.choice(charset) for i in range(15)])

    def _registerAccount(self, email, password, profile):
        return self.registerAccount(email, password, None, profile)

    def registerAccount(self, email, password, jid_s, profile):
        """Register a new profile, its associated XMPP account, send the confirmation emails.

        @param email (unicode): where to send to confirmation email to
        @param password (unicode): password chosen by the user
            while be used for profile *and* XMPP account
        @param jid_s (unicode): JID to re-use or to register:
            - non empty value: bind this JID to the new sat profile
            - None or "": register a new JID on the local XMPP server
        @param profile
        @return Deferred
        """
        d = self.createProfile(password, jid_s, profile)
        d.addCallback(lambda dummy: self.sendEmails(email, profile))
        return d

    def createProfile(self, password, jid_s, profile):
        """Register a new profile and its associated XMPP account.

        @param password (unicode): password chosen by the user
            while be used for profile *and* XMPP account
        @param jid_s (unicode): JID to re-use or to register:
            - non empty value: bind this JID to the new sat profile
            - None or "": register a new JID on the local XMPP server
        @param profile
        @return Deferred
        """
        if not password or not profile:
            raise exceptions.DataError

        if profile.lower() in self.getConfig('reserved_list'):
            return defer.fail(Failure(exceptions.ConflictError))

        d = self.host.memory.asyncCreateProfile(profile, password)
        d.addCallback(lambda dummy: self.profileCreated(password, jid_s, profile))
        return d

    def profileCreated(self, password, jid_s, profile):
        """Create the XMPP account and set the profile connection parameters.

        @param password (unicode): password chosen by the user
        @param jid_s (unicode): JID to re-use or to register:
            - non empty value: bind this JID to the new sat profile
            - None or empty: register a new JID on the local XMPP server
        @param profile
        @return: Deferred
        """
        # XXX: we use "prosodyctl adduser" because "register" doesn't check conflict and just change the password if the account already exists
        if jid_s:
            d = defer.succeed(None)
        else:
            d = ProsodyRegisterProtocol.prosodyctl(self, 'adduser', password, profile)
            jid_s = "%s@%s" % (profile, self.getConfig('new_account_domain'))

        def setParams(dummy):
            self.host.memory.setParam("JabberID", jid_s, "Connection", profile_key=profile)
            d = self.host.memory.setParam("Password", password, "Connection", profile_key=profile)
            return d

        def removeProfile(failure):
            self.host.memory.asyncDeleteProfile(profile)
            return failure

        d.addCallback(lambda dummy: self.host.memory.startSession(password, profile))
        d.addCallback(setParams)
        d.addCallback(lambda dummy: self.host.memory.stopSession(profile))
        d.addErrback(removeProfile)
        return d

    def sendEmails(self, email, profile):
        # time to send the email

        email_host = self.getConfig('email_server')
        email_from = self.getConfig("email_from")
        email_sender_domain = self.getConfig("email_sender_domain") or None
        email_port = int(self.getConfig("email_port"))
        email_username = self.getConfig("email_username") or None
        email_password = self.getConfig("email_password") or None
        email_starttls = C.bool(self.getConfig("email_starttls"))
        email_auth = C.bool(self.getConfig("email_auth"))
        domain = self.getConfig('new_account_domain')

        def sendEmail(recipients, msg):
            return sendmail(email_host.encode("utf-8"),
                            email_from.encode("utf-8"),
                            [email.encode("utf-8") for email in recipients],
                            msg.as_string(),
                            senderDomainName=email_sender_domain.encode("utf-8") if email_sender_domain else None,
                            port=email_port,
                            username=email_username.encode("utf-8") if email_username else None,
                            password=email_password.encode("utf-8") if email_password else None,
                            requireAuthentication=email_starttls,
                            requireTransportSecurity=email_auth)

        # email to the administrators
        admins_emails = self.getConfig('email_admins_list')
        if not admins_emails:
            log.warning(u"No known admin email, we can't send email to administrator(s).\nPlease fill email_admins_list parameter")
            d_admin = defer.fail(exceptions.DataError("no admin email"))
        else:
            body = (u"""New account created: %(profile)s [%(email)s]""" % {'profile': profile, 'email': email}).encode('utf-8')
            msg = MIMEText(body, 'plain', 'UTF-8')
            msg['Subject'] = _('New Libervia account created')
            msg['From'] = email_from
            msg['To'] = ", ".join(admins_emails)

            d_admin = sendEmail(admins_emails, msg)
        admins_emails_txt = u', '.join([u"<{}>".format(addr) for addr in admins_emails])
        d_admin.addCallbacks(lambda dummy: log.debug(u"Account creation notification sent to admin(s) {}".format(admins_emails_txt)),
                             lambda dummy: log.error(u"Failed to send account creation notification to admin {}".format(admins_emails_txt)))
        if not email:
            return d_admin

        jid_s = self.host.memory.getParamA("JabberID", "Connection", profile_key=profile)
        body = (_(u"""Welcome to Libervia, the web interface of Salut à Toi.

Your account on {domain} has been successfully created. This is a demonstration version to show you the current status of the project. It is still under development, please keep it in mind!

Here is your connection information:

Login on {domain}: {profile}
Jabber ID (JID): {jid}
Your password has been chosen by yourself during registration.

In the beginning, you have nobody to talk to. To find some contacts, you may use the users' directory:
    - make yourself visible in "Service / Directory subscription".
    - search for people with "Contacts" / Search directory".

Any feedback welcome. Thank you!

Salut à Toi association
http://www.salut-a-toi.org
""").format(profile=profile, jid=jid_s, domain=domain)).encode('utf-8')
        msg = MIMEText(body, 'plain', 'UTF-8')
        msg['Subject'] = _(u'Libervia account created')
        msg['From'] = email_from
        msg['To'] = email

        def email_ko(dummy):
            # TODO: return error code to user
            log.error(u"Failed to send account creation confirmation to <%s>" % email)

        # XXX: this will not fail when the email address doesn't exist
        # FIXME: check email reception to validate email given by the user
        # FIXME: delete the profile if the email could not been sent?
        d_user = sendEmail([email], msg)
        d_user.addCallbacks(lambda dummy: log.debug(u"Account creation confirmation sent to <%s>" % email),
                            email_ko)
        return defer.DeferredList([d_user, d_admin])

    def getNewAccountDomain(self):
        """@return: the domain that will be set to new account"""
        return self.getConfig('new_account_domain')

    def _getAccountDialogUI(self, profile):
        """Get the main dialog to manage your account
        @param menu_data
        @param profile: %(doc_profile)s
        @return: XML of the dialog
        """
        form_ui = xml_tools.XMLUI("form", "tabs", title=D_("Manage your account"), submit_id=self.__account_cb_id)
        tab_container = form_ui.current_container

        tab_container.addTab("update", D_("Change your password"), container=xml_tools.PairsContainer)
        form_ui.addLabel(D_("Current profile password"))
        form_ui.addPassword("current_passwd", value="")
        form_ui.addLabel(D_("New password"))
        form_ui.addPassword("new_passwd1", value="")
        form_ui.addLabel(D_("New password (again)"))
        form_ui.addPassword("new_passwd2", value="")

        # FIXME: uncomment and fix these features
        """
        if 'GROUPBLOG' in self.host.plugins:
            tab_container.addTab("delete_posts", D_("Delete your posts"), container=xml_tools.PairsContainer)
            form_ui.addLabel(D_("Current profile password"))
            form_ui.addPassword("delete_posts_passwd", value="")
            form_ui.addLabel(D_("Delete all your posts and their comments"))
            form_ui.addBool("delete_posts_checkbox", "false")
            form_ui.addLabel(D_("Delete all your comments on other's posts"))
            form_ui.addBool("delete_comments_checkbox", "false")

        tab_container.addTab("delete", D_("Delete your account"), container=xml_tools.PairsContainer)
        form_ui.addLabel(D_("Current profile password"))
        form_ui.addPassword("delete_passwd", value="")
        form_ui.addLabel(D_("Delete your account"))
        form_ui.addBool("delete_checkbox", "false")
        """

        return form_ui.toXml()

    @defer.inlineCallbacks
    def _accountDialogCb(self, data, profile):
        """Called when the user submits the main account dialog
        @param data
        @param profile
        """
        sat_cipher = yield self.host.memory.asyncGetParamA(C.PROFILE_PASS_PATH[1], C.PROFILE_PASS_PATH[0], profile_key=profile)

        @defer.inlineCallbacks
        def verify(attempt):
            auth = yield PasswordHasher.verify(attempt, sat_cipher)
            defer.returnValue(auth)

        def error_ui(message=None):
            if not message:
                message = D_("The provided profile password doesn't match.")
            error_ui = xml_tools.XMLUI("popup", title=D_("Attempt failure"))
            error_ui.addText(message)
            return {'xmlui': error_ui.toXml()}

        # check for account deletion
        # FIXME: uncomment and fix these features
        """
        delete_passwd = data[xml_tools.SAT_FORM_PREFIX + 'delete_passwd']
        delete_checkbox = data[xml_tools.SAT_FORM_PREFIX + 'delete_checkbox']
        if delete_checkbox == 'true':
            verified = yield verify(delete_passwd)
            assert isinstance(verified, bool)
            if verified:
                defer.returnValue(self.__deleteAccount(profile))
            defer.returnValue(error_ui())

        # check for blog posts deletion
        if 'GROUPBLOG' in self.host.plugins:
            delete_posts_passwd = data[xml_tools.SAT_FORM_PREFIX + 'delete_posts_passwd']
            delete_posts_checkbox = data[xml_tools.SAT_FORM_PREFIX + 'delete_posts_checkbox']
            delete_comments_checkbox = data[xml_tools.SAT_FORM_PREFIX + 'delete_comments_checkbox']
            posts = delete_posts_checkbox == 'true'
            comments = delete_comments_checkbox == 'true'
            if posts or comments:
                verified = yield verify(delete_posts_passwd)
                assert isinstance(verified, bool)
                if verified:
                    defer.returnValue(self.__deleteBlogPosts(posts, comments, profile))
                defer.returnValue(error_ui())
        """

        # check for password modification
        current_passwd = data[xml_tools.SAT_FORM_PREFIX + 'current_passwd']
        new_passwd1 = data[xml_tools.SAT_FORM_PREFIX + 'new_passwd1']
        new_passwd2 = data[xml_tools.SAT_FORM_PREFIX + 'new_passwd2']
        if new_passwd1 or new_passwd2:
            verified = yield verify(current_passwd)
            assert isinstance(verified, bool)
            if verified:
                if new_passwd1 == new_passwd2:
                    data = yield self.__changePassword(new_passwd1, profile=profile)
                    defer.returnValue(data)
                else:
                    defer.returnValue(error_ui(D_("The values entered for the new password are not equal.")))
            defer.returnValue(error_ui())

        defer.returnValue({})

    def __changePassword(self, password, profile):
        """Ask for a confirmation before changing the XMPP account and SàT profile passwords.

        @param password (str): the new password
        @param profile (str): %(doc_profile)s
        """
        session_id, dummy = self._sessions.newSession({'new_password': password}, profile=profile)
        form_ui = xml_tools.XMLUI("form", title=D_("Change your password?"), submit_id=self.__change_password_id, session_id=session_id)
        form_ui.addText(D_("Note for advanced users: this will actually change both your SàT profile password AND your XMPP account password."))
        form_ui.addText(D_("Continue with changing the password?"))
        return {'xmlui': form_ui.toXml()}

    def __changePasswordCb(self, data, profile):
        """Actually change the user XMPP account and SàT profile password
        @param data (dict)
        @profile (str): %(doc_profile)s
        """
        password = self._sessions.profileGet(data['session_id'], profile)['new_password']
        del self._sessions[data['session_id']]

        def passwordChanged(result):
            d = self.host.memory.setParam(C.PROFILE_PASS_PATH[1], password, C.PROFILE_PASS_PATH[0], profile_key=profile)
            d.addCallback(lambda dummy: self.host.memory.setParam("Password", password, "Connection", profile_key=profile))
            confirm_ui = xml_tools.XMLUI("popup", title=D_("Confirmation"))
            confirm_ui.addText(D_("Your password has been changed."))
            return defer.succeed({'xmlui': confirm_ui.toXml()})

        def errback(failure):
            error_ui = xml_tools.XMLUI("popup", title=D_("Error"))
            error_ui.addText(D_("Your password could not be changed: %s") % failure.getErrorMessage())
            return defer.succeed({'xmlui': error_ui.toXml()})

        d = ProsodyRegisterProtocol.prosodyctl(self, 'passwd', password, profile=profile)
        d.addCallbacks(passwordChanged, errback)
        return d

    def __deleteAccount(self, profile):
        """Ask for a confirmation before deleting the XMPP account and SàT profile
        @param profile
        """
        form_ui = xml_tools.XMLUI("form", title=D_("Delete your account?"), submit_id=self.__delete_account_id)
        form_ui.addText(D_("If you confirm this dialog, you will be disconnected and then your XMPP account AND your SàT profile will both be DELETED."))
        target = D_('contact list, messages history, blog posts and comments' if 'GROUPBLOG' in self.host.plugins else D_('contact list and messages history'))
        form_ui.addText(D_("All your data stored on %(server)s, including your %(target)s will be erased.") % {'server': self.getNewAccountDomain(), 'target': target})
        form_ui.addText(D_("There is no other confirmation dialog, this is the very last one! Are you sure?"))
        return {'xmlui': form_ui.toXml()}

    def __deleteAccountCb(self, data, profile):
        """Actually delete the XMPP account and SàT profile
        @param data
        @param profile
        """
        def userDeleted(result):
            client = self.host.profiles[profile]

            for jid_ in client.roster._jids:  # empty roster
                client.presence.unsubscribe(jid_)

            for jid_ in self.host.memory.getWaitingSub(profile):  # delete waiting subscriptions
                self.host.memory.delWaitingSub(jid_)

            delete_profile = lambda: self.host.memory.asyncDeleteProfile(profile, force=True)
            if 'GROUPBLOG' in self.host.plugins:
                d = self.host.plugins['GROUPBLOG'].deleteAllGroupBlogsAndComments(profile_key=profile)
                d.addCallback(lambda dummy: delete_profile())
            else:
                delete_profile()

            return defer.succeed({})

        def errback(failure):
            error_ui = xml_tools.XMLUI("popup", title=D_("Error"))
            error_ui.addText(D_("Your XMPP account could not be deleted: %s") % failure.getErrorMessage())
            return defer.succeed({'xmlui': error_ui.toXml()})

        d = ProsodyRegisterProtocol.prosodyctl(self, 'deluser', profile=profile)
        d.addCallbacks(userDeleted, errback)
        return d

    def __deleteBlogPosts(self, posts, comments, profile):
        """Ask for a confirmation before deleting the blog posts
        @param posts: delete all posts of the user (and their comments)
        @param comments: delete all the comments of the user on other's posts
        @param data
        @param profile
        """
        if posts:
            if comments:  # delete everything
                form_ui = xml_tools.XMLUI("form", title=D_("Delete all your (micro-)blog posts and comments?"), submit_id=self.__delete_posts_comments_id)
                form_ui.addText(D_("If you confirm this dialog, all the (micro-)blog data you submitted will be erased."))
                form_ui.addText(D_("These are the public and private posts and comments you sent to any group."))
                form_ui.addText(D_("There is no other confirmation dialog, this is the very last one! Are you sure?"))
            else:  # delete only the posts
                form_ui = xml_tools.XMLUI("form", title=D_("Delete all your (micro-)blog posts?"), submit_id=self.__delete_posts_id)
                form_ui.addText(D_("If you confirm this dialog, all the public and private posts you sent to any group will be erased."))
                form_ui.addText(D_("There is no other confirmation dialog, this is the very last one! Are you sure?"))
        elif comments:  # delete only the comments
            form_ui = xml_tools.XMLUI("form", title=D_("Delete all your (micro-)blog comments?"), submit_id=self.__delete_comments_id)
            form_ui.addText(D_("If you confirm this dialog, all the public and private comments you made on other people's posts will be erased."))
            form_ui.addText(D_("There is no other confirmation dialog, this is the very last one! Are you sure?"))

        return {'xmlui': form_ui.toXml()}

    def __deleteBlogPostsCb(self, posts, comments, data, profile):
        """Actually delete the XMPP account and SàT profile
        @param posts: delete all posts of the user (and their comments)
        @param comments: delete all the comments of the user on other's posts
        @param profile
        """
        if posts:
            if comments:
                target = D_('blog posts and comments')
                d = self.host.plugins['GROUPBLOG'].deleteAllGroupBlogsAndComments(profile_key=profile)
            else:
                target = D_('blog posts')
                d = self.host.plugins['GROUPBLOG'].deleteAllGroupBlogs(profile_key=profile)
        elif comments:
            target = D_('comments')
            d = self.host.plugins['GROUPBLOG'].deleteAllGroupBlogsComments(profile_key=profile)

        def deleted(result):
            ui = xml_tools.XMLUI("popup", title=D_("Deletion confirmation"))
            # TODO: change the message when delete/retract notifications are done with XEP-0060
            ui.addText(D_("Your %(target)s have been deleted.") % {'target': target})
            ui.addText(D_("Known issue of the demo version: you need to refresh the page to make the deleted posts actually disappear."))
            return defer.succeed({'xmlui': ui.toXml()})

        def errback(failure):
            error_ui = xml_tools.XMLUI("popup", title=D_("Error"))
            error_ui.addText(D_("Your %(target)s could not be deleted: %(message)s") % {'target': target, 'message': failure.getErrorMessage()})
            return defer.succeed({'xmlui': error_ui.toXml()})

        d.addCallbacks(deleted, errback)
        return d

    def asyncConnectWithXMPPCredentials(self, jid_s, password):
        """Create and connect a new SàT profile using the given XMPP credentials.

        Re-use given JID and XMPP password for the profile name and profile password.
        @param jid_s (unicode): JID
        @param password (unicode): XMPP password
        @return Deferred(bool)
        @raise exceptions.PasswordError, exceptions.ConflictError
        """
        try:  # be sure that the profile doesn't exist yet
            self.host.memory.getProfileName(jid_s)
        except exceptions.ProfileUnknownError:
            pass
        else:
            raise exceptions.ConflictError

        d = self.createProfile(password, jid_s, jid_s)
        d.addCallback(lambda dummy: self.host.memory.getProfileName(jid_s))  # checks if the profile has been successfuly created
        d.addCallback(self.host.asyncConnect, password, 0)


        def connected(result):
            self.sendEmails(None, profile=jid_s)
            return result

        def removeProfile(failure):  # profile has been successfully created but the XMPP credentials are wrong!
            log.debug("Removing previously auto-created profile: %s" % failure.getErrorMessage())
            self.host.memory.asyncDeleteProfile(jid_s)
            raise failure

        # FIXME: we don't catch the case where the JID host is not an XMPP server, and the user
        # has to wait until the DBUS timeout ; as a consequence, emails are sent to the admins
        # and the profile is not deleted. When the host exists, removeProfile is well called.
        d.addCallbacks(connected, removeProfile)
        return d
