"""Interface for pod resources."""

import collections
import enum
import functools
import ipaddress

import kube._base
import kube._cluster
import kube._error
import kube._meta
import kube._namespace
import kube._util


class PodView(kube._base.ViewABC):
    """All the pods within a namespace.

    :param kube.Cluster cluster: The cluster this view is part of.

    :param str namespace: The namespace this view is contstrained to.

    :ivar kube.Cluster cluster: The cluster instance this view is part of.
    :ivar str namespace: The namespace this view is contrained to, if
       the view is not bound to a namespace this will be ``None``.
    """

    def __init__(self, cluster, namespace=None):
        self.cluster = cluster
        self.namespace = namespace

    def __iter__(self):
        """Iterate over all the :class:`Pod`s in the view.

        :raises kube.APIError: For errors from the k8s API server.
        """
        if self.namespace:
            data = self.cluster.proxy.get('namespaces', self.namespace, 'pods')
        else:
            data = self.cluster.proxy.get('pods')
        for item in data['items']:
            yield PodResource(self.cluster, item)

    def fetch(self, name):
        """Retrieve an individual pod by name.

        .. warning::

           This method is only available when the view was created for
           a namespace.

        :param str name: The name of the pod to retrive.

        :return: A :class:`kube.PodResource` instance.
        :raises LookupError: If the pod does not exist.
        :raises kube.APIError: For errors from the k8s API server.
        :raises RuntimeError: When the view is not bound to a namespace.
        """
        if not self.namespace:
            raise RuntimeError('Fetch requires the view to have a namespace')
        data = kube._util.fetch_resource(self.cluster, 'pods',
                                         name, namespace=self.namespace)
        return PodResource(self.cluster, data)

    def filter(self, selector=None):
        """Get a filtered iterator of pods.

        :param kube.Selector selector: the criteria that pods must match in
            order to be returned. If ``None`` or the selector is empty then
            an unfiltered iterator is returned.

        :returns: an iterator of :class:`Pod`s that match the given selector.
        """
        data_iter = kube._util.filter_list(self.cluster, 'pods',
                                           selector, namespace=self.namespace)
        for item in data_iter:
            yield PodResource(self.cluster, item)

    def watch(self):
        """Watch the list of pods for changes.

        :returns: an iterator of :class:`kube.WatchEvent`s where the
            :attr:`kube.WatchEvent.object` attribute will be :class:`Pod`
            instances.
        :raises kube.NamespaceError: When the namespace no longer
           exists.
        :raises kube.APIError: For errors from the k8s API server.
        """
        if self.namespace:
            path = ['namespaces', self.namespace, 'pods']
        else:
            path = ['pods']
        try:
            podlist = self.cluster.proxy.get(*path)
        except kube._error.APIError as err:
            if self.namespace and err.status_code == 404:
                raise kube._error.NamespaceError from err
            else:
                raise
        version = podlist['metadata']['resourceVersion']
        for event in self.cluster.proxy.watch(*path, version=version):
            if (event.object['kind'] == 'Pod'
                    and event.type is not event.WatchEventType.ERROR):
                yield kube._cluster.WatchEvent(
                    event.type,
                    PodResource(self.cluster, event.object),
                )


class PodPhase(enum.Enum):
    """Enumeration of all possible pod phases.

    This is aliased to :attr:`Pod.PodPhase` for convenience.
    """
    Pending = 'Pending'
    Running = 'Running'
    Succeeded = 'Succeeded'
    Failed = 'Failed'


