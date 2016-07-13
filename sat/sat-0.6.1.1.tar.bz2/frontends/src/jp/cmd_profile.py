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

"""This module permits to manage profiles. It can list, create, delete
and retrieve information about a profile."""

import logging as log
from sat.core.i18n import _
from sat_frontends.jp import base

__commands__ = ["Profile"]

PROFILE_HELP = _('The name of the profile')


class ProfileConnect(base.CommandBase):
    """Dummy command to use profile_session parent, i.e. to be able to connect without doing anything else"""

    def __init__(self, host):
        # it's weird to have a command named "connect" with need_connect=False, but it can be handy to be able
        # to launch just the session, so some paradox don't hurt
        super(ProfileConnect, self).__init__(host, 'connect', need_connect=False, help=_('connect a profile'))

    def add_parser_options(self):
        pass


class ProfileDefault(base.CommandBase):
    def __init__(self, host):
        super(ProfileDefault, self).__init__(host, 'default', use_profile=False, help=_('print default profile'))

    def add_parser_options(self):
        pass

    def start(self):
        print self.host.bridge.getProfileName('@DEFAULT@')


class ProfileDelete(base.CommandBase):
    def __init__(self, host):
        super(ProfileDelete, self).__init__(host, 'delete', use_profile=False, help=_('delete a profile'))

    def add_parser_options(self):
        self.parser.add_argument('profile', type=str, help=PROFILE_HELP)
        self.parser.add_argument('-f', '--force', action='store_true', help=_(u'delete profile without confirmation'))

    def start(self):
        if self.args.profile not in self.host.bridge.getProfilesList():
            log.error("Profile %s doesn't exist." % self.args.profile)
            self.host.quit(1)
        message = u"Are you sure to delete profile [{}] ?".format(self.args.profile)
        if not self.args.force:
            res = raw_input("{} (y/N)? ".format(message))
            if res not in ("y", "Y"):
                self.disp(_(u"Profile deletion cancelled"))
                self.host.quit(2)

        self.host.bridge.asyncDeleteProfile(self.args.profile, callback=lambda dummy: None)


class ProfileInfo(base.CommandBase):
    def __init__(self, host):
        super(ProfileInfo, self).__init__(host, 'info', need_connect=False, help=_('get information about a profile'))
        self.need_loop = True
        self.to_show = [(_(u"jid"), "Connection", "JabberID"),]
        self.largest = max([len(item[0]) for item in self.to_show])


    def add_parser_options(self):
        self.parser.add_argument('--show-password', action='store_true', help=_(u'show the XMPP password IN CLEAR TEXT'))

    def showNextValue(self, label=None, category=None, value=None):
        """Show next value from self.to_show and quit on last one"""
        if label is not None:
            print((u"{label:<"+unicode(self.largest+2)+"}{value}").format(label=label+": ", value=value))
        try:
            label, category, name = self.to_show.pop(0)
        except IndexError:
            self.host.quit()
        else:
            self.host.bridge.asyncGetParamA(name, category, profile_key=self.host.profile,
                                            callback=lambda value: self.showNextValue(label, category, value))

    def start(self):
        if self.args.show_password:
            self.to_show.append((_(u"XMPP password"), "Connection", "Password"))
        self.showNextValue()


class ProfileList(base.CommandBase):
    def __init__(self, host):
        super(ProfileList, self).__init__(host, 'list', use_profile=False, use_output='list', help=_('list profiles'))

    def add_parser_options(self):
        pass

    def start(self):
        self.output(self.host.bridge.getProfilesList())


class ProfileCreate(base.CommandBase):
    def __init__(self, host):
        super(ProfileCreate, self).__init__(host, 'create', use_profile=False, help=_('create a new profile'))
        self.need_loop = True

    def add_parser_options(self):
        self.parser.add_argument('profile', type=str, help=_('the name of the profile'))
        self.parser.add_argument('-p', '--password', type=str, default='', help=_('the password of the profile'))
        self.parser.add_argument('-j', '--jid', type=str, help=_('the jid of the profile'))
        self.parser.add_argument('-x', '--xmpp-password', type=str, help=_('the password of the XMPP account (use profile password if not specified)'),
                                 metavar='PASSWORD')

    def _session_started(self, dummy):
        if self.args.jid:
            self.host.bridge.setParam("JabberID", self.args.jid, "Connection" ,profile_key=self.args.profile)
        xmpp_pwd = self.args.password or self.args.xmpp_password
        if xmpp_pwd:
            self.host.bridge.setParam("Password", xmpp_pwd, "Connection", profile_key=self.args.profile)
        self.host.quit()

    def _profile_created(self):
        self.host.bridge.profileStartSession(self.args.password, self.args.profile, callback=self._session_started, errback=None)

    def start(self):
        """Create a new profile"""
        if self.args.profile in self.host.bridge.getProfilesList():
            log.error("Profile %s already exists." % self.args.profile)
            self.host.quit(1)
        self.host.bridge.asyncCreateProfile(self.args.profile, self.args.password, callback=self._profile_created, errback=None)


class ProfileModify(base.CommandBase):
    def __init__(self, host):
        super(ProfileModify, self).__init__(host, 'modify', need_connect=False, help=_('modify an existing profile'))

    def add_parser_options(self):
        profile_pwd_group = self.parser.add_mutually_exclusive_group()
        profile_pwd_group.add_argument('-w', '--password', type=base.unicode_decoder, help=_('change the password of the profile'))
        profile_pwd_group.add_argument('--disable-password', action='store_true', help=_('disable profile password (dangerous!)'))
        self.parser.add_argument('-j', '--jid', type=base.unicode_decoder, help=_('the jid of the profile'))
        self.parser.add_argument('-x', '--xmpp-password', type=base.unicode_decoder, help=_('change the password of the XMPP account'),
                                 metavar='PASSWORD')
        self.parser.add_argument('-D', '--default', action='store_true', help=_(u'set as default profile'))

    def start(self):
        if self.args.disable_password:
            self.args.password = ''
        if self.args.password is not None:
            self.host.bridge.setParam("Password", self.args.password, "General", profile_key=self.host.profile)
        if self.args.jid is not None:
            self.host.bridge.setParam("JabberID", self.args.jid, "Connection", profile_key=self.host.profile)
        if self.args.xmpp_password is not None:
            self.host.bridge.setParam("Password", self.args.xmpp_password, "Connection", profile_key=self.host.profile)
        if self.args.default:
            self.host.bridge.profileSetDefault(self.host.profile)


class Profile(base.CommandBase):
    subcommands = (ProfileConnect, ProfileCreate, ProfileDefault, ProfileDelete, ProfileInfo, ProfileList, ProfileModify)

    def __init__(self, host):
        super(Profile, self).__init__(host, 'profile', use_profile=False, help=_('Profile commands'))
