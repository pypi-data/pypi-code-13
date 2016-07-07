"""Tools to work with a Kubernetes cluster.

This module contains the toplevel tools to work with a Kubernets
cluster and it's API server.
"""

import collections
import enum
import json
import os
import urllib.parse

import requests

import kube
from kube import _namespace as namespace
from kube import _node as node
from kube import _pod as pod
from kube import _util as util


class Cluster:
    """A Kubernetes cluster.

    The entrypoint to control a Kubernetes cluster.  There is only one
    connection mechanism, which is via a local API server proxy.  This
    is normally achieved by running ``kubectl proxy``.

    :param url: The URL of the API server.

    :ivar proxy: A helper class to directly access the API server. An
        instance of :class:`kube.APIServerProxy` helper class.
    :ivar nodes: A :class:`kube.nodes.NodeList` instance.
    """

    def __init__(self, url='http://localhost:8001/api/'):
        if not url.endswith('/'):
            url += '/'
        api_url = urllib.parse.urljoin(url, 'v1/')
        self.proxy = APIServerProxy(api_url)
        self.namespaces = namespace.NamespaceView(self)
        self.nodes = node.NodeView(self)
        self.pods = pod.PodView(self)
        # self.rc = kube.rc.ReplicationControllerList(self)
        # self.svc = kube.svc.ServiceList(self)
        # self.secrets = kube.secrets.SecretList(self)
        # self.endpoints = kube.endpoints.EndpointList(self)
        # self.serviceaccounts = kube.serviceaccounts.ServiceAccountList(self)

    def close(self):
        """Close and clean up underlying resources."""
        self.proxy.close()

    def __enter__(self):
        return self

    def __exit__(self, exc, type_, tb):
        self.close()


class APIServerProxy:
    """Helper class to directly communicate with the API server.

    Since most classes need to communicate with the Kubernetes
    cluster's API server in a common way this class helps take care of
    the common logic.  It also keeps the requests session alive to
    enable connection pooling to the API server.

    :param base_url: The URL of the API, including the API version.
    """

    def __init__(self, base_url='http://localhost:8001/api/v1/'):
        if not base_url.endswith('/'):
            base_url += '/'
        self._base_url = base_url
        self._session = requests.Session()

    def close(self):
        """Close underlying connections.

        Once the proxy has been closed then the it can no longer be used
        to issue further requests.
        """
        self._session.close()

    def urljoin(self, *path):
        """Wrapper around urllib.parse.urljoin for self.baseurl.

        :param path: Individual relative path components, they will be
           joined using "/".  None of the path components should
           include a "/" separator themselves.
        """
        return urllib.parse.urljoin(self._base_url, '/'.join(path))

    def get(self, *path, **params):
        """HTTP GET the relative path from the API server.

        :param path: Individual relative path components, they will be
           joined using "/".  None of the path components should
           include a "/" separator themselves.

        :raises kube.APIError: If the response status is not 200 OK.
        :return: The decoded JSON data.
        """
        url = self.urljoin(*path)
        response = self._session.get(url, params=params)
        if response.status_code != 200:
            raise kube.APIError(response, 'Failed to GET {}:'.format(url))
        else:
            return response.json(cls=util.ImmutableJSONDecoder)

    def patch(self, *path, patch=None):
        """HTTP PATCH as application/strategic-merge-patch+json.

        This allows using the Strategic Merge Patch to patch a
        resource on the Kubernetes API server.

        :param path: Individual relative path components, they will be
           joined using "/".  None of the path components should
           include a "/" separator themselves, unless you only provide
           one component which will be joined to the base URL using
           :func:`urllib.parse.urljoin`.  This case can be useful to
           use the links provided by the API itself directly,
           e.g. from a resource's ``metadata.selfLink`` field.
        :param patch: The decoded JSON object with the patch data.

        :raises APIError: If the response status is not 200 OK.
        :returns: The decoded JSON object of the resource after
           applying the patch.
        """
        url = self.urljoin(*path)
        headers = {'Content-Type': 'application/strategic-merge-patch+json'}
        response = self._session.patch(url, headers=headers, json=patch)
        if response.status_code != 200:
            raise kube.APIError(response, 'Failed to PATCH {}:'.format(url))
        else:
            return response.json(cls=util.ImmutableJSONDecoder)

    def watch(self, *path, version):
        """Watch a resource for additions, updates and deletions.

        This issues a request to the API with the ``watch`` query string
        paramter set to ``true`` which returns a chunked response. An
        iterator is returned which continuously reads from the response,
        yielding :class:`WatchEvent`s.

        :param path: the URL path to the resource to watch. See
            :meth:`urljoin`.
        :param str version: the resource version to start watching from.

        :returns: an iterator of :class:`WatchEvent`s.
        """
        response = self._session.get(
            self.urljoin(*path),
            params={'watch': 'true', 'resourceVersion': version},
            stream=True,
        )
        for line in self._iter_response_lines(response):
            event_raw = json.loads(line, cls=util.ImmutableJSONDecoder)
            event_type = WatchEventType(event_raw['type'])
            event_object = event_raw['object']
            yield WatchEvent(event_type, event_object)

    @staticmethod
    def _iter_response_lines(response, chunk_size=1024):
        pending = None
        fd = response.raw.fileno()
        while True:
            chunk = os.read(fd, chunk_size)
            if not chunk:
                break
            if pending is not None:
                chunk = pending + chunk
                pending = None
            lines = chunk.splitlines()
            if lines[-1:] and chunk[-1:] != '\n':
                pending = lines.pop()
            yield from lines
        if pending:
            yield pending


class WatchEventType(enum.Enum):
    """Represents the type of watch event."""
    MODIFIED = 'MODIFIED'
    ADDED = 'ADDED'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


WatchEvent = collections.namedtuple('WatchEvent', ('type', 'object'))
WatchEvent.WatchEventType = WatchEventType
WatchEvent.__doc__ = """\
Represents an event generated from watching a resource.

:cvar WatchEventType: a convenience alias of :class:`WatchEventType`.

:ivar WatchEventType type: the type of event.
:ivar object: the object which is the subject of the event. At the lowest
    level this will be the raw, JSON-decoded object. However, higher-level
    abstractions may take its place.
"""
