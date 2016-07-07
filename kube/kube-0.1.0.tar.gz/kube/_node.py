"""Interface for Node and NodeList objects."""

import collections
import copy
import enum
import ipaddress

import kube._base
import kube._meta
import kube._util


class NodeView(kube._base.ViewABC):
    """All the cluster nodes.

    :param cluster: The :class:`kube.Cluster` instance which this node
       list must represent.

    :ivar cluster: The :class:`kube.Cluster` instance.
    """

    def __init__(self, cluster):
        self.cluster = cluster

    def __iter__(self):
        """Iterator over all Nodes.

        :raises kube.APIError: For errors from the k8s API server.
        """
        data = self.cluster.proxy.get('nodes')
        for item in data['items']:
            yield NodeResource(self.cluster, item)

    def fetch(self, name):
        """Retrieve an individual node by name.

        :param str name: The name of the node to retrieve.

        :return: A single :class:`kube.Node` instance.
        :raises LookupError: If the node does not exist.
        :raises kube.APIError: For errors from the k8s API server.
        """
        data = kube._util.fetch_resource(self.cluster, 'nodes', name)
        return NodeResource(self.cluster, data)

    def filter(self, selector):
        """Return an iterator of a subset of the nodes.

        Currently selectors with only equality-based requirements are
        supported.  This has the same constraints as the selectors you
        can use in a ReplicationController or Service.

        :param dict selector: Dictionary of the labels to use as
           equality based selector.

        :returns: An iterator of :class:`NodeResource` instances which
           match the selector.
        :raises ValueError: If an empty selector is used.  An empty
           selector is almost certainly not what you want.  Kubernetes
           treats an **empty** selector as *all* items and treats a
           **null** selector as *no* items.
        :raises kube.APIError: For errors from the k8s API server.
        """
        data_iter = kube._util.filter_list(self.cluster, 'nodes', selector)
        for item in data_iter:
            yield NodeResource(self.cluster, item)

    def watch(self):
        pass


class AddressType(enum.Enum):
    """Enumeration of the address types."""
    ExternalIP = 'ExternalIP'
    InternalIP = 'InternalIP'
    Hostname = 'Hostname'


class NodeResource(kube._base.ResourceABC):
    """A node in the Kubernetes cluster.

    See http://kubernetes.io/v1.1/docs/admin/node.html for details.

    :param str name: The name of the node.
    :param kube.Cluster cluster: The cluster this node belongs to.

    :ivar cluster: The :class:`kube.Cluster` this node belongs to.
    :ivar raw: The raw decoded JSON ojbect as returned by the API
       server.  Do not idly modify this.
    """
    _Address = collections.namedtuple('Address', ['type', 'addr'])
    _Capacity = collections.namedtuple('Capacity', ['cpu', 'mem', 'pods'])

    def __init__(self, cluster, raw):
        self.cluster = cluster
        self.raw = raw

    @property
    def meta(self):
        """The node's metadata as a :class:`kube.meta.ObjectMeta` instance.

        This provides access to the node's name, labels etc.
        """
        return kube._meta.ObjectMeta(self)

    def spec(self):
        """The spec of this node's resource.

        This is the raw, decoded JSON data representing the spec of
        this node.
        """
        return copy.deepcopy(self.raw['spec'])

    @property
    def addresses(self):
        """An iterator of the addresses for this node.

        Each address is a namedtuple with ``(type, addr)`` as fields.
        Known types are: ``ExternalIP``, ``InternalIP`` and
        ``Hostname``.

        An empty list is returned if there are not yet any addresses
        associated with the node.
        """
        status = self.raw.get('status', {})
        for raw in status.get('addresses', []):
            type_ = AddressType(raw['type'])
            addr = ipaddress.ip_address(raw['address'])
            yield self._Address(type_, addr)

    @property
    def capacity(self):
        """The capacity of the node.

        CPU is expressed in cores and can use fractions of cores,
        while memory is expressed in bytes.

        :returns: a namedtuple with ``(cpu, mem, pods)`` as fields.

        :raises kube.StatusError: If there is not yet a capacity
           associated with the node.
        """
        # See http://kubernetes.io/v1.1/docs/design/resources.html for
        # details on resources usage.  This needs to deal with custom
        # resources as well.  The current stub implementation does not
        # match well.
        status = self.raw.get('status', {})
        raw = status.get('capacity', None)
        if not raw:
            raise kube.StatusError('No capacity found')
        return self._Capacity(float(raw['cpu']),
                              int(raw['memory']), int(raw['pods']))

    @property
    def conditions(self):
        """List of conditions.

        XXX
        """

    def watch(self):
        pass
