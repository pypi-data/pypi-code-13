import base64
import io
import json
import os
import tarfile
import urllib
import uuid
from datetime import datetime, timedelta

from .exceptions import InputDataError


class TopicApiMixin(object):
    """Mixing class which encapsulates the functionality of the object API
    service. See [[Working with Entities]] for documentation on the API.

    All the methods of this class are made available in the
    [[SquirroClient]] class.

    {TOC}
    """

    # Supported attributes for objects.
    TOPIC_ATTRIBUTES = set([
        'title', 'is_ready', 'query', 'type', 'owner_id',
    ])

    # Supported attributes for projects.
    PROJECT_ATTRIBUTES = set([
        'default_search', 'title', 'default_sort',
    ])

    #
    # Items
    #
    def get_encrypted_query(self, project_id, query=None, aggregations=None,
                            fields=None, created_before=None,
                            created_after=None, options=None, **kwargs):
        """Encrypts and signs the `query` and returns it. If set the
        `aggregations`, `created_before`, `created_after`, `fields` and
        `options` are part of the encrypted query as well.

        :param project_id: Project identifier.
        :param query: query to encrypt.
        For additional parameters see `self.query()`
        :returns: A dictionary which contains the encrypted query

        Example::

            >>> client.get_encrypted_query(
                    '2aEVClLRRA-vCCIvnuEAvQ',
                    query='test_query')
            {u'encrypted_query': 'YR4h147YAldsARmTmIrOcJqpuntiJULXPV3ZrX_'
            'blVWvbCavvESTw4Jis6sTgGC9a1LhrLd9Nq-77CNX2eeieMEDnPFPRqlPGO8V'
            'e2rlwuKuVQJGQx3-F_-eFqF-CE-uoA6yoXoPyYqh71syalWFfc-tuvp0a7c6e'
            'eKAO6hoxwNbZlb9y9pha0X084JdI-_l6hew9XKZTXLjT95Pt42vmoU_t6vh_w1'
            'hXdgUZMYe81LyudvhoVZ6zr2tzuvZuMoYtP8iMcVL_Z0XlEBAaMWAyM5hk_tAG'
            '7AbqGejZfUrDN3TJqdrmHUeeknpxpMp8nLTnbFMuHVwnj2hSmoxD-2r7BYbolJ'
            'iRFZuTqrpVi0='}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items/query_encryption'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        headers = {'Content-Type': 'application/json'}

        args = {
            'query': query,
            'aggregations': aggregations,
            'fields': fields,
            'options': options,
            'created_before': created_before,
            'created_after': created_after,
        }
        args.update(kwargs)
        data = dict([(k, v) for k, v in args.iteritems() if v is not None])

        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res)

    def query(self, project_id, query=None, aggregations=None, start=None,
              count=None, fields=None, highlight=None, next_params=None,
              created_before=None, created_after=None, options=None,
              encrypted_query=None, **kwargs):
        """Returns items for the provided project.

        This is the successor to the `get_items` method and should be used in
        its place.

        :param project_id: Project identifier.
        :param query: Optional query to run.
        :param start: Zero based starting point.
        :param count: Maximum number of items to return.
        :param fields: Fields to return.
        :param highlight: Dictionary containing highlight information. Keys
            are: `query` (boolean) if True the response will contain highlight
            information. `smartfilters` (list): List of Smart Filter names to
            be highlighted.
        :param options: Dictionary of options that influence the
            result-set. Valid options are:

                - `fold_near_duplicates` to fold near-duplicates together and
                  filter them out of the result-stream. Defaults to False.
                - `abstract_size` to set the length of the returned abstract in
                  number of characters. Defaults to the configured
                  default_abstract_size (500).
                - `update_cache` if `False` the result won't be cached. Used
                  for non-interactive queries that iterate over a large number
                  of items. Defaults to `True`.
        :param encrypted_query: Optional Encrypted query returned by
            `get_encrypted_query` method. This parameter overrides the `query`
            parameter and `query_template_params` (as part of `options`
            parameter), if provided. Returns a 403 if the encrypted query is
            expired or has been altered with.
        :param next_params: Parameter that were sent with the previous
            response as `next_params`.
        :param created_before: Restrict result set to items created before
            `created_before`.
        :param created_after: Restrict result set to items created after
            `created_after`.
        :param kwargs: Additional query parameters. All keyword arguments are
            passed on verbatim to the API.
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items/query'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        headers = {'Content-Type': 'application/json'}

        args = {
            'query': query,
            'aggregations': aggregations,
            'start': start,
            'count': count,
            'fields': fields,
            'highlight': highlight,
            'next_params': next_params,
            'options': options,
            'created_before': created_before,
            'created_after': created_after,
            'encrypted_query': encrypted_query,
        }
        args.update(kwargs)
        data = dict([(k, v) for k, v in args.iteritems() if v is not None])

        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res)

    def get_items(self, project_id, **kwargs):
        """Returns items for the provided project.

        :param project_id: Project identifier.
        :param kwargs: Query parameters. All keyword arguments are passed on
            verbatim to the API. See the [[Items#List Items|List Items]]
            resource for all possible parameters.
        :returns: A dictionary which contains the items for the project.

        Example::

            >>> client.get_items('2aEVClLRRA-vCCIvnuEAvQ', count=1)
            {u'count': 1,
             u'eof': False,
             u'items': [{u'created_at': u'2012-10-06T08:27:58',
                         u'id': u'haG6fhr9RLCm7ZKz1Meouw',
                         u'link': u'https://www.youtube.com/watch?v=Zzvhu42dWAc&feature=youtube_gdata',
                         u'read': True,
                         u'item_score': 0.5,
                         u'score': 0.56,
                         u'sources': [{u'id': u'oMNOQ-3rQo21q3UmaiaLHw',
                                       u'link': u'https://gdata.youtube.com/feeds/api/users/mymemonic/uploads',
                                       u'provider': u'feed',
                                       u'title': u'Uploads by mymemonic'},
                                      {u'id': u'H4nd0CasQQe_PMNDM0DnNA',
                                       u'link': None,
                                       u'provider': u'savedsearch',
                                       u'title': u'Squirro Alerts for "memonic"'}],
                         u'starred': False,
                         u'thumbler_url': u'22327aa6b6f4d2492346bed39ae354c0e94bf804/thumb/trunk/6f/87/f9/6f87f929773bd941d4a84209604ed014c7a21d7d.jpg',
                         u'title': u'Web Clipping - made easy with Memonic',
                         u'objects': [],
                         u'webshot_height': 360,
                         u'webshot_url': u'http://webshot.trunk.cluster.squirro.net.s3.amazonaws.com/6f/87/f9/6f87f929773bd941d4a84209604ed014c7a21d7d.jpg',
                         u'webshot_width': 480}],
             u'now': u'2012-10-11T14:39:54'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        res = self._perform_request('get', url, params=kwargs)
        return self._process_response(res)

    def get_item(self, project_id, item_id, **kwargs):
        """Returns the requested item for the provided project.

        :param project_id: Project identifier.
        :param item_id: Item identifier.
        :param kwargs: Query parameters. All keyword arguments are passed on
            verbatim to the API. See the [[Items#Get Item|Get Item]] resource
            for all possible parameters.
        :returns: A dictionary which contains the individual item.

        Example::

            >>> client.get_item('2aEVClLRRA-vCCIvnuEAvQ', 'haG6fhr9RLCm7ZKz1Meouw')
            {u'item': {u'created_at': u'2012-10-06T08:27:58',
                       u'id': u'haG6fhr9RLCm7ZKz1Meouw',
                       u'link': u'https://www.youtube.com/watch?v=Zzvhu42dWAc&feature=youtube_gdata',
                       u'read': True,
                       u'item_score': 0.5,
                       u'score': 0.56,
                       u'sources': [{u'id': u'oMNOQ-3rQo21q3UmaiaLHw',
                                     u'link': u'https://gdata.youtube.com/feeds/api/users/mymemonic/uploads',
                                     u'provider': u'feed',
                                     u'title': u'Uploads by mymemonic'},
                                    {u'id': u'H4nd0CasQQe_PMNDM0DnNA',
                                     u'link': None,
                                     u'provider': u'savedsearch',
                                     u'title': u'Squirro Alerts for "memonic"'}],
                       u'starred': False,
                       u'thumbler_url': u'22327aa6b6f4d2492346bed39ae354c0e94bf804/thumb/trunk/6f/87/f9/6f87f929773bd941d4a84209604ed014c7a21d7d.jpg',
                       u'title': u'Web Clipping - made easy with Memonic',
                       u'objects': [],
                       u'webshot_height': 360,
                       u'webshot_url': u'http://webshot.trunk.cluster.squirro.net.s3.amazonaws.com/6f/87/f9/6f87f929773bd941d4a84209604ed014c7a21d7d.jpg',
                       u'webshot_width': 480}}

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items/%(item_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'item_id': item_id})

        res = self._perform_request('get', url, params=kwargs)
        return self._process_response(res)

    def modify_item(self, project_id, item_id, star=None, read=None,
                    keywords=None):
        """Updates the flags and keywords of an item.

        :param project_id: Project identifier.
        :param item_id: Item identifier.
        :param star: Starred flag for the item, either `True` or `False`.
        :param read: Read flag for the item, either `True` or `False`.
        :param keywords: Overwrites all `keywords` of the item.

        Example::

            >>> client.modify_item('2aEVClLRRA-vCCIvnuEAvQ', 'haG6fhr9RLCm7ZKz1Meouw', star=True, read=False, keywords={'Canton': ['Berne'], 'Topic': None})

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items/%(item_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'item_id': item_id})

        # build item state
        state = {}
        if star is not None:
            state['starred'] = star
        if read is not None:
            state['read'] = read

        data = {'state': state}

        if not keywords is None:
            data['keywords'] = keywords

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        self._process_response(res, [204])

    def delete_item(self, project_id, item_id, object_ids=None):
        """Deletes an item. If `object_ids` is provided the item gets not
        deleted but is de-associated from these objects.

        :param project_id: Project identifier.
        :param item_id: Item identifier.
        :param object_ids: Object identifiers from which the item is
            de-associated.

        Example::

            >>> client.delete_item('2aEVClLRRA-vCCIvnuEAvQ', 'haG6fhr9RLCm7ZKz1Meouw', object_ids=['object01'])
        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items/%(item_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'item_id': item_id})

        # build params
        params = {}
        if object_ids:
            params['object_ids'] = ','.join(object_ids)

        res = self._perform_request('delete', url, params=params)
        self._process_response(res, [204])

    #
    #
    # Typeahead
    #

    def get_typeahead_suggestions(self, project_id, searchbar_query, cursor_pos):
        """Get the typeahead suggestions for a query `searchbar_query` in the
        project identified by the id `project_id`.

        :param project_id: Project identifier from which the typeahead
            suggestions should be returned.
        :param searchbar_query: The full query that goes into a searchbar. The
            `searchbar_query` will automatically be parsed and the suggestion
            on the field defined by the `cursor_pos` and filtered by the rest
            of the query will be returned. `searchbar_query` can not be None.
        :param cursor_pos: The position in the searchbar_query on which the
            typeahead is needed. `cursor_pos` parameter follow a 0-index
            convention, i.e. the first position in the searchbar-query is 0.
            `cursor_pos` should be a positive integer.

        :returns: A dict of suggestions

        Example::

            >>> client.get_typeahead_suggestions(
                    project_id='Sz7LLLbyTzy_SddblwIxaA',
                    'searchbar_query='Country:India c',
                    'cursor_pos'=15)

                {u'suggestions': [{
                    u'type': u'facetvalue', u'key': u'Country:India
                    City:Calcutta', u'value': u'city:Calcutta', 'score': 12,
                    'cursor_pos': 26, 'group': 'country'},

                    {u'type': u'facetvalue', u'key': u'Country:India
                    Name:Caesar', u'value': u'name:Caesar', 'score': 8,
                    'cursor_pos': 24, 'group': 'country'},

                    {u'type': u'facetname', u'key': u'Country:India city:',
                    u'value': u'City', 'score': 6, 'cursor_pos': 19, 'group':
                    'Fields'}]}
        """

        # construct the url
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/typeahead'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        # prepare the parameters dict
        params = {}
        params['searchbar_query'] = searchbar_query
        params['cursor_pos'] = cursor_pos

        # issue request
        res = self._perform_request('get', url, params=params)

        return self._process_response(res)

    # Objects
    #

    def get_user_objects(self, project_id, full=None):
        """Get all objects for the provided user.

        :param project_id: Project identifier from which the objects should be
            returned.
        :param full: If set to `True`, then include subscription and source
            details in the response.
        :returns: A list which contains the objects.

        Example::

            >>> client.get_user_objects(project_id='Sz7LLLbyTzy_SddblwIxaA')
            [{u'project_id': u'Sz7LLLbyTzy_SddblwIxaA',
              u'id': u'zFe3V-3hQlSjPtkIKpjkXg',
              u'is_ready': True,
              u'needs_preview': False,
              u'noise_level': None,
              u'title': u'Alexander Sennhauser',
              u'type': u'contact'}]

        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s/objects'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})
        if full:
            url += '/full'

        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_object(self, project_id, object_id):
        """Get object details.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :returns: A dictionary which contains the object.

        Example::

            >>> client.get_object('2aEVClLRRA-vCCIvnuEAvQ', '2sic33jZTi-ifflvQAVcfw')
            {u'project_id': u'2aEVClLRRA-vCCIvnuEAvQ',
             u'id': u'2sic33jZTi-ifflvQAVcfw',
             u'is_ready': True,
             u'managed_subscription': False,
             u'needs_preview': False,
             u'noise_level': None,
             u'subscriptions': [u'3qTRv4W9RvuOxcGwnnAYbg',
                                u'hw8j7LUBRM28-jAellgQdA',
                                u'4qBkea4bTv-QagNS76_akA',
                                u'NyfRri_2SUa_JNptx0JAnQ',
                                u'oTvI6rlaRmKvmYCfCvLwpw',
                                u'c3aEwdz5TMefc_u7hCl4PA',
                                u'Xc0MN_7KTAuDOUbO4mhG6A',
                                u'y1Ur-vLuRmmzUNMi4xGrJw',
                                u'iTdms4wgTRapn1ehMqJgwA',
                                u'MawimNPKSlmpeS9YlMzzaw'],
             u'subscriptions_processed': True,
             u'title': u'Squirro',
             u'type': u'organization'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/objects/%(object_id)s' % ({
                  'ep': self.topic_api_url, 'version': self.version,
                  'tenant': self.tenant, 'project_id': project_id,
                  'object_id': object_id})

        res = self._perform_request('get', url)
        return self._process_response(res)

    def new_object(self, project_id, title, owner_id=None, type=None,
                   is_ready=None):
        """Create a new object.

        :param project_id: Project identifier.
        :param title: Object title.
        :param owner_id: User identifier which owns the objects.
        :param type: Object type.
        :param is_ready: Object `is_ready` flag, either `True` or `False`.
        :returns: A dictionary which contains the project identifier and the
            new object identifier.

        Example::

            >>> client.new_object('H5Qv-WhgSBGW0WL8xolSCQ', '2aEVClLRRA-vCCIvnuEAvQ', 'Memonic', type='organization')
            {u'project_id': u'2aEVClLRRA-vCCIvnuEAvQ', u'id': u'2TBYtWgRRIa23h1rEveI3g'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/objects' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        # build data
        data = {'title': title}
        user_values = locals()
        for key in self.TOPIC_ATTRIBUTES:
            if user_values.get(key) is not None:
                data[key] = user_values[key]

        res = self._perform_request('post', url, data=data)
        return self._process_response(res, [201])

    def modify_object(self, project_id, object_id, title=None,
                      is_ready=None, noise_level=None):
        """Modify an object.

        :param project_id: Project identifier for the object.
        :param object_id: Object identifier.
        :param title: New object title.
        :param is_ready: New object `is_ready` flag, either `True` for `False`.
        :param noise_level: New object noise level. Can be any float value from
            0.0 to 1.0.
        :returns: A dictionary which contains the object.

        Example::

            >>> client.modify_object('2aEVClLRRA-vCCIvnuEAvQ', '2TBYtWgRRIa23h1rEveI3g', is_ready=False)
            {}

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/objects/%(object_id)s' % ({
                  'ep': self.topic_api_url, 'version': self.version,
                  'tenant': self.tenant, 'project_id': project_id, 'object_id': object_id})

        # build data
        data = {}
        user_values = locals()
        for key in self.TOPIC_ATTRIBUTES:
            if user_values.get(key) is not None:
                data[key] = user_values[key]

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201, 204])

    def delete_object(self, project_id, object_id):
        """Delete a object.

        :param project_id: Project identifier.
        :param object_id: Object identifier.

        Example::

            >>> client.delete_object('2aEVClLRRA-vCCIvnuEAvQ', '2TBYtWgRRIa23h1rEveI3g')

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/objects/%(object_id)s' % ({
                  'ep': self.topic_api_url, 'version': self.version,
                  'tenant': self.tenant, 'project_id': project_id, 'object_id': object_id})

        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    def pause_object(self, project_id, object_id, subscription_ids=None):
        """Pause all (or some) subscriptions of an object.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param subscription_ids: Optional, list of subscription identifiers.
            Only pause these subscriptions of the object.

        Example::

            >>> client.pause_object('2aEVClLRRA-vCCIvnuEAvQ', '2TBYtWgRRIa23h1rEveI3g')

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/objects/%(object_id)s/pause' % ({
                  'ep': self.topic_api_url, 'version': self.version,
                  'tenant': self.tenant, 'project_id': project_id, 'object_id': object_id})

        data = {}
        if subscription_ids:
            data = {'subscription_ids': subscription_ids}

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request('post', url, data=json.dumps(data),
                                    headers=headers)
        self._process_response(res, [200, 204])

    def resume_object(self, project_id, object_id, subscription_ids=None):
        """Resume all (or some) paused subscriptions of an object.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param subscription_ids: Optional, list of subscription identifiers.
            Only resume these subscriptions of the object.

        Example::

            >>> client.resume_object('2aEVClLRRA-vCCIvnuEAvQ', '2TBYtWgRRIa23h1rEveI3g')

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/objects/%(object_id)s/resume' % ({
                  'ep': self.topic_api_url, 'version': self.version,
                  'tenant': self.tenant, 'project_id': project_id, 'object_id': object_id})

        data = {}
        if subscription_ids:
            data = {'subscription_ids': subscription_ids}

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request('post', url, data=json.dumps(data),
                                    headers=headers)
        self._process_response(res, [200, 204])

    #
    # Projects
    #

    def get_user_projects(self, owner_id=None, include_objects=False):
        """Get projects for the provided user.

        :param owner_id: User identifier which owns the projects.
        :param include_objects: Whether to include object information, either
            `True` or `False`.
        :returns: A list of projects.

        Example::

            >>> client.get_user_projects()
            [{u'id': u'Sz7LLLbyTzy_SddblwIxaA',
              u'title': u'My Contacts',
              u'objects': 1,
              u'type': u'my contacts'},
             {u'id': u'2aEVClLRRA-vCCIvnuEAvQ',
              u'title': u'My Organizations',
              u'objects': 2,
              u'type': u'my organizations'}]

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant})

        # build params
        params = {'include_objects': include_objects}
        if owner_id is not None:
            params['owner_id'] = owner_id

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def get_project(self, project_id):
        """Get project details.

        :param project_id: Project identifier.
        :returns: A dictionary which contains the project.

        Example::

            >>> client.get_project('2aEVClLRRA-vCCIvnuEAvQ')
            {u'id': u'2aEVClLRRA-vCCIvnuEAvQ',
             u'title': u'My Organizations',
             u'type': u'my organizations'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        res = self._perform_request('get', url)
        return self._process_response(res)

    def new_project(self, title, owner_id=None, locator=None,
                    default_sort=None):
        """Create a new project.

        :param title: Project title.
        :param owner_id: User identifier which owns the objects.
        :param locator: Custom index locator configuration which is a
            dictionary which contains the `index_server` (full URI including
            the port for index server) key.
        :param default_sort: Custom default sort configuration which is a
            dictionary which contains the `sort` (valid values are `date` and
            `relevance`) and `order` (valid values are `asc` and `desc`) keys.
        :returns: A dictionary which contains the project identifier.

        Example::

            >>> locator = {'index_server': 'http://10.0.0.1:9200'}
            >>> default_sort = [{'relevance': {'order': 'asc'}}]
            >>> client.new_project('My Project', locator=locator, default_sort=default_sort)
            {u'id': u'gd9eIipOQ-KobU0SwJ8VcQ'}
        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant})

        # build data
        data = {'title': title}
        if owner_id is not None:
            data['owner_id'] = owner_id
        if locator is not None:
            data['locator'] = json.dumps(locator)
        if default_sort is not None:
            data['default_sort'] = json.dumps(default_sort)

        res = self._perform_request('post', url, data=data)
        return self._process_response(res, [201])

    def modify_project(self, project_id, **kwargs):
        """Modify a project.

        :param project_id: Project identifier.
        :param kwargs: Query parameters. All keyword arguments are passed on
            verbatim to the API. See the
            [[Projects#Update Project|Update Project]] resource for all
            possible parameters.

        Example::

            >>> client.modify_project('gd9eIipOQ-KobU0SwJ8VcQ', title='My Other Project')

        """
        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        # build data
        data = {}
        for key in self.PROJECT_ATTRIBUTES:
            if key in kwargs:
                data[key] = kwargs[key]

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201, 204])

    def delete_project(self, project_id):
        """Delete a project.

        :param project_id: Project identifier.

        Example::

            >>> client.delete_project('gd9eIipOQ-KobU0SwJ8VcQ')

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    #
    # Subscriptions
    #

    def get_object_subscriptions(self, project_id, object_id, user_id=None,
                                 filter_deleted=None):
        """Get all subscriptions for the provided object.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param user_id: User identifier.
        :param filter_deleted: If `True` returns only non-deleted
            subscriptions.
        :returns: A list which contains subscriptions.

        Example::

            >>> client.get_object_subscriptions('2sic33jZTi-ifflvQAVcfw', '2TBYtWgRRIa23h1rEveI3g')
            [
                {
                    u'config': {
                        u'market': u'de-CH',
                        u'query': u'squirro',
                        u'vertical': u'News',
                    },
                    u'deleted': False,
                    u'id': u'hw8j7LUBRM28-jAellgQdA',
                    u'link': u'http://bing.com/news/search?q=squirro',
                    u'modified_at': u'2012-10-09T07:54:12',
                    u'provider': u'bing',
                    u'seeder': None,
                    u'source_id': u'2VkLodDHTmiMO3rlWi2MVQ',
                    u'title': u'News Alerts for "squirro" in Switzerland',
                }
            ]
        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id})

        # build params
        params = {}
        if user_id is not None:
            params['user_id'] = user_id
        if filter_deleted is not None:
            params['filter_deleted'] = filter_deleted

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def get_subscription(self, project_id, object_id, subscription_id):
        """Get subscription details.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param subscription_id: Subscription identifier.
        :returns: A dictionary which contains the subscription.

        Example::

            >>> client.get_subscription('2sic33jZTi-ifflvQAVcfw', '2TBYtWgRRIa23h1rEveI3g', 'hw8j7LUBRM28-jAellgQdA')
            {
                u'config': {
                    u'market': u'de-CH',
                    u'query': u'squirro',
                    u'vertical': u'News',
                },
                u'deleted': False,
                u'id': u'hw8j7LUBRM28-jAellgQdA',
                u'link': u'http://bing.com/news/search?q=squirro',
                u'modified_at': u'2012-10-09T07:54:12',
                u'provider': u'bing',
                u'seeder': None,
                u'source_id': u'2VkLodDHTmiMO3rlWi2MVQ',
                u'title': u'News Alerts for "squirro" in Switzerland',
                u'processed': True,
                u'paused': False,
            }
        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions/%(subscription_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id,
            'subscription_id': subscription_id})

        res = self._perform_request('get', url)
        return self._process_response(res)

    def new_subscription(self, project_id, object_id, provider, config,
                         user_id=None, seeder=None, private=None):
        """Create a new subscription.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param provider: Provider name.
        :param config: Provider configuration dictionary.
        :param user_id: User identifier.
        :param seeder: Seeder which manages the subscription.
        :param private: Hints that the contents for this subscriptions should
            be treated as private.
        :returns: A dictionary which contains the new subscription.

        Example::

            >>> client.new_subscription('2sic33jZTi-ifflvQAVcfw', '2TBYtWgRRIa23h1rEveI3g', 'feed', {'url': 'http://blog.squirro.com/rss'})
            {u'config': {u'url': u'http://blog.squirro.com/rss'},
             u'deleted': False,
             u'id': u'oTvI6rlaRmKvmYCfCvLwpw',
             u'link': u'http://blog.squirro.com/rss',
             u'modified_at': u'2012-10-12T09:32:09',
             u'provider': u'feed',
             u'seeder': u'team',
             u'source_id': u'D3Q8AiPoTg69bIkqFhe3Bw',
             u'title': u'Squirro',
             u'processed': False,
             u'paused': False}

        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id})

        # build data
        data = {
            'provider': provider, 'config': json.dumps(config)
        }
        if user_id is not None:
            data['user_id'] = user_id
        if seeder is not None:
            data['seeder'] = seeder
        if private is not None:
            data['private'] = private

        res = self._perform_request('post', url, data=data)
        return self._process_response(res, [200, 201])

    def modify_subscription(self, project_id, object_id, subscription_id,
                            config=None):
        """Modify an existing subscription.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param subscription_id: Subscription identifier.
        :param config: Changed config of the subscription.

        Example::

            >>> client.modify_subscription('2sic33jZTi-ifflvQAVcfw', '2TBYtWgRRIa23h1rEveI3g', 'oTvI6rlaRmKvmYCfCvLwpw', config={'url': 'http://blog.squirro.com/atom'})
        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions/%(subscription_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id, 'subscription_id': subscription_id})

        # build data
        data = {}
        if config is not None:
            data['config'] = json.dumps(config)

        res = self._perform_request('put', url, data=data)
        return self._process_response(res, [200])

    def delete_subscription(self, project_id, object_id, subscription_id,
                            seeder=None):
        """Delete an existing subscription.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param subscription_id: Subscription identifier.
        :param seeder: Seeder that deletes the subscription.

        Example::

            >>> client.delete_subscription('2sic33jZTi-ifflvQAVcfw', '2TBYtWgRRIa23h1rEveI3g', 'oTvI6rlaRmKvmYCfCvLwpw')

        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions/%(subscription_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id,
            'subscription_id': subscription_id})

        # build params
        params = {}
        if seeder is not None:
            params['seeder'] = seeder

        res = self._perform_request('delete', url, params=params)
        self._process_response(res, [204])

    def pause_subscription(self, project_id, object_id, subscription_id):
        """Pause a subscription.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param subscription_id: Subscription identifier.

        Example::

            >>> client.pause_subscription('2sic33jZTi-ifflvQAVcfw', '2TBYtWgRRIa23h1rEveI3g', 'hw8j7LUBRM28-jAellgQdA')
        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions/%(subscription_id)s/pause'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id,
            'subscription_id': subscription_id})

        res = self._perform_request('post', url)
        self._process_response(res, [200, 204])

    def resume_subscription(self, project_id, object_id, subscription_id):
        """Resume a paused subscription.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param subscription_id: Subscription identifier.

        Example::

            >>> client.resume_subscription('2sic33jZTi-ifflvQAVcfw', '2TBYtWgRRIa23h1rEveI3g', 'hw8j7LUBRM28-jAellgQdA')
        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions/%(subscription_id)s/resume'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id,
            'subscription_id': subscription_id})

        res = self._perform_request('post', url)
        self._process_response(res, [200, 204])

    #
    # Object Signals
    #

    def get_object_signals(self, project_id, object_id, flat=False):
        """Return a dictionary of object signals for a object.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param flat: Set to `True` to receive a simpler dictionary
            representation. The `seeder` information is not displayed in that
            case.
        :returns: Dictionary of signals on this object.

        Example::

            >>> client.get_object_signals('gd9eIipOQ-KobU0SwJ8VcQ', '2sic33jZTi-ifflvQAVcfw')
            {'signals': [{u'key': u'email_domain',
                          u'value': 'nestle.com',
                          u'seeder': 'salesforce'}]}

            >>> client.get_object_signals('gd9eIipOQ-KobU0SwJ8VcQ', '2sic33jZTi-ifflvQAVcfw', flat=True)
            {u'email_domain': 'nestle.com'}
        """
        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s/objects/%(object_id)s/signals'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id})

        res = self._perform_request('get', url)
        retval = self._convert_flat(flat, self._process_response(res, [200]))
        return retval

    def update_object_signals(self, project_id, object_id, signals,
                              seeder=None, flat=False):
        """Updates the object signals of a object.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param signals: List of all objects to update. Only signals that exist
            in this list will be touched, the others are left intact. Use the value
            `None` for a key to delete that signal.
        :param seeder: Seeder that owns these signals. Should be set for
            automatically written values.
        :param flat: Set to `True` to pass in and receive a simpler dictionary
            representation. The `seeder` information is not displayed in that
            case.
        :returns: List or dictionary of all signals of that object in the same
            format as returned by `get_object_signals`.

        Example::

            >>> client.update_object_signals('gd9eIipOQ-KobU0SwJ8VcQ', '2sic33jZTi-ifflvQAVcfw',
                [{'key': 'essentials',
                  'value': ['discovery-baseobject-A96PWkLzTIWSJy3WMsvzzw']}])
            [
                {u'key': u'essentials',
                 u'value': [u'discovery-baseobject-A96PWkLzTIWSJy3WMsvzzw'],
                 u'seeder': None},
                {u'key': u'email_domain',
                 u'value': 'nestle.com',
                 u'seeder': 'salesforce'}
            ]

            >>> client.update_object_signals('gd9eIipOQ-KobU0SwJ8VcQ', '2sic33jZTi-ifflvQAVcfw',
                {'essentials': ['discovery-baseobject-A96PWkLzTIWSJy3WMsvzzw']},
                flat=True)
            {u'essentials': [u'discovery-baseobject-A96PWkLzTIWSJy3WMsvzzw'],
             u'email_domain': u'nestle.com'}
        """
        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s/objects/%(object_id)s/signals'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id})

        if flat:
            signals = [{'key': key, 'value': value}
                       for key, value in signals.iteritems()]

        data = {'signals': signals, 'seeder': seeder}

        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        retval = self._convert_flat(flat, self._process_response(res, [200]))
        return retval

    def _convert_flat(self, flat, retval):
        """Converts the object API response to the flat format.
        """
        if flat:
            retval = dict([(s['key'], s['value']) for s in retval['signals']])
        return retval

    #
    # Preview
    #

    def get_preview(self, project_id, provider, config):
        """Preview the provider configuration.

        :param project_id: Project identifier.
        :param provider: Provider name.
        :param config: Provider configuration.
        :returns: A dictionary which contains the provider preview items.

        Example::

            >>> client.get_preview('feed', {'url': ''})
            {u'count': 2,
             u'items': [{u'created_at': u'2012-10-01T20:12:07',
                         u'id': u'F7EENNQeTz2z7O7htPACgw',
                         u'link': u'http://blog.squirro.com/post/32680369129/swisscom-features-our-sister-product-memonic-in-its-all',
                         u'read': False,
                         u'item_score': 0,
                         u'score': 0,
                         u'starred': False,
                         u'thumbler_url': u'd486ac63fc3490b42ce044feba7b71b18cb84061/thumb/trunk/57/cd/10/57cd10d6e0163a7e068370d91f14ed0e46dca085.jpg',
                         u'title': u'Swisscom features our sister product Memonic in its all new App Store',
                         u'webshot_height': 237,
                         u'webshot_url': u'http://webshot.trunk.cluster.squirro.net.s3.amazonaws.com/57/cd/10/57cd10d6e0163a7e068370d91f14ed0e46dca085.jpg',
                         u'webshot_width': 600},
                        {u'created_at': u'2012-09-25T08:09:24',
                         u'id': u'Nrj308UNTEixra3qTYLn7w',
                         u'link': u'http://blog.squirro.com/post/32253089480/247-million-emails-are-sent-every-day-80-are',
                         u'read': False,
                         u'item_score': 0,
                         u'score': 0,
                         u'starred': False,
                         u'thumbler_url': u'b4269d64a8b5993678a33a68ea013e1e8875bc67/thumb/trunk/ca/24/f2/ca24f263eb044e8ed3bc5135ab7d56112cb8206a.jpg',
                         u'title': u'247 million emails are sent every day - 80% are spam.\\nPeople...',
                         u'webshot_height': 360,
                         u'webshot_url': u'http://webshot.trunk.cluster.squirro.net.s3.amazonaws.com/ca/24/f2/ca24f263eb044e8ed3bc5135ab7d56112cb8206a.jpg',
                         u'webshot_width': 480}]}

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/preview' % ({
            'ep': self.topic_api_url, 'project_id': project_id,
            'version': self.version, 'tenant': self.tenant})

        # build params
        params = {'provider': provider, 'config': json.dumps(config)}

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    #
    # Saved searches
    #

    def new_savedsearch(self, scope_type, scope_id, query,
                        name=None, actions=None, created_before=None,
                        created_after=None, relative_start=None,
                        relative_end=None, dashboard_id=None):
        """Create a new saved search.

        :param scope_type: Saved search scope type.
        :param scope_id: Saved search scope identifier.
        :param query: Saved search query.
        :param name: The name of the new saved search.
        :param actions: A list of actions to execute when the saved search
            matches.
        :param created_before: Only show items created before.
        :param created_after: Only show items created after.
        :param relative_start: Relative start date for displaying.
        :param relative_end: Relative end date for displaying.
        :param dashboard_id: Dashboard this query is associated with (query
            will be updated whenever the dashboard changes).
        :returns: A dictionary with created saved search.

        Example::

            >>> client.new_savedsearch(
                    scope_id='2sic33jZTi-ifflvQAVcfw',
                    scope_type='project',
                    query='hello world',
                )
            {u'actions': [{u'id': u'678b8102e5c55683130a469c12f6ce55a97ab8b5',
                           u'type': u'show'}],
             u'id': u'1ba32747c302d1c3cd4f2d43cfe937d7ae64489b',
             u'query': u'hello world'}
        """
        if actions is not None and not isinstance(actions, list):
            raise ValueError('`actions` must be a list')
        url = self._get_savedsearch_base_url(scope_type) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_id': scope_id,
        })
        headers = {'Content-Type': 'application/json'}
        data = {
            'query': query,
            'actions': actions,
            'name': name,
            'created_before': created_before,
            'created_after': created_after,
            'relative_start': relative_start,
            'relative_end': relative_end,
            'dashboard_id': dashboard_id,
        }
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201, 200])

    def modify_savedsearch(self, savedsearch_id, scope_type, scope_id, query,
                           name=None, actions=None, created_before=None,
                           created_after=None, relative_start=None,
                           relative_end=None):
        """Modify a saved search.

        :param savedsearch_id: Saved search identifier.
        :param scope_type: Saved search scope type.
        :param scope_id: Saved search scope identifier.
        :param query: Saved search query.
        :param name: The new name of the saved search.
        :param actions: A list of actions to execute when the saved search
            matches.
        :param created_before: Only show items created before.
        :param created_after: Only show items created after.
        :param relative_start: Relative start date for displaying.
        :param relative_end: Relative end date for displaying.
        :return: A dictionary with updated saved search data.

        Example::

            >>> client.modify_savedsearch(
                    savedsearch_id='77e2bbb206527a2e1ff2e5baf548656a8cb999cc',
                    scope_id='2sic33jZTi-ifflvQAVcfw',
                    scope_type='project',
                    query='test me'
                )
            {u'actions': [{u'id': u'4e23249793e9a3df2126321109c6619df66aaa51',
                           u'type': u'show'}],
             u'id': u'77e2bbb206527a2e1ff2e5baf548656a8cb999cc',
             u'query': u'test me'}
        """
        url = self._get_savedsearch_base_url(scope_type, savedsearch_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_id': scope_id,
            'savedsearch_id': savedsearch_id,
        })
        data = {
            'query': query,
            'actions': actions,
            'name': name,
            'created_before': created_before,
            'created_after': created_after,
            'relative_start': relative_start,
            'relative_end': relative_end,
        }
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res)

    def get_savedsearches(self, scope_type, scope_id):
        """Get saved searches for the provided scope.

        :param scope_type: Saved search scope type.
        :param scope_id: Saved search scope identifier.
        :returns: A dictionary with data for the saved searches.

        Example::

            >>> client.get_savedsearches(scope_type='project', scope_id='2sic33jZTi-ifflvQAVcfw')
            {u'savedsearches': [{u'actions': [{u'id': u'ff18180f74ebdf4b964ac8b5dde66531e0acba83',
                                               u'type': u'show'}],
                                 u'id': u'9c2d1a9002a8a152395d74880528fbe4acadc5a1',
                                 u'query': u'hello world',
                                 u'relative_start': '24h',
                                 u'relative_end': None,
                                 u'created_before': None,
                                 u'created_after': None}]}
        """
        url = self._get_savedsearch_base_url(scope_type) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_id': scope_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_savedsearch(self, scope_type, scope_id, savedsearch_id):
        """Get saved search details.

        :param scope_type: Saved search scope type.
        :param scope_id: Saved search scope identifier.
        :param savedsearch_id: Saved search identifier.
        :returns: A dictionary with saved search data.

        Example::

            >>> client.get_savedsearch(scope_type='project',
                                       scope_id='2sic33jZTi-ifflvQAVcfw',
                                       savedsearch_id='77e2bbb206527a2e1ff2e5baf548656a8cb999cc')
            {u'actions': [{u'id': u'4e23249793e9a3df2126321109c6619df66aaa51',
                           u'type': u'show'}],
             u'id': u'77e2bbb206527a2e1ff2e5baf548656a8cb999cc',
             u'query': u'test me',
             u'relative_start': '24h',
             u'relative_end': None,
             u'created_before': None,
             u'created_after': None}
        """

        url = self._get_savedsearch_base_url(scope_type, savedsearch_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_type': scope_type,
            'scope_id': scope_id,
            'savedsearch_id': savedsearch_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def delete_savedsearch(self, scope_type, scope_id, savedsearch_id):
        """Delete a savedsearch.

        :param scope_type: Saved search scope type.
        :param scope_id: Saved search scope identifier.
        :param savedsearch_id: Saved search identifier.

        Example::

            >>> client.delete_savedsearch(scope_type='project',
                                          scope_id='2sic33jZTi-ifflvQAVcfw',
                                          savedsearch_id='9c2d1a9002a8a152395d74880528fbe4acadc5a1')
        """
        url = self._get_savedsearch_base_url(scope_type, savedsearch_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_type': scope_type,
            'scope_id': scope_id,
            'savedsearch_id': savedsearch_id,
        })
        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    def _get_savedsearch_base_url(self, scope_type, savedsearch_id=None):
        """Returns the URL template for the saved searches of this scope
        type."""
        parts = ['%(ep)s/v0/%(tenant)s']
        if scope_type == 'project':
            parts.append('/projects/%(scope_id)s/savedsearches')
        else:
            raise InputDataError(400, 'Invalid scope type %r' % scope_type)

        if savedsearch_id:
            parts.append('/%(savedsearch_id)s')

        return ''.join(parts)

    #
    # trend detections
    #

    def new_trenddetection(self, project_id, name, query, email_user,
                           aggregation_interval=None, aggregation_field=None,
                           aggregation_method=None,
                           aggregation_time_field=None):
        """Create a new trend detection.

        :param project_id: Id of the project.
        :param query: Trend Detection query.
        :param name: The name of the new Trend Detection Entity.
        :param email_user: Email address for alert emails.
        :param aggregation_interval: Time aggregation interval for items.
            `aggregation_interval` is `{offset}{unit}` where `offset` is a
            number and `unit` is one of `m` (minutes), `h` (hours), `d` (days),
            `w` (weeks). Examples: `5m` for five minutes or `1d` for one day.
            Defaults to `1w`.

            This parameter defines the discretization level of the time series
            data for Trend Detection Analysis. As an example, setting this
            parameter to one week will result in the aggregation of data into
            one week windows for Trend Detection Analysis.
        :param aggregation_field: A numerical keyword field name to use
            as the base for trend detection
        :param aggregation_method: An aggregation method. Current options are
            'sum', 'avg', 'max' and 'min'. Defaults to 'avg'. Only used if
            aggregation_field is set too.
        :param aggregation_time_field: A datetime keyword field that is used
            as the timestamp for setting up trend detection instead. Defaults
            to `$item_created_at`.

        Example::

            >>> client.new_trenddetection(
                    project_id='2sic33jZTi-ifflvQAVcfw',
                    query='hello world',
                    name='test name',
                    email_user='test@squirro.com',
                    aggregation_interval='1w',
                    aggregation_field='votes',
                    aggregation_method='avg',
                    aggregation_time_field='my_datetime_facet'
                )
            {
                u'apiVersion': u'v0',
                u'data': {
                    u'created_at': u'2016-02-23T16:28:00',
                    u'id': u'iR81vxDnShu5di4snCu6Jg',
                    u'modified_at': u'2016-02-23T16:28:00',
                    u'name': u'test name',
                    u'project_id': u'2sic33jZTi-ifflvQAVcfw',
                    u'query': u'hello world'
                    u'aggregation_interval': u'1w',
                    u'aggregation_field': u'votes',
                    u'aggregation_method': u'avg',
                    u'aggregation_time_field': u'my_datetime_facet'
                }
                'deprecated': false,
                'id': '2c926905-cd53-4443-9524-420db741e721'
            }
        """
        url = self._get_trenddetection_base_url() % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
        })
        data = {'query': query, 'name': name, 'email_user': email_user,
                'aggregation_interval': aggregation_interval,
                'aggregation_field': aggregation_field,
                'aggregation_method': aggregation_method,
                'aggregation_time_field': aggregation_time_field}

        headers = {
            'Accept': 'application/json', 'Content-Type': 'application/json'}
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201])

    def get_trenddetections(self, project_id):
        """Get details of all the trend detections on a particular project.

        :param project_id: Id of the project.
        :returns: A dictionary with all the Trend Detection Entities.

        Example::

            >>> client.get_trenddetections(project_id='2sic33jZTi-ifflvQAVcfw')
                {
                    u'apiVersion': u'v0',
                    u'data': {
                        u'trend_detection_entities': [
                            {
                                u'created_at': '2016-02-09T08:34:17',
                                u'id': 'nwBnJ5tkQVGMjKFUBZ1Cbw',
                                u'modified_at': '2016-02-09T08:34:19',
                                u'name': 'test_tde',
                                u'project_id': 'oFFPR28pTUOkmUF8pZO0cA',
                                u'query': '',
                                u'aggregation_interval': u'1w',
                                u'aggregation_field': u'votes',
                                u'aggregation_method': u'avg',
                                u'aggregation_time_field': u'my_datetime_facet'
                            }
                        ]
                    },
                    'deprecated': false,
                    'id': '2c926905-cd53-4443-9524-420db741e721'
                }
        """
        url = self._get_trenddetection_base_url() % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
        })

        headers = {'Accept': 'application/json'}
        res = self._perform_request('get', url, headers=headers)
        return self._process_response(res)

    def get_trenddetection(self, project_id, trenddetection_id):
        """Get details for a particular trend detection entity.

        :param project_id: Id of the project.
        :param trenddetection_id: Trend Detection identifier.
        :returns: A dictionary with the requested Trend Detection Entity.

        Example::

            >>> client.get_trenddetection(project_id='oFFPR28pTUOkmUF8pZO0cA',
                                          trenddetection_id='nwBnJ5tkQVGMjKFUBZ1Cbw')
            {
                u'apiVersion': u'v0',
                u'data': {
                    u'created_at': u'2016-02-09T08:34:17',
                    u'id': u'nwBnJ5tkQVGMjKFUBZ1Cbw',
                    u'modified_at': u'2016-02-09T08:34:19',
                    u'name': u'test name',
                    u'project_id': u'oFFPR28pTUOkmUF8pZO0cA',
                    u'query': u'test_query',
                    u'aggregation_interval': u'1w',
                    u'aggregation_field': u'votes',
                    u'aggregation_method': u'avg',
                    u'aggregation_time_field': u'my_datetime_facet'
                },
                u'deprecated: false,
                u'id': u'f48a8c5d-5150-456d-9592-51b5c2cd41e4'
            }
        """
        url = self._get_trenddetection_base_url(trenddetection_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'trenddetection_id': trenddetection_id,
        })

        headers = {'Accept': 'application/json'}
        res = self._perform_request('get', url, headers=headers)
        return self._process_response(res)

    def delete_trenddetection(self, project_id, trenddetection_id):
        """Delete a particular Trend Detection Entity.

        :param project_id: Id of the project.
        :param trenddetection_id: Trend detection identifier.

        Example::

            >>> client.delete_trenddetection(project_id='2sic33jZTi-ifflvQAVcfw',
                                             trenddetection_id='fd5x9NIqQbyBmF4Yph9MMw')
        """
        url = self._get_trenddetection_base_url(trenddetection_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'trenddetection_id': trenddetection_id,
        })
        res = self._perform_request('delete', url)
        return self._process_response(res, [204])

    def get_trenddetection_predictions(self, project_id, trenddetection_id):
        """Get the predictions for a particular Trend Detection Entity.

        :param project_id: Id of the project.
        :param trenddetection_id: Trend detection identifier.
        :returns: A list of dict containing future predictions and the
            corresponding thresholds

        Example::

            >>> client.get_trenddetection_predictions(project_id='2sic33jZTi-ifflvQAVcfw',
                                                      trenddetection_id='fd5x9NIqQbyBmF4Yph9MMw')
                {
                    u'apiVersion': u'v0',
                    u'data': {
                        u'predictions': [
                            {
                                'prediction_threshold': 12,
                                'prediction_value': 14,
                                'timestamp': '2016-05-30T09:00:00'
                            },
                            {
                                'prediction_threshold': 14,
                                'prediction_value': 16,
                                'timestamp': '2016-05-30T12:00:00'
                            },
                            {
                                'prediction_threshold': 18,
                                'prediction_value': 29,
                                'timestamp': '2016-05-30T15:00:00'
                            },
                            {
                                'prediction_threshold': 22,
                                'prediction_value': 26,
                                'timestamp': '2016-05-30T18:00:00'
                            }
                        ]
                    },
                    'deprecated': false,
                    'id': '2c926905-cd53-4443-9524-420db741e721'
                }
        """
        url = self._get_trenddetection_base_url(trenddetection_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'trenddetection_id': trenddetection_id,
        })

        # URL for predictions
        url = url + '/predictions'

        # headers
        headers = {'Accept': 'application/json'}

        res = self._perform_request('get', url, headers=headers)
        return self._process_response(res, [200])

    # TODO: remove the redundant methods:
    # `get_trenddetection_thresholds`, `get_trenddetection_labels`,
    # `get_trenddetection_predictions`
    def get_trenddetection_result(self, project_id, trenddetection_id,
                                  result_before=None, result_after=None,
                                  include_thresholds=True,
                                  include_anomalies=True,
                                  include_historical_data=True,
                                  include_trend_detection_entity=True,
                                  include_predictions=False):
        """
        Returns predictions, anomalies, thresholds and the underlying data
        values of a trend detection entity.

        :param project_id: Id of the project
        :param trenddetection_id: Id of the trend detection entity
        :param result_before: Timestamp to determine the last time bucket to
            be fetched for trend-results
        :param result_after: Timestamp to determine the first time bucket to be
            fetched for trend-results
        :param include_thresholds: Flag to determine whether to include
            thresholds or not, defaults to True
        :param include_anomalies: Flag to determine whether to include
            anomalies or not, defaults to True
        :param include_historical_data: Flag to determine whether to include
            historical data or not, defaults to True
        :param include_trend_detection_entity: Flag to determine whether to
            include the trend-detection entity or not, defaults to True
        :param include_predictions: Flag to determine whether to include
            predictions or not, defaults to False

        :return: A dict of the trend detection entity, its underlying data
            values, its calculated threshold, anomalies and predictions.

        Example::

            >>> client.get_trenddetection_result(project_id='2sic33jZTi-ifflvQAVcfw',
                                                 trenddetection_id='fd5x9NIqQbyBmF4Yph9MMw',
                                                 include_predictions=True)

                {
                    'thresholds': [
                        {u'count': 18.709624304, u'timestamp': u'2016-01-25T00:00:00'},
                        {u'count': 17.6339240561, u'timestamp': u'2016-02-01T00:00:00'},
                        {u'count': 16.6033921677, u'timestamp': u'2016-02-08T00:00:00'},
                        {u'count': 17.5181532055, u'timestamp': u'2016-02-15T00:00:00'}
                    ],
                    'historical_values': {
                        u'values': [
                            {u'value': 18, u'key': u'2016-01-25T00:00:00'},
                            {u'value': 5, u'key': u'2016-02-01T00:00:00'},
                            {u'value': 7, u'key': u'2016-02-08T00:00:00'},
                            {u'value': 4, u'key': u'2016-02-15T00:00:00'}],
                        u'interval_seconds': 604800.0,
                        u'interval_logical': False},
                     'tde': {
                        u'aggregation_time_field': u'$item_created_at',
                        u'aggregation_field': None,
                        u'name': u'test_client',
                        u'created_at': u'2016-05-04T09:03:55',
                        u'modified_at': u'2016-05-04T09:03:58',
                        u'aggregation_interval': u'1w',
                        u'aggregation_method': None,
                        u'query': u'',
                        u'project_id': u'ZjI9KK3zRTaMkYSzUL6Ehw',
                        u'id': u'lsXDwwErQkq7dGKDaRopQQ'
                    },
                    'anomalies': [u'2016-01-25T00:00:00'],
                    'predictions': [
                        {
                            u'timestamp': u'2016-02-22T00:00:00',
                            u'prediction_value': 8.3735121811,
                            u'prediction_threshold': 11.5988725339
                        },
                        {
                            u'timestamp': u'2016-02-29T00:00:00',
                            u'prediction_value': 11.8071893366,
                            u'prediction_threshold': 13.011517576
                        },
                        {
                            u'timestamp': u'2016-03-07T00:00:00',
                            u'prediction_value': 6.4798976922,
                            u'prediction_threshold': 11.8167726387
                        }
                    ]
                }
        """

        # UTC -- time format
        # TODO: Remove this hardcoded time-format once the trends-service start
        # storing the historical data also as this will not be needed anymore
        time_format = '%Y-%m-%dT%H:%M:%S'

        # return type
        ret = {}

        # TODO: combine some of these requests on the topic api level
        # include tde if asked for
        if include_trend_detection_entity:
            tde = self.get_trenddetection(project_id, trenddetection_id)\
                .get('data', {})
            ret['tde'] = tde

        # include thresholds if asked for
        if include_thresholds:
            thresholds = self.get_trenddetection_thresholds(
                project_id, trenddetection_id, result_before, result_after).\
                get('data', {}).get('thresholds', {})
            ret['thresholds'] = thresholds

        # include anomalies if asked for
        if include_anomalies:
            anomalies = self.get_trenddetection_labels(
                project_id, trenddetection_id, result_before, result_after).\
                get('data', {}).get('labels', {})
            ret['anomalies'] = anomalies

        # include predictions if asked for
        if include_predictions:
            predictions = self.get_trenddetection_predictions(
                project_id, trenddetection_id).get('data', {}). \
                get('predictions', {})

            ret['predictions'] = predictions

        # TODO: remove the logic for getting the historical data once the
        # trends-service store the historical data itself
        # get first & last timestamp of thresholds data, in order to filter the
        # historical data with the same time stamps
        if include_historical_data:
            tde = self.get_trenddetection(project_id, trenddetection_id)\
                .get('data', {})
            thresholds = self.get_trenddetection_thresholds(
                project_id, trenddetection_id, result_before, result_after).\
                get('data', {}).get('thresholds', {})

            # return empty historical data if we get back no thresholds data
            if len(thresholds) < 2:
                ret['historical_values'] = []

            else:
                interval = \
                    (datetime.strptime(thresholds[1].get('timestamp'), time_format) -
                     datetime.strptime(thresholds[0].get('timestamp'), time_format)). \
                    total_seconds()

                historical_data_first_bucket = thresholds[0].get('timestamp')
                historical_data_last_bucket = \
                    datetime.strptime(thresholds[-1].get('timestamp'), time_format) + \
                    timedelta(seconds=interval-1)
                historical_data_last_bucket = \
                    historical_data_last_bucket.strftime(time_format)

                # prepare params for fetching historical data
                time_field = tde.get('aggregation_time_field')
                if not time_field:
                    time_field = '$item_created_at'

                aggregation = {
                    'trend_detection_values': {
                        'fields': [time_field],
                        'interval': tde.get('aggregation_interval'),
                        'method': 'histogram',
                        'min_doc_count': 0
                    }
                }

                aggregation_field = tde.get('aggregation_field')
                aggregation_method = tde.get('aggregation_method')
                if aggregation_field and aggregation_method:
                    innerAggregation = {
                        'fields': [aggregation_field],
                        'method': aggregation_method
                    }
                    aggregation['trend_detection_values']['aggregation'] = \
                        innerAggregation

                # query
                aggs = self.query(
                    project_id, query=tde.get('query'),
                    aggregations=aggregation, count=0,
                    created_before=historical_data_last_bucket,
                    created_after=historical_data_first_bucket)\
                    .get('aggregations', {})

                tds_aggs = aggs.get('trend_detection_values', {}).get(time_field)
                ret['historical_values'] = tds_aggs

                if not tds_aggs:
                    raise ValueError(
                        'Could not retrieve trend detection historical values')

        return ret

    def get_trenddetection_thresholds(self, project_id, trenddetection_id,
                                      thresholds_before=None,
                                      thresholds_after=None):
        """Get the thresholds for a particular Trend Detection Entity.

        :param project_id: Id of the project.
        :param trenddetection_id: Trend detection identifier.
        :param thresholds_before: Timestamp to determine the last time bucket
            of thresholds to be fetched for a particular trend detection entity
        :param thresholds_after: Timestamp to determine the first time bucket
            of thresholds to be fetched for a particular trend detection entity
        :returns: A dictionary of timestamps and corresponding thresholds

        Example::

            >>> client.get_trenddetection_thresholds(project_id='2sic33jZTi-ifflvQAVcfw',
                                                     trenddetection_id='fd5x9NIqQbyBmF4Yph9MMw')
                {
                    u'apiVersion': u'v0',
                    u'data': {
                        u'thresholds': [
                            {'count': 4.7645628705, 'timestamp': '2016-01-17T00:00:00'},
                            {'count': 4.5383389304, 'timestamp': '2016-01-18T00:00:00'},
                            {'count': 4.3557193335, 'timestamp': '2016-01-19T00:00:00'},
                            {'count': 4.4177192207, 'timestamp': '2016-01-20T00:00:00'},
                            {'count': 4.4954732238, 'timestamp': '2016-01-21T00:00:00'},
                            {'count': 4.6123319275, 'timestamp': '2016-01-22T00:00:00'},
                            {'count': 4.0773453641, 'timestamp': '2016-01-23T00:00:00'},
                            {'count': 4.2012054441, 'timestamp': '2016-01-24T00:00:00'},
                            {'count': 4.1041502018, 'timestamp': '2016-01-25T00:00:00'},
                        ]
                    },
                    'deprecated': false,
                    'id': '2c926905-cd53-4443-9524-420db741e721'
                }
        """
        url = self._get_trenddetection_base_url(trenddetection_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'trenddetection_id': trenddetection_id,
        })

        # url for thresholds
        url = url + '/thresholds'

        # headers
        headers = {'Accept': 'application/json'}

        # params
        params = {
            'thresholds_before': thresholds_before,
            'thresholds_after': thresholds_after}

        res = self._perform_request('get', url, params=params, headers=headers)
        return self._process_response(res, [200])

    def get_trenddetection_labels(self, project_id, trenddetection_id,
                                  labels_before=None, labels_after=None):
        """Get the labels for a particular Trend Detection Entity.

        :param project_id: Id of the project.
        :param trenddetection_id: Trend detection identifier.
        :param labels_before: Timestamp to determine the last time bucket of
            labels to be fetched for a particular trend detection entity
        :param labels_after: Timestamp to determine the first time bucket of
            labels to be fetched for a particular trend detection entity
        :returns: A list of all the timestamps where a trend has been detected.

        Example::

            >>> client.get_trenddetection_labels(project_id='2sic33jZTi-ifflvQAVcfw',
                                                 trenddetection_id='fd5x9NIqQbyBmF4Yph9MMw')
                {
                    u'apiVersion': u'v0',
                    u'data': {
                        'labels': [
                            '2014-09-28T00:00:00',
                            '2014-11-08T00:00:00',
                            '2014-12-19T00:00:00',
                            '2015-01-04T00:00:00',
                            '2015-02-05T00:00:00',
                            '2015-03-01T00:00:00',
                            '2015-03-07T00:00:00',
                            '2015-03-16T00:00:00',
                            '2015-05-02T00:00:00',
                            '2015-05-14T00:00:00',
                            '2015-05-28T00:00:00',
                            '2015-06-19T00:00:00',
                            '2015-07-03T00:00:00',
                            '2015-07-20T00:00:00',
                            '2015-08-28T00:00:00',
                            '2015-10-03T00:00:00',
                            '2015-10-12T00:00:00',
                            '2015-12-14T00:00:00',
                            '2016-01-05T00:00:00'
                        ]
                    },
                    'deprecated': false,
                    'id': '2c926905-cd53-4443-9524-420db741e721'
                }
        """
        url = self._get_trenddetection_base_url(trenddetection_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'trenddetection_id': trenddetection_id,
        })

        # url for labels
        url = url + '/labels'

        # headers
        headers = {'Accept': 'application/json'}

        # params
        params = {'labels_before': labels_before, 'labels_after': labels_after}

        res = self._perform_request('get', url, headers=headers, params=params)
        return self._process_response(res, [200])

    def _get_trenddetection_base_url(self, trenddetection_id=None):
        """Returns the URL template for a trend detection. """
        parts = ['%(ep)s/v0/%(tenant)s']
        parts.append('/projects/%(project_id)s/trenddetections')

        if trenddetection_id:
            parts.append('/%(trenddetection_id)s')

        return ''.join(parts)

    #
    # Fingerprint
    #

    def get_project_fingerprints(self, project_id, tags=None,
                                 include_config=False):
        """Get all fingerprints which are applicable on a object.

        :param project_id: Project identifier.
        :param tags: List of tags which can be used to
            filtering the returned fingerprints.
        :param include_config: Boolean flag whether to include each
            Smart Filter config.
        :returns: A list of fingerprints.

        Example::

            >>> client.get_project_fingerprints('zgxIdCxSRWSwJzL1fwNX1Q')
            []
        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/fingerprints'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        params = {}
        if tags is not None:
            params['tags'] = json.dumps(tags)
        if include_config:
            params['include_config'] = True

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def get_fingerprint(self, type, type_id, name):
        """Get a single fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :returns: Fingerprint information in a dictionary.

        Example::

            >>> client.get_fingerprint('object', 'zgxIdCxSRWSwJzL1fwNX1Q', 'default')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        res = self._perform_request('get', url)
        return self._process_response(res, [200])

    def get_project_fingerprint_scores(self, project_id, tags, object_id=None,
                                       fields=None):
        """Get the fingerprint scores for all items contained in the specified
        project. One ore more fingerprints are selected by specifying tags.

        :param project_id: Project identifier.
        :param tags: List of tags.
        :param object_id: Identifier of the object.
        :param fields: String of comma-separated item fields to include in the
            result.
        :returns: A list of fingerprint score entries.

        Example::

            >>> client.get_project_fingerprint_scores('Sz7LLLbyTzy_SddblwIxaA', ['poc', 'testing'])
            [{u'fingerprint': {u'filter_min_score': None,
                               u'name': u'ma',
                               u'title': u'',
                               u'type': u'tenant',
                               u'type_id': u'squirro'},
              u'scores': [{u'fields': {u'external_id': u'a38515'}, u'noise_level': 0.0},
                          {u'fields': {u'external_id': u'a37402'}, u'noise_level': 0.0},
                          {u'fields': {u'external_id': u'a38116'}, u'noise_level': 0.1}]},
             {u'fingerprint': {u'filter_min_score': 1.2950184,
                               u'name': u'something',
                               u'title': u'Something',
                               u'type': u'tenant',
                               u'type_id': u'squirro'},
              u'scores': [{u'fields': {u'external_id': u'a38515'}, u'noise_level': 0.0},
                          {u'fields': {u'external_id': u'a37402'}, u'noise_level': 0.1},
                          {u'fields': {u'external_id': u'a38116'}, u'noise_level': 0.1}]}]
        """
        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/scores'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        params = {'tags': json.dumps(tags)}

        if object_id is not None:
            params['object_id'] = object_id

        if fields is not None:
            params['fields'] = fields

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def validate_fingerprint_attributes(self, data):
        """Validates the attributes syntax of a fingerprint.

        :param data: Fingerprint attributes.

        Valid example::

            >>> data = {'config': {
                'manual_features': 'term1, 1.5, de, Term1\\nterm2, 2.4',
                'default_manual_features_lang': 'de'}}
            >>> client.validate_fingerprint_attributes(data)
            {}

        Invalid example::

            >>> data = {'config': {
                'manual_features': 'invalid, 1.5, de, Term1'}}
            >>> try:
            >>>     client.validate_fingerprint_attributes(data)
            >>> except squirro_client.exceptions.ClientError as e:
            >>>     print e.error
            u'[{"line": 0, "error": "required default language is missing"}]'
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/validate'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant})

        headers = {'Content-Type': 'application/json'}

        if data is None:
            data = {}

        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [200])

    def new_fingerprint(self, type, type_id, name=None, data=None):
        """Create a new fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param data: Fingerprint attributes.

        Example::

            >>> data = {'title': 'Earnings Call'}
            >>> client.new_fingerprint('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
            {}
        """
        if name:
            url = '%(ep)s/%(version)s/%(tenant)s'\
                  '/fingerprint/%(type)s/%(type_id)s/%(name)s'
        else:
            url = '%(ep)s/%(version)s/%(tenant)s'\
                  '/fingerprint/%(type)s/%(type_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        if data is None:
            data = {}

        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201])

    def copy_fingerprint(self, type, type_id, name):
        """Copies the fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.

        Example::

            >>> client.copy_fingerprint('tenant', 'squirro', 'ma')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/copy'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name
        })

        res = self._perform_request('post', url)
        return self._process_response(res, [201])

    def update_fingerprint_from_content(self, type, type_id, name, content):
        """Updates the fingerprint for the provided parameters from content
        data.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param content: Content data which is a list of dictionaries which
            contain the `lang` and `text` keys.

        Example::

            >>> data = [{'lang': 'en', 'text': 'english content'}]
            >>> client.update_fingerprint_from_content('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/content'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'post', url, data=json.dumps(content), headers=headers)
        return self._process_response(res, [204])

    def update_fingerprint_from_baseobject(self, type, type_id, name,
                                           baseobject):
        """Updates the fingerprint for the provided parameters from base object
        data.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param baseobject: List of base object identifiers.

        Example::

            >>> data = ['tK0W2Q8SR9uvSn3AlB9DLg']
            >>> client.update_fingerprint_from_baseobject('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/baseobject'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'post', url, data=json.dumps(baseobject), headers=headers)
        return self._process_response(res, [204])

    def update_fingerprint_from_items(self, type, type_id, name, items,
                                      negative=False):
        """Updates the fingerprint for the provided parameters from items
        data.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param items: List of item identifiers
        :param negative: Boolean, whether to add the items as 'negative' or
            'positive' training definitions. Defaults to False

        Example::

            >>> data = ['tfoOHGEZRAqFURaEE2cPWA']
            >>> client.update_fingerprint_from_items('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/items'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        data = {'item_ids': items, 'negative': negative}
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [204])

    def update_fingerprint_attributes(self, type, type_id, name, data):
        """Updates the fingerprint key-value attributes for the provided
        parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param data: Fingerprint attributes.

        Example::

            >>> data = {'title': 'Earnings Call'}
            >>> client.update_fingerprint_attributes('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [200])

    def delete_fingerprint(self, type, type_id, name):
        """Deletes the fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.

        Example::

            >>> client.delete_fingerprint('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default')
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    def move_fingerprint(self, type, type_id, name, target_name):
        """Moves the fingerprint for the provided parameters.

        This saves the fingerprint and removes the `temporary` flag. The old
        fingerprint is not removed.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param target_name: Name of move target fingerprint.

        Example::

            >>> client.move_fingerprint('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default')
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/move'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        data = {'target_name': target_name}
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201])

    def protect_fingerprint(self, type, type_id, name, locked):
        """Sets the locked state of a fingerprint.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param locked: Boolean flag to either lock or unlock the fingerprint.

        Example::

            >>> client.protect_fingerprint('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', True)
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/protection'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        data = {'locked': bool(locked)}
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [200])

    def get_fingerprint_matches_for_query(self, type, type_id, name,
                                          language, noise_level=0.1, **kwargs):
        """Returns the match counts for each feature of fingerprint with
        `type`, `type_id` and `name` and the query provide in kwargs.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type id.
        :param name: Fingerprint name.
        :param language: Language for which the matches are being returned.
        :param noise_level: Fingerprint noise_level.
        :param kwargs: Query parameters. All keyword arguments are passed on
            verbatim to the API. See the [[Items#List Items|List Items]]
            resource for all possible parameters.
        :returns: A dictionary which contains the matching feature and counts
            for the query.
        """
        project_id = kwargs.get('project_id')
        assert project_id
        del kwargs['project_id']

        # overwrite some query parameters to get the fingerprint matches
        kwargs['fingerprint_type'] = type
        kwargs['fingerprint_type_id'] = type_id
        kwargs['fingerprint_name'] = name
        kwargs['fingerprint_language'] = language
        kwargs['noise_level'] = noise_level
        kwargs['facet_fields'] = 'fingerprint_matches'
        kwargs['keyword_facets'] = False
        kwargs['enable_query_highlighting'] = False
        kwargs['count'] = 0
        kwargs['date_histogram'] = False
        kwargs['date_histogram_fields'] = None
        kwargs['highlight_smartfilters'] = None
        kwargs['fields'] = None

        res = self.get_items(project_id, **kwargs)
        matches = res.get('fingerprint_matches', {})
        return {'fingerprint_matches': matches}

    def delete_contributing_content_record(self, type, type_id, name,
                                           record_id, created_at=None):
        """Deletes a contributing content record and recalculates the
        fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param record_id: Contributing record identifier.
        :param created_at: Contributing record creation timestamp.

        Example::

            >>> client.delete_contributing_content_record('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', 'M2uyX6aUQVG2J2zcblSFHg')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/content/%(record_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name, 'record_id': record_id})

        params = {}
        if created_at is not None:
            params['created_at'] = created_at

        res = self._perform_request('delete', url, params=params)
        return self._process_response(res, [204])

    def update_contributing_content_record(self, type, type_id, name,
                                           record_id, content,
                                           created_at=None):
        """Updates a contributing content record and recalculates the
        fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param record_id: Contributing record identifier.
        :param content: Content data which is a dictionary which contains the
            `lang` and `text` keys.
        :param created_at: Contributing record creation timestamp.

        Example::

            >>> data = {'lang': 'en', 'text': 'updated english content'}
            >>> client.update_fingerprint_from_content('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', 'M2uyX6aUQVG2J2zcblSFHg', data, created_at='2013-07-01T14:08:23')
            {}
         """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/content/%(record_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name, 'record_id': record_id})

        headers = {'Content-Type': 'application/json'}

        params = {}
        if created_at is not None:
            params['created_at'] = created_at

        res = self._perform_request(
            'put', url, params=params, data=json.dumps(content),
            headers=headers)
        return self._process_response(res, [204])

    def delete_contributing_baseobject_record(self, type, type_id, name,
                                              record_id, created_at=None):
        """Deletes a contributing base object record and recalculates the
        fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param record_id: Contributing record identifier.
        :param created_at: Contributing record creation timestamp.

        Example::

            >>> client.delete_contributing_baseobject_record('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', 'sPOUuXqgSXqSllVkzheLvw')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s'\
              '/baseobject/%(record_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name, 'record_id': record_id})

        params = {}
        if created_at is not None:
            params['created_at'] = created_at

        res = self._perform_request('delete', url, params=params)
        return self._process_response(res, [204])

    def delete_contributing_items_record(self, type, type_id, name,
                                         record_id, created_at=None):
        """Deletes a contributing items record and recalculates the
        fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param record_id: Contributing record identifier.
        :param created_at: Contributing record creation timestamp.

        Example::

            >>> client.delete_contributing_items_record('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', '0L5jwLdfTJWRcTFMtBzhGg')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/items/%(record_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name, 'record_id': record_id})

        params = {}
        if created_at is not None:
            params['created_at'] = created_at

        res = self._perform_request('delete', url, params=params)
        return self._process_response(res, [204])

    #
    # Tasks
    #

    def get_tasks(self):
        """Return a list of all scheduled tasks for the current user."""
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_task(self, task_id):
        """Return details for a scheduled task.

        :param task_id: Task identifier.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks/%(task_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'task_id': task_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def create_task(self, **params):
        """Create a scheduled task. All parameters are passed on as attributes
        to create.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
        })
        res = self._perform_request('post', url, data=json.dumps(params),
                                    headers={'Content-Type': 'application/json'})
        return self._process_response(res, [201])

    def update_task(self, task_id, **params):
        """Update a scheduled task. All parameters are passed on as attributes
        to update.

        :param task_id: Task identifier.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks/%(task_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'task_id': task_id,
        })
        res = self._perform_request('put', url, data=json.dumps(params),
                                    headers={'Content-Type': 'application/json'})
        return self._process_response(res)

    def delete_task(self, task_id):
        """Delete a scheduled task.

        :param task_id: Task identifier.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks/%(task_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'task_id': task_id,
        })
        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    #
    # Tasks
    #

    def get_projects(self):
        """Return all projects.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/projects' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    #
    # Dashboards
    #

    def get_dashboards(self, project_id):
        """Return all dashboard for the given project.

        :param project_id: Project identifier

        :returns: A list of dashboard dictionaries.

        Example::

            >>> client.get_dashboards('2aEVClLRRA-vCCIvnuEAvQ')
            [{u'id': u'G0Tm2SQcTqu2d4GvfyrsMg',
              u'search': {u'query': u'Test'},
              u'title': u'Test',
              u'type': u'dashboard',
              u'widgets': [{u'col': 1,
                            u'id': 1,
                            u'row': 1,
                            u'size_x': 1,
                            u'size_y': 1,
                            u'title': u'Search Results',
                            u'type': u'Search'}]}]
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboards' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_dashboard(self, project_id, dashboard_id):
        """Return a specific dashboard from the given project.

        :param project_id: Project identifier
        :param dashboard_id: Dashboard identifier

        :returns: A dictionary of the given dashboard.

        Example::

            >>> client.get_dashboard('2aEVClLRRA-vCCIvnuEAvQ', 'G0Tm2SQcTqu2d4GvfyrsMg')
            {u'id': u'G0Tm2SQcTqu2d4GvfyrsMg',
             u'search': {u'query': u'Test'},
             u'title': u'Test',
             u'type': u'dashboard',
             u'theme_id': u'G0Tm2SQcTqu2d4GvfyrsMg',
             u'widgets': [{u'col': 1,
                           u'id': 1,
                           u'row': 1,
                           u'size_x': 1,
                           u'size_y': 1,
                           u'title': u'Search Results',
                           u'type': u'Search'}]}
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboards/%(dashboard_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'dashboard_id': dashboard_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def new_dashboard(self, project_id, title, search=None, type=None,
                      widgets=None, column_count=None, row_height=None,
                      theme_id=None, hide_title=None, reset_placement=None):
        """Create a new dashboard.

        :param project_id: Project identifier
        :param title: Dashboard title
        :param search: Search parameters for the dashboard
        :param widgets: Widgets shown on the dashboard
        :param type: Dashboard type (`dashboard` or `result`). The latter is
            used for the chart view in the UI and not displayed as a dashboard
            tab.
        :param column_count: Number of columns on this dashboard. Used by
            the frontend to render the widgets in the correct size.
        :param row_height: Height in pixels of each row on this dashboard. Used
            by the frontend to render the widgets in the correct size.
        :param theme_id: Dashboard theme identifier
        :param hide_title: Boolean, whether to hide the dashboard title when
            shared
        :param reset_placement: Position of the filter reset flyout, either
            `left` or `right` is supported


        :returns: A list of dashboard dictionaries.

        Example::

            >>> client.new_dashboard('2aEVClLRRA-vCCIvnuEAvQ', title='Sample')
            {
                u'widgets': None,
                u'search': None,
                u'type': u'dashboard',
                u'id': u'YagQNSecR_ONHxwBmOkkeQ',
                u'title': u'Sample',
                u'theme_id': u'G0Tm2SQcTqu2d4GvfyrsMg',
                u'hide_title': False,
                u'reset_placement': 'right',
            }
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboards' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
        })
        data = {
            'title': title,
            'search': search,
            'type': type,
            'widgets': widgets,
        }
        if column_count:
            data['column_count'] = column_count
        if row_height:
            data['row_height'] = row_height
        if theme_id:
            data['theme_id'] = theme_id
        if hide_title:
            data['hide_title'] = hide_title
        if reset_placement:
            data['reset_placement'] = reset_placement
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201])

    def modify_dashboard(self, project_id, dashboard_id, title=None,
                         search=None, widgets=None, type=None,
                         column_count=None, row_height=None, theme_id=None,
                         hide_title=None, reset_placement=None):
        """Update a dashboard.

        :param project_id: Project identifier
        :param dashboard_id: Dashboard identifier
        :param title: Dashboard title
        :param search: Search parameters for the dashboard
        :param widgets: Widgets shown on the dashboard
        :param type: Dashboard type
        :param column_count: Number of columns on this dashboard. Used by
            the frontend to render the widgets in the correct size.
        :param row_height: Height in pixels of each row on this dashboard. Used
            by the frontend to render the widgets in the correct size.
        :param theme_id: Associated theme id
        :param hide_title: Boolean, whether to hide the dashboard title when
            shared
        :param reset_placement: Position of the filter reset flyout, either
            `left` or `right` is supported

        :returns: A dictionary of the updated dashboard.

        Example::

            >>> client.modify_dashboard('2aEVClLRRA-vCCIvnuEAvQ', 'YagQNSecR_ONHxwBmOkkeQ', search={'query': 'Demo'})
            {
                u'widgets': None,
                u'search': {u'query': u'Demo'},
                u'type': u'dashboard',
                u'id': u'YagQNSecR_ONHxwBmOkkeQ',
                u'title': u'Sample',
                u'theme_id': u'GIHU8w_USBuAE3gqkMhuaA',
                u'hide_title': False,
                u'reset_placement': 'right',
            }
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboards/%(dashboard_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'dashboard_id': dashboard_id,
        })
        data = {
            'title': title,
            'search': search,
            'type': type,
            'widgets': widgets,
            'column_count': column_count,
            'row_height': row_height,
            'theme_id': theme_id,
            'hide_title': hide_title,
            'reset_placement': reset_placement,
        }
        post_data = {}
        for key, value in data.iteritems():
            if value is not None:
                post_data[key] = value
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'put', url, data=json.dumps(post_data), headers=headers)
        return self._process_response(res)

    def move_dashboard(self, project_id, dashboard_id, after):
        """Move a dashboard.

        :param project_id: Project identifier
        :param dashboard_id: Dashboard identifier
        :param after: The dashboard identifier after which the dashboard should
            be moved. Can be `None` to move the dashboard to the beginning
            of the list.

        :returns: No return value.

        Example::

            >>> client.move_dashboard('2aEVClLRRA-vCCIvnuEAvQ', 'Ue1OceLkQlyz21wpPqml9Q', 'nJXpKUSERmSgQRjxX7LrZw')
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboards/%(dashboard_id)s/move' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'dashboard_id': dashboard_id,
        })
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'post', url, data=json.dumps({'after': after}), headers=headers)
        return self._process_response(res, [204])

    def delete_dashboard(self, project_id, dashboard_id):
        """Delete a specific dashboard from the given project.

        :param project_id: Project identifier
        :param dashboard_id: Dashboard identifier

        :returns: No return value.

        Example::

            >>> client.delete_dashboard('2aEVClLRRA-vCCIvnuEAvQ', 'Ue1OceLkQlyz21wpPqml9Q')
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboards/%(dashboard_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'dashboard_id': dashboard_id,
        })
        res = self._perform_request('delete', url)
        return self._process_response(res, [204])

    #
    # Dashboard Themes
    #

    def get_dashboard_themes(self, project_id):
        """Return all dashboard themes for the given project.

        :param project_id: Project identifier

        :returns: A list of dashboard theme dictionaries.

        Example::

            >>> client.get_dashboard_themes('2aEVClLRRA-vCCIvnuEAvQ')
            [{u'id': u'G0Tm2SQcTqu2d4GvfyrsMg',
              u'title': u'Test',
              u'scope': u'custom',
              u'definition': [{u'background': u'#ffffff',
                               u'titleColor': u'#525252',
                               .....}]}]
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboard_themes' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_dashboard_theme(self, project_id, theme_id):
        """Return a specific dashboard theme from the given project.

        :param project_id: Project identifier
        :param theme_id: Dashboard identifier

        :returns: A dictionary of the given dashboard theme.

        Example::

            >>> client.get_dashboard_theme('2aEVClLRRA-vCCIvnuEAvQ', 'G0Tm2SQcTqu2d4GvfyrsMg')
            {u'id': u'G0Tm2SQcTqu2d4GvfyrsMg',
             u'title': u'Test',
             u'scope': u'custom',
             u'definition': [{u'background': u'#ffffff',
                             u'titleColor': u'#525252',
                             .....}]}]
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboard_themes/%(theme_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'theme_id': theme_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def new_dashboard_theme(self, project_id, title, definition=None):
        """Create a new dashboard theme.

        :param project_id: Project identifier
        :param title: Theme title
        :param definition: Theme definition

        :returns: Location of new theme.

        Example::

            >>> client.new_dashboard_theme('2aEVClLRRA-vCCIvnuEAvQ', title='Sample')
            {u'id': u'G0Tm2SQcTqu2d4GvfyrsMg',
             u'title': u'Test',
             u'scope': u'custom',
             u'definition': [{u'background': u'#ffffff',
                             u'titleColor': u'#525252',
                             .....}]}]
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboard_themes' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
        })
        data = {
            'title': title,
            'definition': definition,
        }
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201])

    def modify_dashboard_theme(self, project_id, theme_id, title=None,
                               definition=None):
        """Update a dashboard theme.

        :param project_id: Project identifier
        :param dashboard_id: Dashboard identifier
        :param title: Dashboard title
        :param definition: Theme definition
        :param widgets: Widgets shown on the dashboard

        :returns: A dictionary of the updated dashboard.

        Example::

            >>> client.modify_dashboard_theme('2aEVClLRRA-vCCIvnuEAvQ', 'YagQNSecR_ONHxwBmOkkeQ', title='New Title')
            {
                u'id': u'YagQNSecR_ONHxwBmOkkeQ',
                u'title': u'New Title',
                u'definition': [{u'background': u'#ffffff',
                                 u'titleColor': u'#525252',
                                 .....}]}]
            }
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboard_themes/%(theme_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'theme_id': theme_id,
        })
        data = {
            'title': title,
            'definition': definition,
        }
        post_data = {}
        for key, value in data.iteritems():
            if value is not None:
                post_data[key] = value
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'put', url, data=json.dumps(post_data), headers=headers)
        return self._process_response(res)

    def delete_dashboard_theme(self, project_id, theme_id):
        """Delete a specific dashboard theme from the given project.

        :param project_id: Project identifier
        :param theme_id: Theme identifier

        :returns: No return value.

        Example::

            >>> client.delete_dashboard_theme('2aEVClLRRA-vCCIvnuEAvQ', 'Ue1OceLkQlyz21wpPqml9Q')
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/dashboard_themes/%(theme_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'theme_id': theme_id,
        })
        res = self._perform_request('delete', url)
        return self._process_response(res, [204])

    #
    # Dashboard Custom Widgets
    #

    def get_dashboard_widgets(self):
        """Return all dashboard widgets (for tenant).

        :returns: A list of custom dashboard widgets dictionaries.

        Example::

            >>> client.get_dashboard_widgets()
            [{u'id': u'G0Tm2SQcTqu2d4GvfyrsMg',
              u'title': u'Test',
              u'scope': u'custom',
              u'definition': [{u'background': u'#ffffff',
                               u'titleColor': u'#525252',
                               .....}]}]
        """
        url = '%(ep)s/v0/%(tenant)s/widgets' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_dashboard_widget(self, name):
        """Return a specific custom dashboard widget.

        :param name: Name of custom widget (in current tenant)

        :returns: A dictionary of the named custom widget.

        Example::

            >>> client.get_dashboard_widget('map_us')
            {u'id': u'G0Tm2SQcTqu2d4GvfyrsMg',
             u'title': u'Test',
             u'scope': u'custom',
             u'definition': [{u'background': u'#ffffff',
                             u'titleColor': u'#525252',
                             .....}]}]
        """
        url = '%(ep)s/v0/%(tenant)s/widgets/%(name)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'name': name,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def new_dashboard_widget(self, config):
        """Upload a new custom widget to squirro
        :param config: properties that require at least the `directory`
                       to be specified where the custom widget code
                       resides. Optional properties are `base_widget`
                       a builtin widget whose widget attributes to
                       inherit and `friendly_name` to be used in the
                       user interface. All properties other than
                       `directory` are passed on to the backend
                       in the widget.ini file unless widget.ini
                       already exists. The `name` and `hash` properties are
                       reserved for internal use.

        Example::

            >>> client.new_dashboard_widget(
            >>>     config={u'directory': u'/home/us_map',
            >>>             u'base_widget': u'world_map',
            >>>             u'friendly_name': u'Map of the USA'})
        """
        if config is None or not config.has_key(u'directory'):
            raise ValueError('Config needs to include directory: "%r"', config)
        directory = config[u'directory'].rstrip('/')
        widget_ini = os.path.join(directory, 'widget.ini')
        name = os.path.basename(directory)

        if not name.replace('_', '').replace('-', '').isalnum():
            raise ValueError('The directory name "' + name + '" in config ' +
                             'needs to be alphanumeric or can contain - or _' +
                             '. Please rename the directory.')

        # move any pre-existing widget_ini file (from a previous upload
        # attempt) aside.
        if os.path.exists(widget_ini):
            os.rename(widget_ini, widget_ini + '.orig')

        with open(widget_ini, 'w') as widget_config:
            widget_config.writelines(['[widget]\n'])
            for key, value in config.iteritems():
                if key == u'directory':
                    continue
                elif key in [u'name', u'hash']:
                    raise ValueError('Reserved "' + key +
                                     '" property in config')
                widget_config.writelines([key + '=' + value + '\n'])
            widget_config.writelines(['hash = ' + str(uuid.uuid1()) + '\n'])

        try:
            binary_data = io.BytesIO()
            with tarfile.open(fileobj=binary_data, mode='w|gz') as tar:
                tar.add(directory, arcname=name, recursive=True)

            data = base64.b64encode(binary_data.getvalue())
            data_json = {
                'data': data,
            }
        except Exception as e:
            raise ValueError(e)

        headers = {'Content-Type': 'application/json'}
        url = '%(ep)s/v0/%(tenant)s/widgets/%(name)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'name': name,
        })
        res = self._perform_request(
            'post', url, data=json.dumps(data_json), headers=headers)
        return self._process_response(res, [201])

    #
    # Pipelets
    #

    def get_pipelets(self):
        """Return all available pipelets.

        These pipelets can be used for enrichments of type `pipelet`.

        :returns: A dictionary where the value for `pipelets` is a list of
            pipelets.

        Example::

            >>> client.get_pipelets()
            {u'pipelets': [{u'id': u'tenant01/textrazor', u'name': u'textrazor'}]}
        """
        url = '%(ep)s/v0/%(tenant)s/pipelets' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    #
    # Enrichments
    #

    def create_enrichment(self, project_id, type, name, config):
        """Create a new enrichment on the project.

        :param project_id: Project identifier. Enrichment will be created in
            this project.
        :param type: Enrichment type. Possible values: `pipelet`, `keyword`.
        :param name: The new name of the enrichment.
        :param config: The configuration of the new enrichment. This is an
            dictionary and the contents depends on the type.
        :returns: The new enrichment.

        Example::

            >>> client.create_enrichment('Sz7LLLbyTzy_SddblwIxaA', 'pipelet', 'TextRazor', {'pipelet': 'tenant-example/textrazor', 'api_key': 'TextRazor-API-Key'})
            {
                u'type': u'pipelet',
                u'config': {u'api_key': u'TextRazor-API-Key', u'pipelet': u'tenant-example/textrazor'},
                u'name': u'TextRazor',
                u'id': u'pipelet-rTBoGNl6S4aG4TDkBoN6xQ'
            }
        """
        data = {
            'type': type,
            'name': name,
            'config': config,
        }
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/enrichments' % ({
            'ep': self.topic_api_url,
            'project_id': project_id,
            'tenant': self.tenant,
        })
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201])

    def get_enrichments(self, project_id):
        """Return enrichments configured on this project.

        :param project_id: Project identifier. Enrichments are retrieved from
            this project.

        Example::

            >>> client.get_enrichments('Sz7LLLbyTzy_SddblwIxaA')
            [{
                u'type': u'pipelet',
                u'config': {u'api_key': u'TextRazor-API-Key', u'pipelet': u'tenant-example/textrazor'},
                u'name': u'TextRazor',
                u'id': u'pipelet-rTBoGNl6S4aG4TDkBoN6xQ'
            }]
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/enrichments' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_enrichment(self, project_id, enrichment_id):
        """Returns a single enrichment configured on this project.

        :param project_id: Project identifier. Enrichment must exist in this
            project.
        :param enrichment_id: Enrichment identifier.

        Example::

            >>> client.get_enrichment('Sz7LLLbyTzy_SddblwIxaA', 'pipelet-rTBoGNl6S4aG4TDkBoN6xQ'})
            {
                u'type': u'pipelet',
                u'config': {u'api_key': u'TextRazor-API-Key', u'pipelet': u'tenant-example/textrazor'},
                u'name': u'TextRazor',
                u'id': u'pipelet-rTBoGNl6S4aG4TDkBoN6xQ'
            }
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/enrichments/%(enrichment_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'enrichment_id': urllib.quote_plus(enrichment_id),
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def delete_enrichment(self, project_id, enrichment_id):
        """Delete a single enrichment configured on this project.

        :param project_id: Project identifier. Enrichment must exist in this
            project.
        :param enrichment_id: Enrichment identifier.

        Example::

            >>> client.delete_enrichment('Sz7LLLbyTzy_SddblwIxaA', 'pipelet-rTBoGNl6S4aG4TDkBoN6xQ')
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/enrichments/%(enrichment_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'enrichment_id': urllib.quote_plus(enrichment_id),
        })
        res = self._perform_request('delete', url)
        return self._process_response(res, [204])

    def update_enrichment(self, project_id, enrichment_id, type, name, config):
        """Update a single enrichment configured on this project.

        :param project_id: Project identifier. Enrichment must exist in this
            project.
        :param enrichment_id: Enrichment identifier.
        :param type: Enrichment type. Possible values: `pipelet`, `keyword`.
        :param name: The new name of the enrichment.
        :param config: The new configuration of the enrichment. This is an
            dictionary and the contents depends on the type.
        :returns: The modified enrichment.

        Example::

            >>> client.update_enrichment('Sz7LLLbyTzy_SddblwIxaA', 'pipelet-rTBoGNl6S4aG4TDkBoN6xQ', 'pipelet', 'TextRazor', {'pipelet': 'tenant-example/textrazor', 'api_key': 'New-Key'})
            {
                u'type': u'pipelet',
                u'config': {u'api_key': u'New-Key', u'pipelet': u'tenant-example/textrazor'},
                u'name': u'TextRazor',
                u'id': u'pipelet-rTBoGNl6S4aG4TDkBoN6xQ'
            }
        """
        data = {
            'type': type,
            'name': name,
            'config': config,
        }
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/enrichments/%(enrichment_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'enrichment_id': urllib.quote_plus(enrichment_id),
        })
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res)

    #
    # Facets
    #

    def get_facet(self, project_id, id):
        """Retrieves a facet of project `project_id`.

        :param project_id: Project identifier
        :param id: Facet identifier"""
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/facets/%(id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'id': id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_facets(self, project_id):
        """Retrieves all facets of project `project_id`.

        :param project_id: Project identifier"""
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/facets' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
        })
        res = self._perform_request('get', url)
        retval = self._process_response(res)
        if retval:
            retval = retval.get('facets')
        return retval

    def new_facet(self, project_id, name, data_type=None, display_name=None,
                  group_name=None, visible=None, format_instr=None,
                  searchable=None, typeahead=None):
        """Creates a new facet on project `project_id`.

        :param project_id: Project identifier
        :param name: Name of the facet in queries and on incoming items
        :param data_type: One of ('string', 'int', 'float', 'date')
        :param display_name: Name to show to the user in the frontend
        :param group_name: Label to group this facet under.
        :param visible: If `False` this facet will be hidden in the front-end
        :param format_instr: Formatting instruction for the facet value display.
        :param searchable: If 'True' this facet values will be searchable.
            Defaults to 'False' if not specified
        :param typeahead: If 'True' this facet values will be available for
            typeahead suggestions. Defaults to 'True' if not specified.

        """
        data = {
            'name': name,
            'data_type': data_type,
            'display_name': display_name,
            'visible': visible,
            'group_name': group_name,
            'format_instr': format_instr,
            'searchable': searchable,
            'typeahead': typeahead
        }
        data = dict([(k, v) for k, v in data.iteritems() if v is not None])

        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/facets' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
        })
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request('post', url, data=json.dumps(data),
                                    headers=headers)
        return self._process_response(res, [201])

    def modify_facet(self, project_id, id, display_name=None, group_name=None,
                     visible=None, format_instr=None, searchable=None,
                     typeahead=None, **kwargs):
        """Modifies a facet on project `project_id`.

        :param project_id: Project identifier
        :param id: Facet identifier
        :param display_name: Name to show to the user in the frontend
        :param group_name: Label to group this facet under.
        :param visible: If `False` this facet will be hidden in the front-end
        :param format_instr: Formatting instruction for the facet value display.
        :param searchable: If 'True' this facet values will be searchable.
        :param typeahead: If 'True' this facet values & name will be
            searchable.
        :param kwargs: Query parameters. All keyword arguments are passed on
            verbatim to the API. See the [[Facets#Update Facet|Update Facet]]
            resource for all possible parameters.
        """
        data = {
            'display_name': display_name,
            'visible': visible,
            'group_name': group_name,
            'format_instr': format_instr,
            'searchable': searchable,
            'typeahead': typeahead
        }
        data.update(**kwargs)
        data = dict([(k, v) for k, v in data.iteritems() if v is not None])

        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/facets/%(id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'id': id,
        })
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request('put', url, data=json.dumps(data),
                                    headers=headers)
        return self._process_response(res)

    def get_facet_stats(self, project_id, id):
        """Returns stats for a facet on project `project_id`.

        :param project_id: Project identifier
        :param id: Facet identifier

        Example::
            >>> client.get_facet_stats('Sz7LLLbyTzy_SddblwIxaA', 'da1d234f7e85c4edf37c3286ad7d4ea2c0c64ee8899a5219be21077214719d77'})
            {
                u'all_single_values': True
            }
        """
        url = '%(ep)s/v0/%(tenant)s/projects/%(project_id)s/facets/%(id)s/stats' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'project_id': project_id,
            'id': id,
        })
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request('get', url, headers=headers)
        return self._process_response(res)
