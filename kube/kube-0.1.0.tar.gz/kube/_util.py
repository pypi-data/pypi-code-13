"""Common utilities kube."""

import datetime
import json
import types

import kube._error


def parse_rfc3339(when):
    """Parse a RFC 3339 timestamp into a :class:`datetime.datetime`."""
    return datetime.datetime.strptime(when, '%Y-%m-%dT%H:%M:%SZ')


def fetch_resource(cluster, resource, name, namespace=None):
    """Return the single resource data.

    This method helps implement common functionality for the
    :meth:`kube.ViewABC.fetch` method.  In particular it handles 404 as
    aa :class:`LookupError`.

    .. warning::

       Take care not to use this without a namespace when the resource
       does not support this, as this will result in a
       :class:`KeyError` instead of :class:`kube.APIError`.

    :returns: The decoded JSON object of the resource.
    :raises LookupError: if the resource does not exist.
    :raises kube.APIError: for errors from the k8s API server.
    """
    try:
        if namespace:
            data = cluster.proxy.get('namespaces', namespace, resource, name)
        else:
            data = cluster.proxy.get(resource, name)
    except kube._error.APIError as exc:
        if exc.status_code == 404:
            raise LookupError('No such {} resource'.format(resource))
        else:
            raise
    else:
        return data


def filter_list(cluster, resource, selector, namespace=None):
    """Return an iterator for a resource restricted to the selector.

    This method helps implement common functionality for the
    :meth:`kube.ViewABC.filter` method.

    :param kube.Cluster cluster: The cluster instance.
    :param str resource: The resource name, defining the API server
       endpoint to use.
    :param dict selector: Dictionary of the labels to use as equality
       based selector.

    :returns: an iterator of decoded JSON objects of resources
       matching the selector.
    :raises ValueError: if an empty selector is used.
    :raises kube.APIError: for errors from the k8s API server.
    """
    if not selector:
        raise ValueError('No empty selector allowed')
    selector = ','.join('{}={}'.format(k, v) for k, v in selector.items())
    if namespace:
        data = cluster.proxy.get('namespaces', namespace,
                                 resource, labelSelector=selector)
    else:
        data = cluster.proxy.get(resource, labelSelector=selector)
    yield from data['items']


def thaw(obj):
    """Thaw an objct.

    The reverse of :func:`freeze`.
    """
    if isinstance(obj, tuple):
        return list(thaw(i) for i in obj)
    elif isinstance(obj, types.MappingProxyType):
        return dict({k: thaw(v) for k, v in obj.items()})
    else:
        return obj


class ImmutableJSONDecoder(json.JSONDecoder):
    """Decode JSON to immutable types."""

    @classmethod
    def freeze(cls, obj):
        """Recursively convert JSON-deocded objects to immutable types.

        Specifically JSON arrays are converted to tuples and objects are
        are wrapped in :class:`types.MappingProxyType`. When converting
        arrays and objects their contiuent values are also converted in a
        recursive fashion.

        :param obj: the object to convert to an immutable type.

        :return: the immutable equivalent of the given object.
        """
        if isinstance(obj, list):
            return tuple(cls.freeze(i) for i in obj)
        elif isinstance(obj, dict):
            return types.MappingProxyType({
                key: cls.freeze(value) for key, value in obj.items()})
        else:
            return obj

    def decode(self, string, *args, **kwargs):
        return self.freeze(super().decode(string, *args, **kwargs))
