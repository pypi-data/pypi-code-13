#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This module provides an easy client for the WL Document REST API.

    .. moduleauthor: Fabian Fischer <fabian.fischer@modul.ac.at>
'''

import json
import requests


class WlDocumentRestApiClient(object):
    '''
    The client for the WL Document REST API.
    '''
    API_VERSION = 1.0

    def __init__(self, base_url):
        '''
        Sets the base url for the API endpoint.

        :param base_url: The base URL without version number.
        :type base_url: str
        '''
        self.base_url = '/'.join([base_url, str(self.API_VERSION)])

    def add_document(self, portal_name, document):
        '''
        Adds the document to the given portal.

        :param portal_name: The portal to add the document to.
        :type portal_name: str
        :param document: The document to add. Either as JSON document \
                or as dict corresponding to the JSON format.
        :type document: str or dict
        :returns: The content_id of the added document.
        :rtype: int
        '''
        if isinstance(document, dict):
            document = json.dumps(document)
        r = requests.post('/'.join([self.base_url, 'documents', portal_name]),
                          data=document,
                          headers={'Content-Type': 'application/json'})
        return r.json()

    def retrieve_document(self, portal_name, content_id):
        '''
        Retrieve the document with content_id from portal_name.

        :param portal_name: The repository/matview name to add the document to.
        :type portal_name: str
        :param content_id: The document identifier/content_id.
        :type content_id: int
        :rtype: str
        '''
        r = requests.get('/'.join([self.base_url, 'documents', portal_name, str(content_id)]))
        return r.json()

    def update_document(self, portal_name, content_id, document):
        '''
        Adds the document to the specified repository/matview.

        :param portal_name: The portal name to add the document to.
        :type portal_name: str
        :param content_id: The document identifier/content_id.
        :type content_id: int
        :param document: The document to add, in the weblyzard API JSON \
            document format.
        :type document: str
        :returns: A JSON string containing information about the update action.
        :rtype: str
        '''
        if isinstance(document, dict):
            document = json.dumps(document)
        r = requests.put('/'.join([self.base_url,
                                   'documents',
                                   portal_name,
                                   str(content_id)]),
                         data=document,
                         headers={'Content-Type': 'application/json'})
        return r.json()

    def delete_document(self, portal_name, content_id):
        '''
        Deletes the document with the specified identifier. If a version is \
            provided, only that version is deleted.

        :param portal_name: The repository/matview name to add the document to.
        :type portal_name: str
        :param content_id: The document identifier/content_id.
        :type content_id: int
        :returns: A JSON string containing information about the delete action.
        :rtype: str
        '''
        r = requests.delete('/'.join([self.base_url,
                                      'documents',
                                      portal_name,
                                      str(content_id)]))
        return r.json()

    def annotate_document(self, document, analyzer_steps):
        '''
        Annotate the given document and return it augmented with the given
        annotations. If no annotation_types are provided, a set of default
        annotations will be added.

        :param document: The document to annotate, in the weblyzard API JSON \
            document format or dict corresponding to it.
        :type document: str or 
        :param analyzer_steps: The types of annotation to add as a list of \
            strings.
        :type analyzer_steps: list
        :returns: The JSON document with added annotations.
        :rtype: str
        '''
        assert isinstance(analyzer_steps, list)
        if isinstance(document, dict):
            document = json.dumps(document)
        print document
        print type(document)
        r = requests.post('/'.join([self.base_url,
                                    'annotate',
                                    '+'.join(analyzer_steps)]),
                          data=document,
                          headers={'Content-Type': 'application/json'})
        print r.url
        print r.content
        return r.json()

    def check_document(self, document):
        '''
        Checks the document's format.

        :param document: The document to annotate, in the weblyzard API JSON \
            document format or dict corresponding to it.
        :type document: str or 
        :returns: The result of the check.
        :rtype: str
        '''
        if isinstance(document, dict):
            document = json.dumps(document)
        r = requests.post('/'.join([self.base_url,
                                    'check']),
                          data=document,
                          headers={'Content-Type': 'application/json'})
        return r.json()

    def get_status(self):
        '''
        Calls the server's status method.
        '''
        r = requests.get(self.base_url+'/status')
        return r.json()