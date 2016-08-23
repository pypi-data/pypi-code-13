#!/usr/bin/env python
# coding: utf-8

import copy

try:
    import simplejson as json
except ImportError:
    import json

import requests
import six

from six.moves.urllib import parse



class OpsviewClientException(Exception):

    def __init__(self, message, response=None):
        message = message + response if response else message

        super(OpsviewClientException, self).__init__(message)

        self.response = response


class Contact(Resource):

    def __repr__(self):
        return '<Contact: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class ContactManager(Manager):

    resource_class = Contact

    def get(self, contact):
        return self._get('/config/contact/%s' % get_id(contact))

    def delete(self, contact):
        return self._delete('/config/contact/%s' % get_id(contact))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/contact%s' % qstring)


class Host(Resource):

    def __repr__(self):
        return '<Host: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)

    def update(self, **kwds):
        return self.manager.update(self, **kwds)


class HostManager(Manager):

    resource_class = Host

    def get(self, host):
        return self._get('/config/host/%s' % get_id(host))

    def delete(self, host):
        return self._delete('/config/host/%s' % get_id(host))

    def list(self, rows='all', page=None, cols=None, order=None,
             search=None, in_use=None, is_parent=None, include_ms=None,
             include_encrypted=None, monitored_by_id=None, template_id=None,
             template_name=None, bsm_component_id=None, with_snmpifs=False,
             kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0
        if is_parent is not None:
            qparams['is_parent'] = 1 if is_parent else 0
        if include_ms is not None:
            qparams['include_ms'] = 1 if include_ms else 0
        if include_encrypted is not None:
            qparams['include_encrypted'] = 1 if include_encrypted else 0
        if monitored_by_id:
            qparams['s.monitored_by.id'] = int(monitored_by_id)
        if template_id:
            qparams['s.hosttemplates.id'] = int(template_id)
        if template_name:
            qparams['s.hosttemplates.name'] = str(template_name)
        if bsm_component_id:
            qparams['s.business_components.id'] = int(bsm_component_id)
        if with_snmpifs:
            if 'cols' in qparams:
                qparams['cols'] += ',+snmpinterfaces'
            else:
                qparams['cols'] = '+snmpinterfaces'

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/host%s' % qstring)

    def update(self, host, **kwds):
        body = host._info
        body.update(kwds)
        return self._update('/config/host/%s' % get_id(host), body=body)

    def create(self, name, address, alias=None, check_attempts=None,
               check_command=None, check_interval=None, check_period=None,
               enable_snmp=None, event_handler_always_exec=None,
               event_handler=None, flap_detection_enabled=None,
               hostattributes=None, hostgroup=None, hosttemplates=None,
               icon=None, keywords=None, monitored_by=None,
               notification_interval=None, notification_options=None,
               notification_period=None, other_addresses=None, parents=None,
               rancid_autoenable=None, rancid_connection_type=None,
               rancid_username=None, rancid_vendor=None,
               retry_check_interval=None, servicechecks=None,
               snmp_extended_throughput_data=None, snmp_max_msg_size=None,
               snmp_port=None, snmp_version=None, snmpv3_authprotocol=None,
               snmpv3_privprotocol=None, snmpv3_username=None,
               tidy_ifdescr_level=None, use_rancid=None):

        req = {
            'name': name,
            'ip': address,
        }

        if alias is not None:
            req['alias'] = alias

        if check_attempts is not None:
            req['check_attempts'] = fmt_str(check_attempts)

        if check_command is not None:
            req['check_command'] = nameref(check_command)

        if check_interval is not None:
            req['check_interval'] = fmt_str(check_interval)

        if check_period is not None:
            req['check_period'] = nameref(check_period)

        if enable_snmp is not None:
            req['enable_snmp'] = fmt_str(enable_snmp)

        if event_handler is not None:
            req['event_handler'] = event_handler

        if event_handler_always_exec is not None:
            req['event_handler_always_exec'] = \
                fmt_str(event_handler_always_exec)

        if flap_detection_enabled is not None:
            req['flap_detection_enabled'] = fmt_str(flap_detection_enabled)

        if hostattributes is not None:
            if not isinstance(hostattributes, list):
                hostattributes = [hostattributes]

            req['hostattributes'] = hostattributes

        if hostgroup is not None:
            req['hostgroup'] = nameref(hostgroup)

        if hosttemplates is not None:
            if not isinstance(hosttemplates, list):
                hosttemplates = [hosttemplates]

            req['hosttemplates'] = []
            for template in hosttemplates:
                req['hosttemplates'].append(nameref(template))

        if icon is not None:
            if isinstance(icon, str):
                key = 'path' if icon[0] == '/' else 'name'

                req['icon'] = {key: icon}
            else:
                req['icon'] = icon

        if keywords is not None:
            if not isinstance(keywords, list):
                keywords = [keywords]

            req['keywords'] = []
            for keyword in keywords:
                req['keywords'].append(nameref(keyword))

        if monitored_by is not None:
            req['monitored_by'] = nameref(monitored_by)

        if notification_interval is not None:
            req['notification_interval'] = fmt_str(notification_interval)

        if notification_options is not None:
            req['notification_interval'] = notification_options

        if notification_period is not None:
            req['notification_period'] = nameref(notification_period)

        if other_addresses is not None:
            if isinstance(other_addresses, list):
                other_addresses = ','.join(other_addresses)

            req['other_addresses'] = other_addresses

        if parents is not None:
            if not isinstance(parents, list):
                parents = [parents]

            req['parents'] = []
            for parent in parents:
                req['parents'].append(nameref(parent))

        if rancid_autoenable is not None:
            req['rancid_autoenable'] = fmt_str(rancid_autoenable)

        if rancid_connection_type is not None:
            req['rancid_connection_type'] = rancid_connection_type

        if rancid_username is not None:
            req['rancid_username'] = rancid_username

        if rancid_vendor is not None:
            req['rancid_vendor'] = rancid_vendor

        if retry_check_interval is not None:
            req['retry_check_interval'] = fmt_str(retry_check_interval)

        if servicechecks is not None:
            if not isinstance(servicechecks, list):
                servicechecks = [servicechecks]

            req['servicechecks'] = []
            for check in servicechecks:
                if isinstance(check, str):
                    req['servicechecks'].append(nameref(check))
                else:
                    req['servicechecks'].append(check)

        if snmp_extended_throughput_data is not None:
            req['snmp_extended_throughput_data'] = \
                fmt_str(snmp_extended_throughput_data)

        if snmp_max_msg_size is not None:
            req['snmp_max_msg_size'] = fmt_str(snmp_max_msg_size)

        if snmp_port is not None:
            req['snmp_port'] = fmt_str(snmp_port)

        if snmp_version is not None:
            req['snmp_version'] = fmt_str(snmp_version)

        if snmpv3_authprotocol is not None:
            req['snmpv3_authprotocol'] = snmpv3_authprotocol

        if snmpv3_privprotocol is not None:
            req['snmpv3_privprotocol'] = snmpv3_privprotocol

        if snmpv3_username is not None:
            req['snmpv3_username'] = snmpv3_username

        if tidy_ifdescr_level is not None:
            req['tidy_ifdescr_level'] = fmt_str(tidy_ifdescr_level)

        if use_rancid is not None:
            req['use_rancid'] = fmt_str(use_rancid)

        return self._create('/config/host', body=req)


class Role(Resource):

    def __repr__(self):
        return '<Role: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class RoleManager(Manager):

    resource_class = Role

    def get(self, role):
        return self._get('/config/role/%s' % get_id(role))

    def delete(self, role):
        return self._delete('/config/role/%s' % get_id(role))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/role%s' % qstring)


class ServiceCheck(Resource):

    def __repr__(self):
        return '<ServiceCheck: %s>' % self.name

    def update(self, **kwds):
        return self.manager.update(self, **kwds)

    def delete(self):
        return self.manager.delete(self)


class ServiceCheckManager(Manager):

    resource_class = ServiceCheck

    def get(self, check):
        return self._get('/config/servicecheck/%s' % get_id(check))

    def delete(self, check):
        return self._delete('/config/servicecheck/%s' % get_id(check))

    def update(self, check, **kwds):
        body = check._info
        body.update(kwds)
        return self._update('/config/servicecheck/%s' % get_id(check))

    def create(self, name, plugin, alert_from_failure=None, args=None,
               attribute=None, calculated_rate=None, cascaded_from=None,
               check_attempts=None, check_freshness=None, check_interval=None,
               check_period=None, checktype=None, critical_comparison=None,
               critical_value=None, dependencies=None, description=None,
               event_handler=None, event_handler_always_exec=None,
               flap_detection_enabled=None, freshness_type=None, hosts=None,
               hosttemplates=None, invertresults=None, keywords=None,
               label=None, markdown_filter=None, notification_interval=None,
               notification_options=None, notification_period=None, oid=None,
               retry_check_interval=None, sensitive_arguments=None,
               servicegroup=None, snmptraprules=None, stale_state=None,
               stale_text=None, stale_threshold_seconds=None, stalking=None,
               volatile=None, warning_comparison=None, warning_value=None):

        body = {
            'name': name,
            'plugin': nameref(plugin)
        }

        if alert_from_failure is not None:
            body['alert_from_failure'] = fmt_str(alert_from_failure)

        if args is not None:
            body['args'] = args

        if attribute is not None:
            body['attribute'] = nameref(attribute)

        if calculated_rate is not None:
            body['calculated_rate'] = calculated_rate

        if cascaded_from is not None:
            body['cascaded_from'] = nameref(cascaded_from)

        if check_attempts is not None:
            body['check_attempts'] = fmt_str(check_attempts)

        if check_freshness is not None:
            body['check_freshness'] = fmt_str(check_freshness)

        if check_interval is not None:
            body['check_interval'] = fmt_str(check_interval)

        if check_period is not None:
            body['check_period'] = nameref(check_period)

        if checktype is not None:
            body['checktype'] = nameref(checktype)

        # TODO:handle these
        if critical_comparison is not None:
            body['critical_comparison'] = critical_comparison
        if critical_value is not None:
            body['critical_value'] = critical_value

        if dependencies is not None:
            if not isinstance(dependencies, list):
                dependencies = [dependencies]

            body['dependencies'] = [nameref(d) for d in dependencies]

        if description is not None:
            body['description'] = description

        if event_handler is not None:
            body['event_handler'] = event_handler

        if event_handler_always_exec is not None:
            body['event_handler_always_exec'] = \
                fmt_str(event_handler_always_exec)

        if flap_detection_enabled is not None:
            body['flap_detection_enabled'] = fmt_str(flap_detection_enabled)

        if freshness_type is not None:
            body['freshness_type'] = freshness_type

        if hosts is not None:
            if not isinstance(hosts, list):
                hosts = [hosts]

            body['hosts'] = [nameref(h) for h in hosts]

        if hosttemplates is not None:
            if not isinstance(hosttemplates, list):
                hosttemplates = [hosttemplates]

            body['hosttemplates'] = [nameref(h) for h in hosttemplates]

        if invertresults is not None:
            body['invertresults'] = fmt_str(invertresults)

        if keywords is not None:
            if not isinstance(keywords, list):
                keywords = [keywords]

            body['keywords'] = [nameref(k) for k in keywords]

        # TODO:handle this
        if label is not None:
            body['label'] = label

        if markdown_filter is not None:
            body['markdown_filter'] = fmt_str(markdown_filter)

        if notification_interval is not None:
            body['notification_interval'] = fmt_str(notification_interval)

        if notification_options is not None:
            body['notification_options'] = notification_options

        if notification_period is not None:
            body['notification_period'] = nameref(notification_period)

        # TODO:handle this
        if oid is not None:
            body['oid'] = oid

        if retry_check_interval is not None:
            body['retry_check_interval'] = fmt_str(retry_check_interval)

        if sensitive_arguments is not None:
            body['sensitive_arguments'] = fmt_str(sensitive_arguments)

        if servicegroup is not None:
            body['servicegroup'] = nameref(servicegroup)

        # TODO:handle this
        if snmptraprules is not None:
            body['snmptraprules'] = [nameref(s) for s in snmptraprules]

        if stale_state is not None:
            body['stale_state'] = fmt_str(stale_state)

        if stale_text is not None:
            body['stale_text'] = stale_text

        if stale_threshold_seconds is not None:
            body['stale_threshold_seconds'] = fmt_str(stale_threshold_seconds)

        if stalking is not None:
            body['stalking'] = fmt_str(stalking)

        if volatile is not None:
            body['volatile'] = fmt_str(volatile)

        # TODO:handle this
        if warning_comparison is not None:
            body['warning_comparison'] = warning_comparison
        if warning_value is not None:
            body['warning_value'] = warning_value

        return self._create('/config/servicecheck', body=body)

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/servicecheck%s' % qstring)


class HostTemplate(Resource):

    def __repr__(self):
        return '<HostTemplate: %s>' % self.name

    def update(self, **kwds):
        return self.manager.update(self, **kwds)

    def delete(self):
        return self.manager.delete(self)


class HostTemplateManager(Manager):

    resource_class = HostTemplate

    def get(self, template):
        return self._get('/config/hosttemplate/%s' % get_id(template))

    def create(self, name, description=None, hosts=None, managementurls=None,
               servicechecks=None):

        body = {'name': name}

        if description is not None:
            body['description'] = description

        if hosts is not None:
            if not isinstance(hosts, list):
                hosts = [hosts]

            body['hosts'] = []
            for host in hosts:
                body['hosts'].append(nameref(host))

        if managementurls is not None:
            if not isinstance(managementurls, list):
                managementurls = [managementurls]

            body['managementurls'] = []
            for url in managementurls:
                body['managementurls'].append(nameref(url))

        if servicechecks is not None:
            if not isinstance(servicechecks, list):
                servicechecks = [servicechecks]

            body['servicechecks'] = []
            for check in servicechecks:
                body['servicechecks'].append(nameref(check))

        return self._create('/config/hosttemplate', body=body)

    def update(self, template, **kwds):
        body = template._info
        body.update(kwds)
        self._update('/config/hosttemplate/%s' % get_id(template), body=body)

    def delete(self, template):
        return self._delete('/config/hosttemplate/%s' % get_id(template))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/hosttemplate%s' % qstring)


class HostGroup(Resource):

    def __repr__(self):
        return '<HostGroup: %s>' % self.name

    def update(self, **kwds):
        return self.manager.update(self, **kwds)

    def delete(self):
        return self.manager.delete(self)


class HostGroupManager(Manager):

    resource_class = HostGroup

    def get(self, group):
        return self._get('/config/hostgroup/%s' % get_id(group))

    def delete(self, group):
        return self._delete('/config/hostgroup/%s' % get_id(group))

    def update(self, group, **kwds):
        body = group._info
        body.update(kwds)
        return self._update('/config/hostgroup/%s' % get_id(group), body=body)

    def create(self, name, children=None, hosts=None, parent=None):
        body = {'name': name}

        if children is not None:
            if not isinstance(children, list):
                children = [children]

            body['children'] = [nameref(c) for c in children]

        if hosts is not None:
            if not isinstance(hosts, list):
                hosts = [hosts]

            body['hosts'] = [nameref(h) for h in hosts]

        if parent is not None:
            body['parent'] = nameref(parent)

        return self._create('/config/hostgroup', body=body)

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/hostgroup%s' % qstring)


class ServiceGroup(Resource):

    def __repr__(self):
        return '<ServiceGroup: %s>' % self.name

    def update(self, **kwds):
        return self.manager.update(self, **kwds)

    def delete(self):
        return self.manager.delete(self)


class ServiceGroupManager(Manager):

    resource_class = ServiceGroup

    def get(self, group):
        return self._get('/config/servicegroup/%s' % get_id(group))

    def update(self, group, **kwds):
        body = group._info
        body.update(kwds)
        return self._update('/config/servicegroup/%s' % get_id(group),
                            body=body)

    def create(self, name, servicechecks=None):
        body = {'name': name}

        if servicechecks is not None:
            if not isinstance(servicechecks, list):
                servicechecks = [servicechecks]

            body['servicechecks'] = [nameref(s) for s in servicechecks]

        return self._create('/config/servicegroup', body=body)

    def delete(self, group):
        return self._delete('/config/servicegroup/%s' % get_id(group))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/servicegroup%s' % qstring)


class Keyword(Resource):

    def __repr__(self):
        return '<Keyword: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class KeywordManager(Manager):

    resource_class = Keyword

    def get(self, keyword):
        return self._get('/config/keyword/%s' % get_id(keyword))

    def delete(self, keyword):
        return self._delete('/config/keyword/%s' % get_id(keyword))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/keyword%s' % qstring)


class MonitoringServer(Resource):

    def __repr__(self):
        return '<MonitoringServer: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)

    def update(self, **kwds):
        return self.manager.update(self, **kwds)


class MonitoringServerManager(Manager):

    resource_class = MonitoringServer

    def get(self, server):
        return self._get('/config/monitoringserver/%s' % get_id(server))

    def delete(self, server):
        return self._delete('/config/monitoringserver/%s' % get_id(server))

    def update(self, server, **kwds):
        body = server._info
        body.update(kwds)

        # Fix issue where the API returns nodes wrapped with '{"host": }' but
        # won't accept these for PUT and POST requests
        nodes = body.get('nodes')
        if nodes and any([n for n in nodes if 'host' in n]):
            # Manually added nodes
            ok_nodes = [n for n in nodes if 'host' not in n]
            # Nodes existing from API returning crap
            ok_nodes += [n['host'] for n in nodes if 'host' in n]

            body['nodes'] = ok_nodes

        return self._update('/config/monitoringserver/%s' % get_id(server),
                            body=body)

    def create(self, name, active=None, nodes=None, passive=None,
               ssh_forward=None):

        body = {'name': name}

        if active is not None:
            body['activated'] = fmt_str(active)

        if nodes is not None:
            if not isinstance(nodes, list):
                nodes = [nodes]

            body['nodes'] = [nameref(n) for n in nodes]

        if passive is not None:
            body['passive'] = fmt_str(passive)

        if ssh_forward is not None:
            body['ssh_forward'] = fmt_str(ssh_forward)

        return self._create('/config/monitoringserver', body=body)

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/monitoringserver%s' % qstring)


class Tenancy(Resource):

    def __repr__(self):
        return '<Tenancy: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class TenancyManager(Manager):

    resource_class = Tenancy

    def get(self, tenancy):
        return self._get('/config/tenancy/%s' % get_id(tenancy))

    def delete(self, tenancy):
        return self._delete('/config/tenancy/%s' % get_id(tenancy))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/tenancy%s' % qstring)


class TimePeriod(Resource):

    def __repr__(self):
        return '<TimePeriod: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class TimePeriodManager(Manager):

    resource_class = TimePeriod

    def get(self, time_period):
        return self._get('/config/timeperiod/%s' % get_id(time_period))

    def delete(self, time_period):
        return self._delete('/config/timeperiod/%s' % get_id(time_period))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/timeperiod%s' % qstring)


class HostCheckCommand(Resource):

    def __repr__(self):
        return '<HostCheckCommand: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class HostCheckCommandManager(Manager):

    resource_class = HostCheckCommand

    def get(self, command):
        return self._get('/config/hostcheckcommand/%s' % get_id(command))

    def delete(self, command):
        return self._delete('/config/hostcheckcommand/%s' % get_id(command))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/hostcheckcommand%s' % qstring)


class NetflowCollector(Resource):

    def __repr__(self):
        return '<NetflowCollector: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class NetflowCollectorManager(Manager):

    resource_class = NetflowCollector

    def get(self, collector):
        return self._get('/config/netflowcollector/%s' % get_id(collector))

    def delete(self, collector):
        return self._delete('/config/netflowcollector/%s' % get_id(collector))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/netflowcollector%s' % qstring)


class NetflowSource(Resource):

    def __repr__(self):
        return '<NetflowSource: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class NetflowSourceManager(Manager):

    resource_class = NetflowSource

    def get(self, source):
        return self._get('/config/netflowsource/%s' % get_id(source))

    def delete(self, source):
        return self._delete('/config/netflowsource/%s' % get_id(source))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/netflowsource%s' % qstring)


class Attribute(Resource):

    def __repr__(self):
        return '<Attribute: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class AttributeManager(Manager):

    resource_class = Attribute

    def get(self, attribute):
        return self._get('/config/attribute/%s' % get_id(attribute))

    def delete(self, attribute):
        return self._delete('/config/attribute/%s' % get_id(profile))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/attribute%s' % qstring)


class SharedNotificationProfile(Resource):

    def __repr__(self):
        return '<SharedNotificationProfile: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class SharedNotificationProfileManager(Manager):

    resource_class = SharedNotificationProfile

    def get(self, profile):
        return self._get('/config/sharednotificationprofile/%s' %
                         get_id(profile))

    def delete(self, profile):
        return self._delete('/config/sharednotificationprofile/%s' %
                            get_id(profile))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/sharednotificationprofile%s' % qstring)


class NotificationMethod(Resource):

    def __repr__(self):
        return '<NotificationMethod: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class NotificationMethodManager(Manager):

    resource_class = NotificationMethod

    def get(self, method):
        return self._get('/config/notificationmethod/%s' % get_id(method))

    def delete(self, method):
        return self._delete('/config/notificationmethod/%s' % get_id(method))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/notificationmethod%s' % qstring)


class OpsviewClient(object):

    _default_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    def __init__(self, username, password, endpoint):

        if endpoint[-1] == '/':
            self.base_url = endpoint
        else:
            self.base_url = endpoint + '/'

        self._username = username
        self._password = password

        self._auth_failed = False

        self._session = requests.Session()
        self._session.headers = OpsviewClient._default_headers

        self.contacts = ContactManager(self)
        self.hosts = HostManager(self)
        self.roles = RoleManager(self)
        self.service_checks = ServiceCheckManager(self)
        self.host_templates = HostTemplateManager(self)
        self.attributes = AttributeManager(self)
        self.time_periods = TimePeriodManager(self)
        self.host_groups = HostGroupManager(self)
        self.service_groups = ServiceGroupManager(self)
        self.notification_methods = NotificationMethodManager(self)
        self.host_check_commands = HostCheckCommandManager(self)
        self.keywords = KeywordManager(self)
        self.shared_notification_profiles = \
            SharedNotificationProfileManager(self)

        self.monitoring_servers = MonitoringServerManager(self)
        self.netflow_collectors = NetflowCollectorManager(self)
        self.netflow_sources = NetflowSourceManager(self)
        self.tenancies = TenancyManager(self)

        self._authenticate()

    def _authenticate(self):
        # Clear the authenticated headers
        self._session.headers.pop('X-Opsview-Username', None)
        self._session.headers.pop('X-Opsview-Token', None)

        payload = {
            'username': self._username,
            'password': self._password,
        }

        response = self._request('POST', 'login', data=payload)

        try:
            token = response['token']
        except Exception as e:
            raise e

        self._session.headers['X-Opsview-Username'] = self._username
        self._session.headers['X-Opsview-Token'] = token

    def _url(self, path):
        if path[0] == '/':
            path = path[1:]

        return self.base_url + path

    def _request(self, method, path, data=None, params=None, expected=[200]):

        response = self._session.request(method=method, url=self._url(path),
                                         data=json.dumps(data), params=params)

        if response.status_code not in expected:
            raise OpsviewClientException('Unexpected response: ', response.text)

        return response.json()

    def reload(self):
        status = self.post('/reload')
        return status

    def get(self, url, **kwds):
        return self._request('GET', url, **kwds)

    def post(self, url, **kwds):
        return self._request('POST', url, **kwds)

    def put(self, url, **kwds):
        return self._request('PUT', url, **kwds)

    def delete(self, url, **kwds):
        return self._request('DELETE', url, **kwds)


def main():
    argspec = {
        'username': {'required': True},
        'password': {'required': True},
        'endpoint': {'required': True},

        'host': {'type': 'dict'},
        'monitoringserver': {'type': 'dict'},
        'servicecheck': {'type': 'dict'},
        'hosttemplate': {'type': 'dict'},
        'hostgroup': {'type': 'dict'},

        'state': {'choices': ['present', 'absent', 'reloaded'],
                  'default': 'present'},

        'name': {'required': True},
        'address': {'required': True},
        'alias': {'type': 'str'},
        'check_attempts': {'type': 'int'},
        'check_command': {'type': 'str'},
        'check_interval': {'type': 'str'},
        'check_period': {'type': 'str'},
        'enable_snmp': {'type': 'bool'},
        'event_handler_always_exec': {'type': 'bool'},
        'event_handler': {'type': 'str'},
        'flap_detection_enabled': {'type': 'bool'},
        'hostattributes': {'type': 'list'},
        'hostgroup': {'type': 'str'},
        'hosttemplates': {'type': 'list'},
        'icon': {'type': 'dict'},
        'keywords': {'type': 'list'},
        'monitored_by': {'type': 'str'},
        'notification_interval': {'type': 'str'},
        'notification_options': {'type': 'str'},
        'notification_period': {'type': 'str'},
        'other_addresses': {'type': 'list'},
        'parents': {'type': 'list'},
        'rancid_autoenable': {'type': 'bool'},
        'rancid_connection_type': {'type': 'str'},
        'rancid_username': {'type': 'str'},
        'rancid_vendor': {'type': 'str'},
        'retry_check_interval': {'type': 'str'},
        'servicechecks': {'type': 'list'},
        'snmp_extended_throughput_data': {'type': 'bool'},
        'snmp_max_msg_size': {'type': 'str'},
        'snmp_port': {'type': 'int'},
        'snmp_version': {'choices': ['1', '2c', '3']},
        'snmpv3_authprotocol': {'choices': ['md5', 'sha']},
        'snmpv3_privprotocol': {'choices': ['des', 'aes', 'aes128']},
        'snmpv3_username': {'type': 'str'},
        'tidy_ifdescr_level': {'type': 'str'},
        'use_rancid': {'type': 'bool'},
        # ADD PWS
    }

    module = AnsibleModule(
        argument_spec=argspec,
        required_one_of=[]
        supports_check_mode=True)
    params = module.params

    client = OpsviewClient(username=params['username'],
                           password=params['password'],
                           endpoint=params['endpoint'])

    changed = False

    # This call should only ever return 1 or 0 hosts as the name must be a
    # unique identifier for Opsview hosts
    host_list = client.hosts.list(search={'name': params['name']})
    host = (host_list[0] if host_list else None)

    if host is None and module.check_mode:
        module.exit_json(msg="%s: %s" % (params['name'], params['address']),
                         changed=True)

    # These params should almost match the params expected by hosts.create()
    # so we can save rewriting all the params in the function calls
    host_params = copy.deepcopy(params)
    del host_params['username']
    del host_params['password']
    del host_params['endpoint']
    del host_params['state']

    if host is None:
        host = client.hosts.create(**host_params)
        changed = True

    module.exit_json(msg='%s: %s' % (host.name, host.ip),
                     host=host._info, changed=changed)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
