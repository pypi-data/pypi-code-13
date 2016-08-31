# Copyright 2016 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
An **Adapter** object represents a single adapter for
a Dynamic Partition Manager-enabled (DPM) system.
Adapters on a z Systems or LinuxONE system fall into four categories:
Network, Storage, Accelerators, and Cryptos.
Each adapter type plays a specific role in communication, or data transfer,
for system partitions and the applications that run in them.
Objects of this class are not provided when the CPC is not in DPM mode.

An adapter is always contained in a CPC.
"""

from __future__ import absolute_import

from ._manager import BaseManager
from ._resource import BaseResource

__all__ = ['AdapterManager', 'Adapter']


class AdapterManager(BaseManager):
    """
    Manager object for Adapters. This manager object is scoped to the
    adapters of a particular CPC.

    Derived from :class:`~zhmcclient.BaseManager`; see there for common methods
    and attributes.
    """

    def __init__(self, cpc):
        """
        Parameters:

          cpc (:class:`~zhmcclient.Cpc`):
            CPC defining the scope for this manager object.
        """
        super(AdapterManager, self).__init__(cpc)

    @property
    def cpc(self):
        """
        :class:`~zhmcclient.Cpc`: Parent object (CPC) defining the scope for
        this manager object.
        """
        return self._parent

    def list(self, full_properties=False):
        """
        List the adapters in scope of this manager object.

        Parameters:

          full_properties (bool):
            Controls whether the full set of resource properties should be
            retrieved, vs. only the short set as returned by the list
            operation.

        Returns:

          : A list of :class:`~zhmcclient.Adapter` objects.

        Raises:

          :exc:`~zhmcclient.HTTPError`
          :exc:`~zhmcclient.ParseError`
          :exc:`~zhmcclient.AuthError`
          :exc:`~zhmcclient.ConnectionError`
        """
        cpc_uri = self.cpc.get_property('object-uri')
        adapters_res = self.session.get(cpc_uri + '/adapters')
        adapter_list = []
        if adapters_res:
            adapter_items = adapters_res['adapters']
            for adapter_props in adapter_items:
                adapter = Adapter(self, adapter_props['object-uri'],
                                  adapter_props)
                if full_properties:
                    adapter.pull_full_properties()
                adapter_list.append(adapter)
        return adapter_list

    def create_hipersocket(self, properties):
        """
        Create and configures a HiperSockets adapter
        with the specified resource properties.

        Parameters:

          properties (dict): Properties for the new adapter.

        Returns:

          string: The resource URI of the new adapter.

        Raises:

          :exc:`~zhmcclient.HTTPError`
          :exc:`~zhmcclient.ParseError`
          :exc:`~zhmcclient.AuthError`
          :exc:`~zhmcclient.ConnectionError`
        """
        cpc_uri = self.cpc.get_property('object-uri')
        result = self.session.post(cpc_uri + '/adapters', body=properties)
        return result['object-uri']


class Adapter(BaseResource):
    """
    Representation of an Adapter.

    Derived from :class:`~zhmcclient.BaseResource`; see there for common
    methods and attributes.
    """

    def __init__(self, manager, uri, properties):
        """
        Parameters:

          manager (:class:`~zhmcclient.AdapterManager`):
            Manager object for this resource.

          uri (string):
            Canonical URI path of the Adapter object.

          properties (dict):
            Properties to be set for this resource object.
            See initialization of :class:`~zhmcclient.BaseResource` for
            details.
        """
        assert isinstance(manager, AdapterManager)
        super(Adapter, self).__init__(manager, uri, properties)

    def delete_hipersocket(self):
        """
        Deletes this adapter if it is a hipersocket adapter.

        Raises:

          :exc:`~zhmcclient.HTTPError`
          :exc:`~zhmcclient.ParseError`
          :exc:`~zhmcclient.AuthError`
          :exc:`~zhmcclient.ConnectionError`
        """
        adapter_uri = self.get_property('object-uri')
        self.manager.session.delete(adapter_uri)

    def update_properties(self, properties):
        """
        Updates one or more of the writable properties of a adapter
        with the specified resource properties.

        Parameters:

          properties (dict): Updated properties for the adapter.

        Raises:

          :exc:`~zhmcclient.HTTPError`
          :exc:`~zhmcclient.ParseError`
          :exc:`~zhmcclient.AuthError`
          :exc:`~zhmcclient.ConnectionError`
        """
        adapter_uri = self.get_property('object-uri')
        self.manager.session.post(adapter_uri, body=properties)
