"""Interface for ObjectMeta objects."""

import collections.abc

import kube._error
import kube._util


class ObjectMeta:
    """Common metadata for API objects.

    :param resource: The object representing the Kubernetes resource which
       this metadata describes.
    """

    def __init__(self, resource):
        self._resource = resource

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self._resource.raw['metadata'] ==
                other._resource.raw['metadata'])
        else:
            return NotImplemented

    @property
    def name(self):
        """The name of the object."""
        return self._resource.raw['metadata']['name']

    @property
    def namespace(self):
        """Namespace the object resides in.

        :raises kube.StatusError: If the object is not in a namespace.
            For example, a :class:`kube.NamespaceResource` won't have a
            namespace.
        """
        if 'namespace' in self._resource.raw['metadata']:
            return self._resource.raw['metadata']['namespace']
        else:
            raise kube._error.StatusError

    @property
    def labels(self):
        """The labels as a :class:`ResourceLabels` instance."""
        return ResourceLabels(self._resource)

    @property
    def version(self):
        """The opaque resource version."""
        return self._resource.raw['metadata']['resourceVersion']

    @property
    def created(self):
        """The created timestamp."""
        return kube._util.parse_rfc3339(
            self._resource.raw['metadata']['creationTimestamp'])

    @property
    def link(self):
        """A link to the resource itself.

        This is currently an absolute URL without the hostname, but
        you don't have to care about that.  The
        :class:`kube.APIServerProxy` will be just fine with it as it's
        ``path`` argument.
        """
        return self._resource.raw['metadata']['selfLink']

    @property
    def uid(self):
        return self._resource.raw['metadata']['uid']


class ResourceLabels(collections.abc.Mapping):
    """The labels applied to an API resource.

    This allows introspecting the labels as a normal mapping and
    provides a few methods to directly manipulate the labels on the
    resource.
    """

    def __init__(self, resource):
        self._resource = resource

    def __getitem__(self, name):
        return self._resource.raw['metadata']['labels'][name]

    def __iter__(self):
        for key in self._resource.raw['metadata']['labels']:
            yield key

    def __len__(self):
        return len(self._resource.raw['metadata']['labels'])

    def set(self, key, value):
        """Set a (new) label.

        This will set or update the label's value on the resource.

        :returns: New instance of the resource.
        """
        new = self._resource.cluster.proxy.patch(
            self._resource.meta.link,
            patch={'metadata': {'labels': {key: value}}},
        )

    def delete(self, key):
        """Delete a label.

        This will remove the label for a given key from the resource.
        """
        new = self._resource.cluster.apiproxy.patch(
            self._resource.meta.link,
            patch={'metadata': {'labels': {key: None}}},
        )
        self._resource.raw = new

    def __dict__(self):
        return dict(self._resource.raw['metadata']['labels'])
