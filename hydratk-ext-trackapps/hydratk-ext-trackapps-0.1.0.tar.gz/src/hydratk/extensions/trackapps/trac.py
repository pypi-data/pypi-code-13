# -*- coding: utf-8 -*-
"""Client for Trac

.. module:: trackapps.trac
   :platform: Unix
   :synopsis: Client for Trac
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
track_before_connect
track_after_connect
track_before_read
track_after_read
track_before_create
track_after_create
track_before_update
track_after_update
track_before_delete
track_after_delete

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from hydratk.lib.network.rest.client import RESTClient
from lxml.etree import Element, SubElement, tostring, XMLSyntaxError
from lxml import objectify
from sys import version_info

config = {
  'login'  : '/{0}/login',
  'rpc'    : '/{0}/login/xmlrpc'
}

rec_fields = {
  'id'             : 'int',
  'status'         : 'string',
  'changetime'     : 'dateTime.iso8601',
  'totalhours'     : 'string',
  '_ts'            : 'string',
  'description'    : 'string',
  'reporter'       : 'string',
  'cc'             : 'string',
  'resolution'     : 'string',
  'time'           : 'dateTime.iso8601',
  'component'      : 'string',
  'summary'        : 'string',
  'priority'       : 'string',
  'keywords'       : 'string',
  'version'        : 'string',
  'milestone'      : 'string',
  'owner'          : 'string',
  'estimatedhours' : 'string',
  'type'           : 'string' 
}

class Client(object):
    """Class Client
    """
    
    _mh = None
    _client = None
    _url = None
    _user = None
    _passw = None
    _domain = None
    _project = None
    _cookie = None
    _return_fields = None
    _default_values = {}
    _is_connected = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized   
        
        Args:
           none
                
        """  
        
        self._mh = MasterHead.get_head()
        self._client = RESTClient()  

        cfg = self._mh.cfg['Extensions']['TrackApps']['trac'] 
        if ('return_fields' in cfg and cfg['return_fields'] != None):
            self._return_fields = cfg['return_fields'].split(',') 
        if ('default_values' in cfg and cfg['default_values'] != None):
            self._default_values = cfg['default_values']  
        if ('url' in cfg and cfg['url'] != None):
            self._url = cfg['url']    
        if ('user' in cfg and cfg['user'] != None):
            self._user = cfg['user']   
        if ('passw' in cfg and cfg['passw'] != None):
            self._passw = cfg['passw']  
        if ('project' in cfg and cfg['project'] != None):
            self._project = cfg['project']              
        
    @property
    def client(self):
        """ client property getter """
        
        return self._client
    
    @property
    def url(self):
        """ url property getter """
        
        return self._url
    
    @property
    def user(self):
        """ user property getter """
        
        return self._user
    
    @property
    def passw(self):
        """ passw property getter """
        
        return self._passw
    
    @property
    def project(self):
        """ project property getter """
        
        return self._project
    
    @property
    def cookie(self):
        """ cookie property getter """
        
        return self._cookie        
    
    @property
    def return_fields(self):
        """ return_fields property getter """
        
        return self._return_fields   
    
    @property
    def default_values(self):
        """ default_values property getter """
        
        return self._default_values     
    
    @property
    def is_connected(self):
        """ is_connected property getter """
        
        return self._is_connected       
    
    def connect(self, url=None, user=None, passw=None, project=None):
        """Method connects to Trac
        
        Args:    
           url (str): URL        
           user (str): username
           passw (str): password
           project (str): project
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_connect
           event: track_after_connect
                
        """    
        
        message = 'url:{0}, user:{1}, passw:{2}, project:{3}'.format(url, user, passw, project)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_connecting', message), self._mh.fromhere()) 
        
        if (url == None):
            url = self._url
        if (user == None):
            user = self._user
        if (passw == None):
            passw = self._passw    
        if (project == None):
            project = self._project            
        
        ev = event.Event('track_before_connect', url, user, passw, project)
        if (self._mh.fire_event(ev) > 0):
            url = ev.argv(0)
            user = ev.argv(1)
            passw = ev.argv(2)
            project = ev.argv(3)
            
        if (ev.will_run_default()):
            self._url = url
            self._user = user
            self._passw = passw
            self._project = project  
            
            url = self._url + config['login'].format(self._project)
            res, body = self._client.send_request(url, self._user, self._passw, 'GET')
        
        result = False
        if (res == 200): 
              
            self._cookie = self._client.get_header('set-cookie')
            if (self._cookie != None):
                self._is_connected = True
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_connected'), self._mh.fromhere())            
                ev = event.Event('track_after_connect')
                self._mh.fire_event(ev)   
                result = True
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_missing_cookie'), self._mh.fromhere())
                
        else:
            try:
                error = objectify.fromstring(body).head.title if (body != None) else None
            except XMLSyntaxError as ex:
                error = body
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, error), self._mh.fromhere())    
        
        return result  
    
    def read(self, id=None, fields=None, query=None): 
        """Method reads records
        
        Args: 
           id (int): record id         
           fields (list): fields to be returned, default all
           query (str): query, see Trac doc
             
        Returns:
           tuple: result (bool), records (list of dictionary)
           
        Raises:
           event: track_before_read
           event: track_after_read
                
        """   
        
        message = 'id:{0}, fields:{1}, query:{2}'.format(id, fields, query)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_reading', message), self._mh.fromhere()) 
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False, None          
        
        if (fields == None and self._return_fields != None):
            fields = self._return_fields
        
        ev = event.Event('track_before_read', id, fields, query)
        if (self._mh.fire_event(ev) > 0):
            id = ev.argv(0)
            fields = ev.argv(1)
            query = ev.argv(2)
            
        if (ev.will_run_default()):                                      
            
            if (id != None):
                res, body = self._read_single(id)  
                recs = [body]                                             
            else:
                root = Element('methodCall')
                SubElement(root, 'methodName').text = 'ticket.query'
                el_params = SubElement(root, 'params')
                el_param = SubElement(el_params, 'param')
                SubElement(el_param, 'string').text = query                      
                body = tostring(root, xml_declaration=True)
                
                url = self._url + config['rpc'].format(self._project)
                headers = {'Cookie': self._cookie, 'Accept': 'application/xml'}                 
                res, body = self._client.send_request(url, method='POST', headers=headers, body=body,
                                                      content_type='xml')                
                
                if (res == 200):
                    
                    recs = []                    
                    for item in body.params.param.value.array.data.value:
                        id = item.int
                        
                        res, rec_body = self._read_single(id)
                        if (res == 200):
                            recs.append(rec_body)                                                                                                                      
                                   
            result = False
            records = None
            if (res == 200 and not hasattr(body, 'fault')):    
                    
                records = []        
                for rec in recs:
                    record = {}
                    
                    for val in rec.params.param.value.array.data.value:
                        if (hasattr(val, 'int') and (fields == None or 'id' in fields)):
                            record['id'] = val.int    
                        elif (hasattr(val, 'struct')):  
                                  
                            for item in val.struct.member:
                                key = str(item.name)                                                              
                                value = getattr(item.value, rec_fields[key]) if (key in rec_fields) else None                                                                  
                                if (fields == None or key in fields):
                                    record[key] = value            
                    
                    if (record != {}):            
                        records.append(record)
                            
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_read', len(records)), self._mh.fromhere())            
                ev = event.Event('track_after_read')
                self._mh.fire_event(ev)   
                result = True   
            else:
                fault_code = body.fault.value.struct.member[0].value.int
                fault_string = body.fault.value.struct.member[1].value.string
                message = 'fault_code:{0}, fault_string:{1}'.format(fault_code, fault_string)
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, message), self._mh.fromhere())                  
                      
            return (result, records) 
        
    def create(self, params={}):  
        """Method creates record
        
        Args: 
           params (dict): record content, key - field name, value - field value
             
        Returns:
           int: record id
           
        Raises:
           event: track_before_create
           event: track_after_create
                
        """       
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_creating', 'issue', params), self._mh.fromhere())
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return None          
        
        if (self._default_values != {}):
            for key, value in self._default_values.items():
                if (key not in params):
                    params[key] = value         
        
        ev = event.Event('track_before_create', params)
        if (self._mh.fire_event(ev) > 0):
            params = ev.argv(0)  
            
        if (ev.will_run_default()): 
            
            root = Element('methodCall')
            SubElement(root, 'methodName').text = 'ticket.create'
            el_params = SubElement(root, 'params')
            el_summary = SubElement(el_params, 'param')
            el_description = SubElement(el_params, 'param')
            el_struct = SubElement(SubElement(el_params, 'param'), 'struct')
                        
            for key, value in params.items():
                if (key == 'summary'):
                    SubElement(el_summary, rec_fields[key]).text = str(value)
                elif (key == 'description'):
                    SubElement(el_description, rec_fields[key]).text = str(value)
                elif (key in rec_fields and rec_fields[key] != 'dateTime.iso8601'):
                    el_member = SubElement(el_struct, 'member')
                    SubElement(el_member, 'name').text = str(key)
                    SubElement(SubElement(el_member, 'value'), rec_fields[key]).text = str(value).decode('utf8') if (version_info[0] == 2) else str(value)                   
            body = tostring(root, xml_declaration=True)
             
            url = self._url + config['rpc'].format(self._project)
            headers = {'Cookie': self._cookie, 'Accept': 'application/xml'}                 
            res, body = self._client.send_request(url, method='POST', headers=headers, body=body,
                                                      content_type='xml')
               
        id = None
        if (res == 200 and not hasattr(body, 'fault')):
            id = int(body.params.param.value.int)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_created', id), self._mh.fromhere())            
            ev = event.Event('track_after_create')
            self._mh.fire_event(ev) 
        else:
            fault_code = body.fault.value.struct.member[0].value.int
            fault_string = body.fault.value.struct.member[1].value.string
            message = 'fault_code:{0}, fault_string:{1}'.format(fault_code, fault_string)            
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, message), self._mh.fromhere())            
        
        return id            
    
    def update(self, id, params={}):  
        """Method updates record
        
        Args: 
           id (int): record id 
           params (dict): record content, key - field name, value - field value
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_update
           event: track_after_update
                
        """       
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_updating', 'issue', id, params), self._mh.fromhere())
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False          
        
        ev = event.Event('track_before_update', id, params)
        if (self._mh.fire_event(ev) > 0):
            id = ev.argv(0)
            params = ev.argv(1)  
            
        if (ev.will_run_default()): 
            
            root = Element('methodCall')
            SubElement(root, 'methodName').text = 'ticket.update'
            el_params = SubElement(root, 'params')
            SubElement(SubElement(el_params, 'param'), 'int').text = str(id)
            SubElement(SubElement(el_params, 'param'), 'string').text = 'comment'
            el_struct = SubElement(SubElement(el_params, 'param'), 'struct')
                        
            for key, value in params.items():
                if (key in rec_fields and rec_fields[key] != 'dateTime.iso8601'):
                    el_member = SubElement(el_struct, 'member')
                    SubElement(el_member, 'name').text = str(key)
                    SubElement(SubElement(el_member, 'value'), rec_fields[key]).text = str(value).decode('utf8') if (version_info[0] == 2) else str(value)                       
            body = tostring(root, xml_declaration=True)
             
            url = self._url + config['rpc'].format(self._project)
            headers = {'Cookie': self._cookie, 'Accept': 'application/xml'}                 
            res, body = self._client.send_request(url, method='POST', headers=headers, body=body,
                                                      content_type='xml')
               
        result = False
        if (res == 200 and not hasattr(body, 'fault')):
            result = True
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_updated', id), self._mh.fromhere())            
            ev = event.Event('track_after_update')
            self._mh.fire_event(ev) 
        else:
            fault_code = body.fault.value.struct.member[0].value.int
            fault_string = body.fault.value.struct.member[1].value.string
            message = 'fault_code:{0}, fault_string:{1}'.format(fault_code, fault_string)            
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, message), self._mh.fromhere())            
        
        return result    
    
    def delete(self, id):  
        """Method deletes record
        
        Args: 
           id (int): record id 
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_delete
           event: track_after_delete
                
        """       
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_deleting', 'issue', id), self._mh.fromhere())
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False          
        
        ev = event.Event('track_before_delete', id)
        if (self._mh.fire_event(ev) > 0):
            id = ev.argv(0)  
            
        if (ev.will_run_default()): 
            
            root = Element('methodCall')
            SubElement(root, 'methodName').text = 'ticket.delete'
            el_params = SubElement(root, 'params')
            SubElement(SubElement(el_params, 'param'), 'int').text = str(id)                  
            body = tostring(root, xml_declaration=True)
             
            url = self._url + config['rpc'].format(self._project)
            headers = {'Cookie': self._cookie, 'Accept': 'application/xml'}                 
            res, body = self._client.send_request(url, method='POST', headers=headers, body=body,
                                                      content_type='xml')
               
        result = False
        if (res == 200 and not hasattr(body, 'fault')):
            result = True
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_deleted', id), self._mh.fromhere())            
            ev = event.Event('track_after_delete')
            self._mh.fire_event(ev) 
        else:
            fault_code = body.fault.value.struct.member[0].value.int
            fault_string = body.fault.value.struct.member[1].value.string
            message = 'fault_code:{0}, fault_string:{1}'.format(fault_code, fault_string)            
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, message), self._mh.fromhere())            
        
        return result                  
        
    def _read_single(self, id):  
        """Method reads single record
        
        Args: 
           id (int): record id         
             
        Returns:
           tuple: result (bool), record (xml)
                
        """    
        
        root = Element('methodCall')
        SubElement(root, 'methodName').text = 'ticket.get'
        el_params = SubElement(root, 'params')
        el_param = SubElement(el_params, 'param')
        SubElement(el_param, 'int').text = str(id)                           
        body = tostring(root, xml_declaration=True)  
         
        url = self._url + config['rpc'].format(self._project)
        headers = {'Cookie': self._cookie, 'Accept': 'application/xml'}                 
        res, body = self._client.send_request(url, method='POST', headers=headers, body=body,
                                              content_type='xml') 
        
        return (res, body)                                          