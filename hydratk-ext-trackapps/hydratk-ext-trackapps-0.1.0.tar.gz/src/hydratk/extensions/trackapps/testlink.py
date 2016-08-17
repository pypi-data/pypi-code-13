# -*- coding: utf-8 -*-
"""Client for TestLink

.. module:: trackapps.testlink
   :platform: Unix
   :synopsis: Client for TestLink
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
track_before_read_suite
track_after_rest_suite
track_before_read_plan
track_after_read_plan

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from hydratk.lib.network.rest.client import RESTClient
from lxml.etree import Element, SubElement, tostring
from lxml import objectify
from sys import version_info

config = {
  'rpc'      : '/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
}

entities = {
  'tl.getTestProjectByName'                  : 'project',
  'tl.getFirstLevelTestSuitesForTestProject' : 'test_suite',
  'tl.getTestSuitesForTestSuite'             : 'test_suite',
  'tl.getTestCasesForTestSuite'              : 'test_suite',
  'tl.getTestSuiteByID'                      : 'test_suite',
  'tl.createTestSuite'                       : 'test_suite',
  'tl.getTestPlanByName'                     : 'test_plan',
  'tl.getTestCasesForTestPlan'               : 'test_plan',
  'tl.createTestPlan'                        : 'test_plan',
  'tl.addTestCaseToTestPlan'                 : 'test_plan',    
  'tl.getLatestBuildForTestPlan'             : 'build',
  'tl.createBuild'                           : 'build',
  'tl.getTestCase'                           : 'test',
  'tl.createTestCase'                        : 'test',  
  'tl.reportTCResult'                        : 'test'
}

class Client(object):
    """Class Client
    """
    
    _mh = None
    _client = None
    _url = None
    _dev_key = None
    _project = None
    _project_id = None
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
        
        cfg = self._mh.cfg['Extensions']['TrackApps']['testlink']  
        if ('return_fields' in cfg and cfg['return_fields'] != None):
            self._return_fields = cfg['return_fields'].split(',')
        if ('default_values' in cfg and cfg['default_values'] != None):
            self._default_values = cfg['default_values']  
        if ('url' in cfg and cfg['url'] != None):
            self._url = cfg['url']    
        if ('dev_key' in cfg and cfg['dev_key'] != None):
            self._dev_key = cfg['dev_key']   
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
    def dev_key(self):
        """ dev key property getter """
        
        return self._dev_key
    
    @property
    def project(self):
        """ project property getter """
        
        return self._project
    
    @property
    def project_id(self):
        """ project id property getter """
        
        return self._project_id
    
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
    
    def connect(self, url=None, dev_key=None, project=None):
        """Method connects to TestLink
        
        Args:    
           url (str): URL        
           dev_key (str): development key to access API
           project (str): project
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_connect
           event: track_after_connect
                
        """    
        
        message = 'url:{0}, dev_key:{1}, project:{2}'.format(url, dev_key, project)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_connecting', message), self._mh.fromhere()) 
        
        if (url == None):
            url = self._url
        if (dev_key == None):
            dev_key = self._dev_key
        if (project == None):
            project = self._project             
        
        ev = event.Event('track_before_connect', url, dev_key, project)
        if (self._mh.fire_event(ev) > 0):
            url = ev.argv(0)
            dev_key = ev.argv(1)
            project = ev.argv(2)
            
        if (ev.will_run_default()):
            self._url = url
            self._dev_key = dev_key
            self._project = project
            
            root = Element('methodCall')
            SubElement(root, 'methodName').text = 'tl.getTestProjectByName'
            params = {'testprojectname': self._project}
            root.append(self._prepare_params('project', params))            
            body = tostring(root, xml_declaration=True)
            
            url = self._url + config['rpc']
            res, body = self._client.send_request(url, 'POST', body=body, content_type='xml')
         
        result = False   
        if (res == 200 and not hasattr(body, 'fault')):   
               
            value = body.params.param.value
            elem = value.array.data.value if (hasattr(value, 'array')) else value
            for item in elem.struct.member:
                if (item.name == 'id' and hasattr(item.value, 'string')):
                    self._project_id = int(item.value.string)
                    break
                if (item.name in ['msg', 'message']):
                    msg = item.value.string
                    break  
                                           
            if (self._project_id != None):  
                self._is_connected = True 
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_connected'), self._mh.fromhere())            
                ev = event.Event('track_after_connect')
                self._mh.fire_event(ev) 
                result = True
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, msg), self._mh.fromhere())                 
        elif (hasattr(body, 'fault')):
            fault_code = body.fault.value.struct.member[0].value.int
            fault_string = body.fault.value.struct.member[1].value.string
            message = 'fault_code:{0}, fault_string:{1}'.format(fault_code, fault_string)            
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, message), self._mh.fromhere())      
        
        return result     
           
    def _read(self, method, params={}, fields=None): 
        """Method reads records
        
        Args: 
           method (str): method title
           params (dict): method params, key - param name, value - param value
           fields (list): fields to be returned, default all
           
        Returns:
           tuple: result (bool), records (list of dictionary)
           
        Raises:
           event: track_before_read
           event: track_after_read
                
        """   
        
        entity = entities[method]
        message = 'entity:{0}, params:{1}, field:{2}'.format(entity, params, fields)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_reading', message), self._mh.fromhere())
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False, None          
        
        if (fields == None and self._return_fields != None):
            fields = self._return_fields        
        
        ev = event.Event('track_before_read', method, params, fields)
        if (self._mh.fire_event(ev) > 0):
            method = ev.argv(0)
            params = ev.argv(1)
            fields = ev.argv(2)
            
        if (ev.will_run_default()):                                      
            
            root = Element('methodCall')
            SubElement(root, 'methodName').text = method
            root.append(self._prepare_params(entity, params))                    
            body = tostring(root, xml_declaration=True)
                
            url = self._url + config['rpc']          
            res, body = self._client.send_request(url, method='POST', body=body, content_type='xml')                                                                                                                                   
                                   
        result = False
        records = None
        if (res == 200 and not hasattr(body, 'fault')):                                        
            records = []
            parse_simple = True
            
            elem = body.params.param.value
            if (hasattr(elem, 'array') and hasattr(elem.array.data, 'value')):
                elem = elem.array.data.value
                           
            for val in elem:                                
                if (hasattr(val, 'struct')):
                    record = {}  
                                
                    for item in val.struct.member:
                        key = str(item.name)
                        if (key == 'steps'): 
                            value = self._parse_steps(item.value, fields) 
                        elif (key.isdigit()):
                            if (entity == 'test_plan'):
                                value = self._parse_plan_tests(item.value, fields)
                            elif (entity == 'test_suite'):
                                value = self._parse_suites(item.value)
                            parse_simple = False                            
                            if (value != {}):
                                records.append(value)
                                
                        elif (key in ['msg', 'message']):
                            msg = item.value.string
                            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, msg), self._mh.fromhere()) 
                            return (False, None)
                        elif (hasattr(item.value, 'string')):   
                            value = getattr(item.value, 'string')
                        elif (hasattr(item.value, 'int')):   
                            value = getattr(item.value, 'int')                                                

                        if (parse_simple and (fields == None or key in fields)):                                                                                              
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
    
    def _create(self, method, params={}):  
        """Method creates record
        
        Args: 
           method (str): method
           params (dict): record content, key - field name, value - field value
             
        Returns:
           int: record id
           
        Raises:
           event: track_before_create
           event: track_after_create
                
        """       

        entity = entities[method]
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_creating', entity, params), self._mh.fromhere())
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return None        
        
        if (self._default_values != None):
            for key, value in self._default_values.items():
                if (key not in params):
                    params[key] = value 

        ev = event.Event('track_before_create', method, params)
        if (self._mh.fire_event(ev) > 0):
            method = ev.argv(0)
            params = ev.argv(1)  
            
        if (ev.will_run_default()): 
            
            root = Element('methodCall')
            SubElement(root, 'methodName').text = method
            root.append(self._prepare_params(entity, params))                    
            body = tostring(root, xml_declaration=True)
                
            url = self._url + config['rpc']           
            res, body = self._client.send_request(url, method='POST', body=body, content_type='xml') 

        id = None
        if (res == 200 and not hasattr(body, 'fault')): 
            value = body.params.param.value
            elem = value.array.data.value if (hasattr(value, 'array')) else value                                                                       
            for item in elem.struct.member:
                if (item.name == 'id' and hasattr(item.value, 'string')):
                    id = int(item.value.string)
                    break
                if (item.name in ['msg', 'message']):
                    msg = item.value.string
                    break
             
            msg = None 
            if (id != None): 
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_created', id), self._mh.fromhere())            
                ev = event.Event('track_after_create')
                self._mh.fire_event(ev)
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, msg), self._mh.fromhere())       
        else:
            fault_code = body.fault.value.struct.member[0].value.int
            fault_string = body.fault.value.struct.member[1].value.string
            message = 'fault_code:{0}, fault_string:{1}'.format(fault_code, fault_string)
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, message), self._mh.fromhere())           
        
        return id 
    
    def _update(self, method, params={}):          
        """Method updates record
        
        Args: 
           method (str): method
           params (dict): record content, key - field name, value - field value
             
        Returns:
           bool: result
           
        Raises:
           event: track_before_update
           event: track_after_update
                
        """       

        entity = entities[method]
        id = params['testcaseid']
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_updating', entity, id, params), self._mh.fromhere())

        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False  

        ev = event.Event('track_before_update', method, params)
        if (self._mh.fire_event(ev) > 0):
            method = ev.argv(0)
            params = ev.argv(1)  
            
        if (ev.will_run_default()): 
            
            root = Element('methodCall')
            SubElement(root, 'methodName').text = method
            root.append(self._prepare_params(entity, params))                    
            body = tostring(root, xml_declaration=True)
                
            url = self._url + config['rpc']           
            res, body = self._client.send_request(url, method='POST', body=body, content_type='xml') 

        result = False
        if (res == 200 and not hasattr(body, 'fault')): 
            
            value = body.params.param.value
            elem = value.array.data.value if (hasattr(value, 'array')) else value   
            msg = None                                                                    
            for item in elem.struct.member:
                if (item.name == 'status' and hasattr(item.value, 'boolean')):
                    result = True if (int(item.value.boolean) == 1) else False
                    break
                if (item.name in ['msg', 'message']):
                    msg = item.value.string
                    break
             
            if (result): 
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_updated', id), self._mh.fromhere())            
                ev = event.Event('track_after_update')
                self._mh.fire_event(ev)     
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, msg), self._mh.fromhere()) 
        else:
            fault_code = body.fault.value.struct.member[0].value.int
            fault_string = body.fault.value.struct.member[1].value.string
            message = 'fault_code:{0}, fault_string:{1}'.format(fault_code, fault_string)
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_error', res, message), self._mh.fromhere())           
        
        return result         
        
    def read_test_suite(self, path, steps=True, fields=None):
        """Method reads tests under test suite
        
        Args: 
           path (str): suite path
           steps (bool): get steps
           fields (list): test fields to be returned, default all
           
        Returns:
           tuple: result (bool), records (dict), key - test suite, value - list of tests
           
        Raises:
           event: track_before_read_suite
           event: track_after_read_suite                           
                
        """   
                
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_reading_folder', path, 'test_suite'), 
                      self._mh.fromhere()) 
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False, None          
        
        if (fields == None and self._return_fields != None):
            fields = self._return_fields        
        
        ev = event.Event('track_before_read_suite', path, steps)
        if (self._mh.fire_event(ev) > 0):
            path = ev.argv(0)
            steps = ev.argv(1)
            
        if (ev.will_run_default()):             
                    
            id = self._get_suite(path)            
            if (id == None):
                return (False, None)
            
            method = 'tl.getTestCasesForTestSuite'
            details = 'full' if (steps) else 'simple'
            params = {'testsuiteid': id, 'details': details}
            result, records = self._read(method, params)
                
            tests = {}
            suites = {str(id): {'name': path, 'parent': None, 'path': True}}
            for record in records:
                parent = str(record['parent_id'])
                parent_orig = parent                 
                    
                while (parent != None and parent not in suites):
                    method = 'tl.getTestSuiteByID'
                    params = {'testsuiteid': parent}
                    res, records = self._read(method, params)     
                    rec = records[0]                   
                    suites[parent] = {'name': rec['name'], 'parent': str(rec['parent_id']), 'path': False}
                    parent = str(rec['parent_id'])
                    
                for key, value in suites.items():
                    parent = None
                    while (not suites[key]['path']):
                        parent = suites[value['parent']] if (parent == None) else parent['parent']
                        suites[key]['name'] = '{0}/{1}'.format(parent['name'], suites[key]['name']) 
                        if (parent['parent'] == None):
                            suites[key]['path'] = True
                        
                suite_name = suites[parent_orig]['name']
                if (suite_name not in tests):
                    tests[suite_name] = []   
                
                record_new = {}
                for key, value in record.items():                                                  
                    if (fields == None or key in fields):                                                                                              
                        record_new[key] = value                     
                
                if (record_new != {}):  
                    tests[suite_name].append(record_new)
             
        if (result):   
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_folder_read', len(records)), 
                          self._mh.fromhere())            
            ev = event.Event('track_after_read_suite')
            self._mh.fire_event(ev)                   
            return (True, tests)
        else:
            return (False, None) 
        
    def create_test_suite(self, path, name, details=None):  
        """Method creates test folder on path
        
        Args: 
           path (str): suite path
           name (str): suite name
           details (str): suite details
             
        Returns:
           int: suite id
                
        """               
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return None          
        
        suite = self._get_suite(path)
        if (suite == None):
            return None
        
        method = 'tl.createTestSuite'
        params = {
                  'testprojectid': self._project_id, 
                  'testsuitename': name,
                  'parentid': suite,
                  'details': details
                 }
        
        return self._create(method, params)
    
    def read_test_plan(self, plan=None, plan_id=None, build_id=None, fields=None):
        """Method reads tests under plan
        
        Args:
           plan (str): plan name, will be translated to plan_id
           plan_id (int): plan_id
           build_id (int): build id, latest build will be used if not specified
           fields (list): test fields to be returned, default all   
           
        Returns:
           tuple: result (bool), records (list of dict)
           
        Raises:
           event: track_before_read_plan
           event: track_after_read_plan                           
                
        """ 
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_reading_folder', plan, 'test_plan'), 
                      self._mh.fromhere()) 
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False, None          
        
        if (fields == None and self._return_fields != None):
            fields = self._return_fields   
        
        ev = event.Event('track_before_read_plan', plan, plan_id, build_id)
        if (self._mh.fire_event(ev) > 0):
            plan = ev.argv(0)
            plan_id = ev.argv(1)
            build_id = ev.argv(2)        
        
        if (ev.will_run_default()): 
            
            if (plan != None):
                method = 'tl.getTestPlanByName'
                params = {
                          'testprojectname': self._project,
                          'testplanname': plan
                         } 
                res, plan = self._read(method, params)
                if (not res):
                    return (False, None)
            
                plan_id = plan[0]['id']
            
            if (build_id == None):
                method = 'tl.getLatestBuildForTestPlan'
                params = {'testplanid': plan_id}
                res, build = self._read(method, params)
            
                if (not res):
                    return (False, None)
            
                build_id = build[0]['id']            
            
            method = 'tl.getTestCasesForTestPlan'
            params = {
                      'testplanid': plan_id,
                      'buildid': build_id
                     } 
            
            result, records = self._read(method, params)
            if (records == None):
                return (False, None)
            
            records_new = []           
            for record in records:
                record_new = {}  
                for key, value in record.items():  
                    if (fields == None or key in fields):                                                                                              
                        record_new[key] = value                     
                
                if (record_new != {}):  
                    records_new.append(record_new)            
            
        if (result):   
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('track_folder_read', len(records_new)), 
                          self._mh.fromhere())            
            ev = event.Event('track_after_read_plan')
            self._mh.fire_event(ev)                   
            return (True, records_new)
        else:
            return (False, None)         
    
    def create_test_plan(self, name, notes=None):  
        """Method creates test plan
        
        Args: 
           name (str): plan name
           notes (str): plan notes
             
        Returns:
           int: plan id
                
        """  
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return None        
        
        method = 'tl.createTestPlan'
        params = {
                  'testprojectname': self._project,
                  'testplanname': name,
                  'notes': notes
                 }  
        
        return self._create(method, params) 
    
    def create_build(self, plan, name, notes=None):
        """Method creates build
        
        Args: 
           plan (int): plan id
           name (str): build name
           notes (str): build notes
             
        Returns:
           int: build id
                
        """         
    
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return None    
    
        method = 'tl.createBuild'
        params = {
                  'testplanid': plan,
                  'buildname': name,
                  'buildnotes': notes
                 }
        
        return self._create(method, params)
    
    def read_test(self, id, fields=None):  
        """Method reads test
        
        Args: 
           id (int): test id
           fields (list): fields to be returned default all
             
        Returns:
           tuple: result (bool), test (dict)
                
        """               
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False, None          
        
        method = 'tl.getTestCase'
        params = {'testcaseid': id}
        
        return self._read(method, params, fields)     
    
    def create_test(self, path, params={}, steps=[]):  
        """Method creates test
        
        Args: 
           path (str): suite path
           params (dict): params, key - field name, value - field value
           steps (list): list of dict, key - field name, value - field value
             
        Returns:
           int: test id
                
        """               
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return None        
        
        suite = self._get_suite(path)
        if (suite == None):
            return None
        
        method = 'tl.createTestCase'
        params['testprojectid'] = self._project_id
        params['testsuiteid'] = suite        
        params['steps'] = steps
        
        return self._create(method, params)  
    
    def add_test_to_plan(self, test, plan=None, plan_id=None):
        """Method adds test to plan
        
        Args:            
           test (int): test id
           plan (str): plan name
           plan_id (int): plan_id
             
        Returns:
           bool: result
                
        """           
        
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False        
        
        if (plan != None):
            method = 'tl.getTestPlanByName'
            params = {
                      'testprojectname': self._project,
                      'testplanname': plan
                     } 
            res, plan = self._read(method, params)
            if (not res):
                return False
            
            plan_id = plan[0]['id']
               
        method = 'tl.addTestCaseToTestPlan'
        params = {
                  'testprojectid': self._project_id,
                  'testplanid': plan_id,
                  'testcaseid': test
                 }   
        
        res, test_detail = self.read_test(test)
        if (res):
            params['version'] = test_detail[0]['version']         
        
        return self._update(method, params)  
    
    def update_test_execution(self, test, status, notes=None, plan=None, plan_id=None, build_id=None):   
        """Method updates test execution
        
        Args:
           test (int): test id
           status (str): status, p|f|b (passed|failed|blocked)
           notes (str): execution notes                
           plan (str): plan name, will be translated to id
           plan_id (int): plan id 
           build_id (int): build id, latest build will be used if not specified   
           
        Returns:
           bool: result   
             
        """
                    
        if (not self._is_connected):
            self._mh.dmsg('htk_on_warning', self._mh._trn.msg('track_not_connected'), self._mh.fromhere()) 
            return False                    
        
        if (plan != None):
            method = 'tl.getTestPlanByName'
            params = {
                      'testprojectname': self._project,
                      'testplanname': plan
                     }
            res, plan = self._read(method, params)
            
            if (not res):
                return False
            
            plan_id = plan[0]['id']
            
        if (build_id == None):
            method = 'tl.getLatestBuildForTestPlan'
            params = {'testplanid': plan_id}
            res, build = self._read(method, params)
            
            if (not res):
                return False
            
            build_id = build[0]['id']
            
        method = 'tl.reportTCResult'
        params = {
                  'testplanid': plan_id,
                  'buildid': build_id,
                  'testcaseid': test,
                  'status': status,
                  'notes': notes 
                 }
        return self._update(method, params)
        
    def _prepare_params(self, entity, params={}):
        """Method prepares params xml
        
        Args: 
           entity (str): entity type
           params (dict): params, key, value
           
        Returns:
           xml: params xml
                
        """          
        
        root = Element('params') 
        el_struct = SubElement(SubElement(SubElement(root, 'param'), 'value'), 'struct') 
        
        if ('devKey' not in params):
            params['devKey'] = self._dev_key 
        
        for key, value in params.items():
            el_param = SubElement(el_struct, 'member')
            SubElement(el_param, 'name').text = key
            if (key == 'version'):
                SubElement(SubElement(el_param, 'value'), 'int').text = str(value).decode('utf8') if (version_info[0] == 2) else str(value)            
            elif (key == 'steps'):
                el_steps = SubElement(SubElement(SubElement(el_param, 'value'), 'array'), 'data')
                for i in range(0, len(value)):
                    el_step = SubElement(SubElement(el_steps, 'value'), 'struct')
                    if ('step_number' not in value[i]):
                        value[i]['step_number'] = i+1
                    for name, val in value[i].items():
                        el_member = SubElement(el_step, 'member')
                        SubElement(el_member, 'name').text = name
                        SubElement(SubElement(el_member, 'value'), 'string').text = str(val).decode('utf8') if (version_info[0] == 2) else str(value) 
            else:
                SubElement(SubElement(el_param, 'value'), 'string').text = str(value).decode('utf8') if (version_info[0] == 2) else str(value)  
            
        return root 
    
    def _get_suite(self, path): 
        """Method gets suite from hierarchical path
        
        Args: 
           path (str): suite path, Suite1/Suite2/...    
             
        Returns:
           int: suite id

        """    
        
        folders = path.split('/')
        cnt = len(folders)
        
        found = False
        id = None
        for i in range(0, cnt):
            if (i == 0):
                method = 'tl.getFirstLevelTestSuitesForTestProject'
                params = {'testprojectid': self._project_id}        
            else:  
                method = 'tl.getTestSuitesForTestSuite'            
                params = {'testsuiteid': id}
            
            res, records = self._read(method, params)
            found = False
            if (res):
                for record in records:                
                    if (record['name'] == folders[i]):                        
                        id = record['id']
                        found = True
                        break   
                    
            if (not found):
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('track_unknown_folder', folders[i]), 
                               self._mh.fromhere())
                return None                                        
            
        return id    
    
    def _parse_steps(self, node, fields=None):
        """Method parses test steps
        
        Args:
           node (xml): steps node
           fields (list): fields to be returned, default all
           
        Returns:
           list: list of dict
        
        """   
        
        entity = 'test'
        if (fields == None and self._return_fields != None):
            fields = self._return_fields          
        
        steps = []
        if (hasattr(node, 'array')):
            for val in node.array.data.value:
                step = {}
                for item in val.struct.member:
                    key = str(item.name)                                                                             
                    value = getattr(item.value, 'string') 
                    if (fields == None or key in fields):                                                                                            
                        step[key] = value                     
                           
                steps.append(step)
            
        return steps  
    
    def _parse_plan_tests(self, node, fields=None):
        """Method parses plan tests
        
        Args:
           node (xml): test node
           fields (list): fields to be returned, default all
           
        Return:
           dict: params
           
        """
        
        entity = 'test'
        params = {}
        if (hasattr(node, 'array')):
            for item in node.array.data.value.struct.member:
                key = str(item.name)
                value = getattr(item.value, 'string')
                if (fields == None or key in fields):  
                    params[key] = value
            
        return params      
    
    def _parse_suites(self, node):
        """Method parses suites
        
        Args:
           node (xml): test suite node
           
        Return:
           dict: params
           
        """
        
        params = {}
        for item in node.struct.member:
            key = str(item.name)
            value = getattr(item.value, 'string')
            params[key] = value
            
        return params                   