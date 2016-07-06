# coding: utf-8

"""
WormApi.py
Copyright 2016 SmartBear Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class WormApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def create_worm_domain(self, worm_domain, **kwargs):
        """
        
        Create a WORM domain.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_worm_domain(worm_domain, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param WormDomainCreateParams worm_domain:  (required)
        :return: WormDomainExtended
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['worm_domain']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_worm_domain" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'worm_domain' is set
        if ('worm_domain' not in params) or (params['worm_domain'] is None):
            raise ValueError("Missing the required parameter `worm_domain` when calling `create_worm_domain`")


        resource_path = '/platform/1/worm/domains'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'worm_domain' in params:
            body_params = params['worm_domain']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['basic_auth']

        response = self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='WormDomainExtended',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_worm_domain(self, worm_domain_id, **kwargs):
        """
        
        View a single WORM domain.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_worm_domain(worm_domain_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str worm_domain_id: View a single WORM domain. (required)
        :return: WormDomains
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['worm_domain_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_worm_domain" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'worm_domain_id' is set
        if ('worm_domain_id' not in params) or (params['worm_domain_id'] is None):
            raise ValueError("Missing the required parameter `worm_domain_id` when calling `get_worm_domain`")


        resource_path = '/platform/1/worm/domains/{WormDomainId}'.replace('{format}', 'json')
        path_params = {}
        if 'worm_domain_id' in params:
            path_params['WormDomainId'] = params['worm_domain_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['basic_auth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='WormDomains',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_worm_settings(self, **kwargs):
        """
        
        Get the global WORM settings.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_worm_settings(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: WormSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_worm_settings" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/platform/1/worm/settings'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['basic_auth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='WormSettings',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def list_worm_domains(self, **kwargs):
        """
        
        List all WORM domains.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_worm_domains(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str sort: The field that will be used for sorting.
        :param int limit: Return no more than this many results at once (see resume).
        :param str dir: The direction of the sort.
        :param str resume: Continue returning results from previous call using this token (token should come from the previous call, resume cannot be used with other options).
        :return: WormDomainsExtended
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['sort', 'limit', 'dir', 'resume']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_worm_domains" % key
                )
            params[key] = val
        del params['kwargs']


        if 'limit' in params and params['limit'] < 1.0: 
            raise ValueError("Invalid value for parameter `limit` when calling `list_worm_domains`, must be a value greater than or equal to `1.0`")

        resource_path = '/platform/1/worm/domains'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'sort' in params:
            query_params['sort'] = params['sort']
        if 'limit' in params:
            query_params['limit'] = params['limit']
        if 'dir' in params:
            query_params['dir'] = params['dir']
        if 'resume' in params:
            query_params['resume'] = params['resume']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['basic_auth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='WormDomainsExtended',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def update_worm_domain(self, worm_domain, worm_domain_id, **kwargs):
        """
        
        Modify a single WORM domain.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_worm_domain(worm_domain, worm_domain_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param WormDomain worm_domain:  (required)
        :param str worm_domain_id: Modify a single WORM domain. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['worm_domain', 'worm_domain_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_worm_domain" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'worm_domain' is set
        if ('worm_domain' not in params) or (params['worm_domain'] is None):
            raise ValueError("Missing the required parameter `worm_domain` when calling `update_worm_domain`")
        # verify the required parameter 'worm_domain_id' is set
        if ('worm_domain_id' not in params) or (params['worm_domain_id'] is None):
            raise ValueError("Missing the required parameter `worm_domain_id` when calling `update_worm_domain`")


        resource_path = '/platform/1/worm/domains/{WormDomainId}'.replace('{format}', 'json')
        path_params = {}
        if 'worm_domain_id' in params:
            path_params['WormDomainId'] = params['worm_domain_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'worm_domain' in params:
            body_params = params['worm_domain']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['basic_auth']

        response = self.api_client.call_api(resource_path, 'PUT',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type=None,
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def update_worm_settings(self, worm_settings, **kwargs):
        """
        
        Modify the global WORM settings.  All input fields are optional, but one or more must be supplied.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_worm_settings(worm_settings, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param WormSettingsExtended worm_settings:  (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['worm_settings']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_worm_settings" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'worm_settings' is set
        if ('worm_settings' not in params) or (params['worm_settings'] is None):
            raise ValueError("Missing the required parameter `worm_settings` when calling `update_worm_settings`")


        resource_path = '/platform/1/worm/settings'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'worm_settings' in params:
            body_params = params['worm_settings']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['basic_auth']

        response = self.api_client.call_api(resource_path, 'PUT',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type=None,
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response
