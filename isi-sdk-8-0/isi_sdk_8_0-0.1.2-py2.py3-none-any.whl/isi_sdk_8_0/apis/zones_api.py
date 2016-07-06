# coding: utf-8

"""
ZonesApi.py
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


class ZonesApi(object):
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

    def create_zone(self, zone, **kwargs):
        """
        
        Create a new access zone.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_zone(zone, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param ZoneCreateParams zone:  (required)
        :return: CreateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['zone']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_zone" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'zone' is set
        if ('zone' not in params) or (params['zone'] is None):
            raise ValueError("Missing the required parameter `zone` when calling `create_zone`")


        resource_path = '/platform/3/zones'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'zone' in params:
            body_params = params['zone']

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
                                            response_type='CreateResponse',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def delete_zone(self, zone_id, **kwargs):
        """
        
        Delete the access zone.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_zone(zone_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int zone_id: Delete the access zone. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['zone_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_zone" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'zone_id' is set
        if ('zone_id' not in params) or (params['zone_id'] is None):
            raise ValueError("Missing the required parameter `zone_id` when calling `delete_zone`")


        resource_path = '/platform/3/zones/{ZoneId}'.replace('{format}', 'json')
        path_params = {}
        if 'zone_id' in params:
            path_params['ZoneId'] = params['zone_id']

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

        response = self.api_client.call_api(resource_path, 'DELETE',
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

    def get_zone(self, zone_id, **kwargs):
        """
        
        Retrieve the access zone information.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_zone(zone_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int zone_id: Retrieve the access zone information. (required)
        :return: Zones
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['zone_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_zone" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'zone_id' is set
        if ('zone_id' not in params) or (params['zone_id'] is None):
            raise ValueError("Missing the required parameter `zone_id` when calling `get_zone`")


        resource_path = '/platform/3/zones/{ZoneId}'.replace('{format}', 'json')
        path_params = {}
        if 'zone_id' in params:
            path_params['ZoneId'] = params['zone_id']

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
                                            response_type='Zones',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def list_zones(self, **kwargs):
        """
        
        List all access zones.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_zones(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: ZonesExtended
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
                    " to method list_zones" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/platform/3/zones'.replace('{format}', 'json')
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
                                            response_type='ZonesExtended',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def update_zone(self, zone, zone_id, **kwargs):
        """
        
        Modify the access zone. All input fields are optional, but one or more must be supplied.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_zone(zone, zone_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param Zone zone:  (required)
        :param int zone_id: Modify the access zone. All input fields are optional, but one or more must be supplied. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['zone', 'zone_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_zone" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'zone' is set
        if ('zone' not in params) or (params['zone'] is None):
            raise ValueError("Missing the required parameter `zone` when calling `update_zone`")
        # verify the required parameter 'zone_id' is set
        if ('zone_id' not in params) or (params['zone_id'] is None):
            raise ValueError("Missing the required parameter `zone_id` when calling `update_zone`")


        resource_path = '/platform/3/zones/{ZoneId}'.replace('{format}', 'json')
        path_params = {}
        if 'zone_id' in params:
            path_params['ZoneId'] = params['zone_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'zone' in params:
            body_params = params['zone']

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
