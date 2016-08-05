'''
Created on Apr 29, 2016

:author: iitow
'''
from modules.http import Restful
from pluginable import Plugin
from modules.log import message


class rest(Plugin):
    '''
    This class handles all rest actions
    '''
    def __init__(self, action_manager):
        '''
        rest Constructor

        :param action_manager: Obj, from action_manager class
        '''
        self.action_manager = action_manager
        Plugin.__init__(self, self.action_manager)

    def send(self,
             req_type,
             base_url,
             url_ext,
             **defaults):
        '''
        Performs a http restful call

        :param type: String, PUT,GET
        :param base_url: String
        :param url_ext: String
        :param params: json string
        :param data: json string
        :param silent: boolean
        :example:
        ```
               - http.rest.send:
                     - "GET"
                     - "https://build.west.isilon.com"
                     - "api/branch"
                     - params: '{"name":"${BRANCH_NAME}"}'
                     - data: '{"name":"${BRANCH_NAME}"}'
        ```
        '''
        silent = False
        if defaults.get('silent',None) is True:
            silent = True
            defaults.pop("silent", None)
        if self.verbose:
            print message('info',"[send] %s @ %s/%s" % (req_type,base_url,url_ext),debug=self.debug)
            for key,value in defaults.iteritems():
                print message('info',"%s: %s" % (key,value),debug=self.debug)
        session = Restful(base_url)
        output = session.send(req_type, url_ext,**defaults)
        if self.verbose:
            if not silent:
                print message('info',output,debug=self.debug)
        if output.get('code') >= 300:
            error = "[%s] http request failed @ %s/%s" % (str(output.get('code')),base_url,url_ext)
            raise Exception(error)
            
        return output.get('response')
