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

import base
from sat.core.i18n import _

__commands__ = ["Info"]


class Disco(base.CommandBase):

    def __init__(self, host):
        super(Disco, self).__init__(host, 'disco', help=_('Service discovery'))
        self.need_loop=True

    def add_parser_options(self):
        self.parser.add_argument("jid", type=str, help=_("Entity to discover"))

    def start(self):
        jids = self.host.check_jids([self.args.jid])
        jid = jids[0]
        self.host.bridge.discoInfos(jid, profile_key=self.host.profile, callback=lambda infos: self.gotInfos(infos, jid), errback=self.error)

    def error(self, failure):
        print (_("Error while doing discovery [%s]") % failure)
        self.host.quit(1)

    def gotInfos(self, infos, jid):
        self.host.bridge.discoItems(jid, profile_key=self.host.profile, callback=lambda items: self.gotItems(infos, items), errback=self.error)

    def gotItems(self, infos, items):
        features, identities, extensions = infos
        features.sort()
        identities.sort(key=lambda identity: identity[2])
        items.sort(key=lambda item: item[2])
        identities_lst = []
        items_lst = []
        for identity in identities:
            category, type_, name = identity
            identities_lst.append(u"{name}({cat}/{type_})".format(
                                 name = (name+' ') if name else '',
                                 cat = category,
                                 type_ = type_))
        for item in items:
            entity, node_id, name = item
            items_lst.append(u"{name}[{entity}{node_id}]".format(
                                 name = (name+' ') if name else '',
                                 entity = entity,
                                 node_id = (', ' + node_id) if node_id else ''
                                 ))
        extensions_types = extensions.keys()
        extensions_types.sort()

        extensions_tpl = []
        for type_ in extensions_types:
            fields = []
            for field in extensions[type_]:
                field_lines = []
                data, values = field
                data_keys = data.keys()
                data_keys.sort()
                for key in data_keys:
                    field_lines.append(u'\t{key} = {value}'.format(key=key, value=data[key]))
                for value in values:
                    field_lines.append(u'\tvalue = {value}'.format(value=value))
                fields.append(u'\n'.join(field_lines))
            extensions_tpl.append(u'{type_}\n{fields}'.format(type_=type_,
                                                              fields='\n\n'.join(fields)))

        template = []
        if features:
            template.append(_(u"Features:\n\n{features}"))
        if identities:
            template.append(_(u"Identities:\n\n{identities}"))
        if extensions_tpl:
            template.append(_(u'Extensions:\n\n{extensions}'))
        if items:
            template.append(_(u"Items:\n\n{items}"))

        print "\n--\n".join(template).format ( features = '\n'.join(features),
                                               identities = '\n'.join(identities_lst),
                                               extensions = '\n'.join(extensions_tpl),
                                               items = '\n'.join(items_lst),
                                             )
        self.host.quit()


class Version(base.CommandBase):

    def __init__(self, host):
        super(Version, self).__init__(host, 'version', help=_('Client version'))
        self.need_loop=True

    def add_parser_options(self):
        self.parser.add_argument("jid", type=str, help=_("Entity to request"))

    def start(self):
        jids = self.host.check_jids([self.args.jid])
        jid = jids[0]
        self.host.bridge.getSoftwareVersion(jid, self.host.profile, callback=self.gotVersion, errback=self.error)

    def error(self, failure):
        print (_("Error while trying to get version [%s]") % failure)
        self.host.quit(1)

    def gotVersion(self, data):
        infos = []
        name, version, os = data
        if name:
            infos.append(_("Client name: %s") %  name)
        if version:
            infos.append(_("Client version: %s") %  version)
        if os:
            infos.append(_("Operating System: %s") %  os)

        print "\n".join(infos)
        self.host.quit()


class Info(base.CommandBase):
    subcommands = (Disco, Version)

    def __init__(self, host):
        super(Info, self).__init__(host, 'info', use_profile=False, help=_('Get various pieces of information on entities'))
