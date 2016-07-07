"""Interface for namespaces."""

import enum

import kube._base
import kube._meta
import kube._pod
import kube._util


class NamespaceView(kube._base.ViewABC):
    """All the namespaces within a cluster.

    :param kube.Cluster cluster: the cluster containing the namespaces.

    :ivar kube.Cluster cluster: the :class:`kube.Cluster` instance.
    """

    def __init__(self, cluster):
        self.cluster = cluster

    def __iter__(self):
        """Iterate over all namespaces in the cluster.

        :raises kube.APIError: for errors from the k8s API server.
        """
        data = self.cluster.proxy.get('namespaces')
        for item in data['items']:
            yield NamespaceResource(self.cluster, item)

    def fetch(self, name):
        """Retrieve an individual namespace by name.

        :param str name: The name of the namespace resource to
           retrieve.

        :returns: A :class:`kube.NamespaceResource` instance.
        :raises LookupError: If the namespace does not exist.
        :raises kube.APIError: For errors from the k8s API server.
        """
        data = kube._util.fetch_resource(self.cluster, 'namespaces', name)
        return NamespaceResource(self.cluster, data)

    def filter(self, selector):
        """Get a filtered iterator of namespaces.

        Currently selectors with only equality-based requirements are
        supported.  This has the same constraints as the selectors you
        can use in a ReplicationController or Service.

        :param dict selector: Dictionary of the labels to use as
           equality based selector.

        :returns: An iterator of :class:`NamespaceResource` instances
            which match the given selector.
        :raises ValueError: if an empty selector is used.  An empty
           selector is almost certainly not what you want.  Kubernetes
           treats an **empty** selector as *all* items and treats a
           **null** selector as *no* items.
        :raises kube.APIError: For errors from the k8s API server.
        """
        data_iter = kube._util.filter_list(self.cluster,
                                           'namespaces', selector)
        for data in data_iter:
            yield NamespaceResource(self.cluster, data)

    def watch(self):
        raise NotImplementedError


class NamespacePhase(enum.Enum):
    """Enumeration of all possible namespace phases.

    This is aliased to :attr:`NamespaceResource.NamespacePhase`
    for convenience.
    """
    Active = 'Active'
    Terminating = 'Terminating'


class NamespaceResource(kube._base.ResourceABC):
    """A namespace in the Kubernetes cluster.

    :cvar NamespacePhase: Convenience alias of :class:`NamespacePhase`.

    :ivar cluster: the :class:`kube.Cluster` instance.
    :ivar raw: the raw JSON-decoded representation of the namespace.
    :ivar pods: a :class:`kube.PodView` of the pods in the namespace.
    """

    NamespacePhase = NamespacePhase

    def __init__(self, cluster, raw):
        self.cluster = cluster
        self.raw = raw
        self.pods = kube._pod.PodView(cluster, self.meta.name)

    @property
    def meta(self):
        """Namespace's metadata as a :class:`kube.ObjectMeta`."""
        return kube._meta.ObjectMeta(self)

    @property
    def phase(self):
        """Phase of the namespace as a :class:`kube.NamespacePhase`."""
        return NamespacePhase(self.raw['status']['phase'])

    def spec(self):
        return kube._util.thaw(self.raw['spec'])

    def watch(self):
        """Watch the namespace for changes.

        :raises NotImplementedError:
        """
        raise NotImplementedError
