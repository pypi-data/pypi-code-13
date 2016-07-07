"""Some base classes and ABCs for kube.

While all implementations are supposed to at least register their
classes, subclassing is not really a aim.  With the exception of
:meth:`__repr__` most properties and methods are marked as abstract
and do not have a common implementation even if they could.  To share
code instead helper functions in ``kube._util`` should be used.
"""

import abc

import kube._error


class ViewABC(metaclass=abc.ABCMeta):
    """Represents a view to a collection of resources.

    All top-level resources in Kubernetes have a collection, resources
    of a ``*List`` kind, with some common functionality.  This ABC
    defines views to provide access to resources in collections in a
    uniform way.  Note that a view is not the same as the collection
    resource, e.g. collections resources have some metadata associated
    with them and exist at a particular point in time, they have a
    metadata.resourceVersion, which views do not have.

    It is always possible to create an instance of this without
    needing to do any requests to the real Kubernetes cluster.

    :param kube.Cluster cluster: The cluster this resource list is
       part of.
    :param str namespace: The optional namespace this resource list is
       part of.  If the resource list is not part of a namespace this
       will be ``None`` which means it will be a view to all resources
       of a certain type, regardelss of their namespace.

       Some resources can not be namespaced, e.g. Nodes.  In this case
       the signature should not include this parameter.

    :ivar kube.Cluster cluster: The cluster this resource list is part
       of.
    :ivar str namespace: The optional namespace this resource list is
       part of.  If the resource list is not part of a namespace this
       will be ``None``, including for resource lists which do not
       support namespaces.

       Some resources can not be namespaced, e.g. Nodes.  In this case
       the view will must not have this attribute.
    """

    @abc.abstractmethod
    def __init__(self, cluster, namespace=None):
        self.cluster = cluster
        self.namespace = namespace

    def __repr__(self):
        if self.namespace is None:
            return '<{0.__class__.__name__}>'.format(self)
        else:
            return ('<{0.__class__.__name__} namespace={0.namespace}>'
                    .format(self))

    @abc.abstractmethod
    def __iter__(self):
        """Iterator of all resources in this collection.

        :raises kube.APIError: for errors from the k8s API server.
        """

    @abc.abstractmethod
    def fetch(self, name):
        """Retrieve a single resource by name.

        Not all resources can be retrieved by name without a
        namespace.  In this case this method will raise a
        :class:`RuntimeError` when being called.

        :param str name: The name of the resource.

        :returns: A single instance representing the resource.
        :raises LookupError: If the resource does not exist.
        :raises kube.APIError: For errors from the k8s API server.
        :raises RuntimeError: When the resource can not be retrieved
           by name only
        """

    @abc.abstractmethod
    def filter(self, selector):
        """Return an iterable of a subset of the resources.

        Currently selectors with only equality-based requirements are
        supported.  This has the same constraints as the selectors you
        can use in a ReplicationController or Service.

        :param dict selector: Dictionary of the labels to use as
           equality based selector.

        :returns: An iterator of :class:`kube.ResourceABC` instances
           of the correct type for the resrouce.
        :raises ValueError: If an empty selector is used.  An empty
           selector is almost certainly not what you want.  Kubernetes
           treats an **empty** selector as *all* items and treats a
           **null** selector as *no* items.
        :raises kube.APIError: for errors from the k8s API server.
        """

    @abc.abstractmethod
    def watch(self):
        """Watch for changes to any of the resources in the view.

        Whenever one of the resources in the view changes a new
        :class:`kube.WatchEvent` instance is yielded.

        :returns: An iterator of :class:`kube.WatchEvent` instances.
        :raises kube.APIError:
        """


class ResourceABC(metaclass=abc.ABCMeta):
    """Representation for a kubernetes resource.

    All resources have some common attributes and API which must match
    this ABC.

    :param kube.Cluster cluster: The cluster this resource is bound to.
    :param dict raw: The decoded JSON representing the resource.

    :ivar cluster: The :class:`kube.Cluster` instance this resource is
       bound to.
    :ivar raw: The raw decoded JSON representing the resource.  This
       behaves like a dict but is actually an immutable view of the
       dict.
    """

    @abc.abstractmethod
    def __init__(self, cluster, raw):
        self.cluster = cluster
        self.raw = raw

    def __repr__(self):
        try:
            return ('<{0.__class__.__name__} {0.meta.name} '
                    'namespace={0.meta.namespace}>' .format(self))
        except kube._error.StatusError:
            return '<{0.__class__.__name__} {0.meta.name}>'.format(self)

    @abc.abstractproperty
    def meta(self):
        """The resource's metadata as a :class:`kube.ObjectMeta` instance."""

    @abc.abstractmethod
    def spec(self):
        """The spec of this node's resource.

        This returns a copy of the raw, decodeed JSON data
        representing the spec of this resource which can be used to
        re-create the resource.
        """

    @abc.abstractmethod
    def watch(self):
        """Watch the resource for changes.

        Whenever the resource changes a new :class:`kube.WatchEvent`
        is returned.

        :returns: an iterator of :class:`kube.WatchEvent` instances
           for the resource.
        """