class PodResource(kube._base.ResourceABC):
    """A pod in the Kubernetes cluster.

    Each pod contains a number of containers and volumes which are executed
    on a node within the cluster. A pod may exist in a namespace. Pods are
    typically managed by a controller such as a replication controller or
    job.

    :param kube.Cluster cluster: The cluster the pods is bound to.
    :param raw: The decoded JSON object representing the pod.

    :cvar PodPhase: Convenience alias of :class:`PodPhase`.

    :ivar kube.Cluster cluster: The cluster this instance is bound to.
    :ivar dict raw: The decoded JSON representation of the pod.
    """
    PodPhase = PodPhase

    def __init__(self, cluster, raw):
        self.cluster = cluster
        self.raw = raw

    @property
    def meta(self):
        """Pod's metadata as a :class:`kube.ObjectMeta`."""
        return kube._meta.ObjectMeta(self)

    def spec(self):
        pass

    @property
    def phase(self):
        """Phase of the pod as a :class:`kube.PodPhase`."""
        return PodPhase(self.raw['status']['phase'])

    @property
    def start_time(self):
        """Start the pod was started as a :class:`datetime.datetime`."""
        return kube._util.parse_rfc3339(self.raw['status']['startTime'])

    @property
    def ip(self):
        """IP address of the pod within the cluster

        This may be as a :class:`ipaddress.IPV4Address` or a
        :class:`ipaddress.IPv6Address`.
        """
        return ipaddress.ip_address(self.raw['status']['podIP'])

    @property
    def host_ip(self):
        """IP address of the pod's host within the cluster.

        This  may be as a :class:`ipaddress.IPV4Address` or a
        :class:`ipaddress.IPv6Address`.
        """
        return ipaddress.ip_address(self.raw['status']['hostIP'])

    @property
    def message(self):
        """Human readable message explaining the pod's state.

        :raises kube.StatusError: If no message set.
        """
        if 'message' not in self.raw['status']:
            raise kube._error.StatusError
        return self.raw['status']['message']

    @property
    def reason(self):
        """PascalCase string explaining the pod's state.

        :raises kube.StatusError: If no reason set.
        """
        if 'reason' not in self.raw['status']:
            raise kube._error.StatusError
        return self.raw['status']['reason']

    @property
    def containers(self):
        """Iterate over all :class:`Container`s in the pod."""
        for container_status in self.raw['status']['containerStatuses']:
            yield Container(container_status, self)

    def watch(self):
        pass


class Container:
    """A container inside a pod.

    Kubernetes containers are a thin abstraction on top of Docker containers.
    If a container dies, it may be restarted inside the pod as controlled
    by the restart policy of the pod.

    :param raw: the JSON-decoded object contained within the ``PodStatus`'
        ``containerStatuses`` array.
    :param Pod pod: The pod the container is bound to.

    :ivar raw: The raw JSON-decoded object representing the container.
    :ivar Pod pod: The pod the container is bound to.
    """

    def __init__(self, raw, pod):
        self.raw = raw
        self.pod = pod

    def __repr__(self):
        return "<{0.__class__.__name__} {0.name!r} of {0.pod}>".format(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.raw == other.raw
        else:
            return NotImplemented

    @property
    def name(self):
        """The name of the container as a string."""
        return self.raw['name']

    @property
    def restart_count(self):
        """The number of times the container was restarted as an integer."""
        return self.raw['restartCount']

    @property
    def ready(self):
        """Whether or not the container is read as a boolean."""
        return self.raw['ready']

    @property
    def image(self):
        """Docker image running in the container

        :returns: A :class:`ContainerImage`.
        """
        return ContainerImage(
            self.raw['imageID'].split('//')[-1],
            self.raw['image'],
        )

    @property
    def id(self):
        """Hex-encoded Docker container ID hash as a string."""
        return self.raw['containerID'].split('//')[-1]

    @property
    def state(self):
        """Current state of the container as a :class:`ContainerState`."""
        return ContainerState(self.raw['state'], self)

    @property
    def last_state(self):
        """Current state of the container.

        :returns: A :class:`ContainerState` or ``None`` if the container has
            no previous state.
        """
        if self.raw['lastState']:
            return ContainerState(self.raw['lastState'], self)
        else:
            return None  # TODO: or StatusError


class ContainerState:
    """The state of a container within a pod.

    A container can be in one of three states: 'running', 'waiting' or
    'terminated'. This class provides a uniform interface to all states.
    However, some fields are only available in certain states. In such
    cases, attempting to access a field that is not supported by the state
    will result in an :exc:`kube.StatusError` being raised.

    The overall state of the container can be determined by inspecting the
    :attr:`running`, :attr:`waiting` and :attr:`terminated` attributes,
    of which one and only one will be ``True``.

    :param raw: The raw JSON-decoded ``ContainerState`` API object
        as exposed by ``ContainerStatus`` objects.
    :param Container container: The container the state refers to.

    :ivar raw: The raw JSON-decoded object representing the container state.
    :ivar Container container: The container the state refers to.
    """

    def __init__(self, raw, container):
        self._state = list(raw.keys())[0]
        self._value = raw[self._state]
        self.raw = raw
        self.container = container

    def __repr__(self):
        if self.running:
            state = 'running'
        elif self.waiting:
            state = 'waiting'
        elif self.terminated:
            state = 'terminated'
        return '<{0.__class__.__name__} {1}>'.format(self, state)

    @property
    def running(self):
        """Boolean indicating if the container is running."""
        return self._state == 'running'

    @property
    def waiting(self):
        """Boolean indicating if the container is waiting."""
        return self._state == 'waiting'

    @property
    def terminated(self):
        """Boolean indicating if the container has been terminated."""
        return self._state == 'terminated'

    def _ensure_state(*states):
        """Decorator to ensure a container is in a specific state.

        This decorator can be used to wrap a method so that it's only
        excuted if the current state is one of the ones specified. If
        the state is invalid when the call is made then a
        :exc:`kube.StatusError` will be raised instead.

        Additionally, this decorator will modify the docstring of the
        wrapped function to include a sphinx-style ``:raises:`` directive
        documenting the valid states for the call.

        :params states: The state attribute names to allow.
        """

        def decorator(function):  # pylint: disable=missing-docstring

            @functools.wraps(function)
            def wrapper(instance, *args, **kwargs):  # pylint: disable=missing-docstring
                if not any(getattr(instance, state) for state in states):
                    raise kube.StatusError(
                        'Only available for states: ' + ', '.join(states))
                return function(instance, *args, **kwargs)

            if not wrapper.__doc__.endswith("\n"):
                wrapper.__doc__ += "\n"
            wrapper.__doc__ += ("\n:raises kube.StatusError: if the container "
                                "state is not {}.".format(', '.join(states)))
            return wrapper

        return decorator

    @property
    @_ensure_state('running', 'terminated')
    def started_at(self):
        """The time the container was started or restarted.

        :returns: A :class:`datetime.datetime`.
        """
        return kube._util.parse_rfc3339(self._value['startedAt'])

    @property
    @_ensure_state('waiting', 'terminated')
    def reason(self):
        """Brief reason explaining the containers state."""
        return self._value['reason']

    @property
    @_ensure_state('terminated')
    def exit_code(self):
        """Exit code of the container."""
        return self._value['exitCode']

    @property
    @_ensure_state('terminated')
    def signal(self):
        """Last signal sent to the container.

        .. warning::
            The signal is identified numerically, however these signal
            numbers are not portable therefore it's ill-advised to attempt
            to compare this value with the constants provided by the
            built-in :mod:`singal` module.
        """
        return self._value['signal']

    @property
    @_ensure_state('terminated')
    def message(self):
        """Message explaining the termination of the container."""
        return self._value['message']

    @property
    @_ensure_state('terminated')
    def finished_at(self):
        """The time the container was terminated.

        :returns: A :class:`datetime.datetime`.
        """
        return kube._util.parse_rfc3339(self._value['finishedAt'])

    del _ensure_state


ContainerImage = collections.namedtuple('ContainerImage', ('id', 'name'))
ContainerImage.__doc__ = """\
Represents a Docker image loaded into a pod's :class:`Container`.

:ivar str id: the hex-encoded Docker image ID hash.
:ivar str name: the respository name of the image including tag.
"""


class PodTemplateList:
    pass  # TODO: everything


class PodTemplate:
    pass  # TODO: everything
