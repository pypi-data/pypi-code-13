from threading import Lock

from .exceptions import AcetoneError


class BaseDependency(object):
    def __init__(self, key, container):
        self._container = container
        self._key = key
        self._name = None
        self._lock = Lock()

    def _determine_name_and_original_objtype(self, objtype):
        # This is the only reasonable way to find attribute name of the service.
        # The other way would be very explicit:
        #     my_name = Service('my_name', Class)
        # but this is error prone and not convenient.
        mro = objtype.mro()

        for mro_type in mro:
            for key, value in mro_type.__dict__.items():
                if value is self:
                    return key, mro_type

        # can't imagine such situation
        raise AcetoneError("Can't determine the name")

_Undefined = object()


class Dependency(BaseDependency):
    def __get__(self, obj, objtype=None):
        with self._lock:
            # the usual property behavior
            if obj is None:
                return self

            # Name was not set, this is the very first access for this Dependency instance.
            if not self._name:
                self._name, _ = self._determine_name_and_original_objtype(objtype)
            else:
                # This part is to avoid potential issues related to accessing:
                #     instance.dependency
                # from multiple threads.
                thing = obj.__dict__.get(self._name, _Undefined)
                if thing is not _Undefined:
                    return thing

            service = self._container[self._key]

            # This is the magic trick which makes it fast. Instance member is
            # set by this code and all subsequent access is solved as
            # a member access, not as a descriptor access.
            setattr(obj, self._name, service)
            return service

    def __repr__(self):
        return 'Dependency(' + repr(self._key) + ')'


class ClassDependency(BaseDependency):
    """
    Class level dependency works the same way as a class member:

        class Class(object):
            class_dependency = ClassDependency()
            class_member = 123

        instance = Class()
        assert Class.class_dependency == instance.class_dependency
        assert Class.class_member == instance.class_member

    """
    def __get__(self, obj, objtype=None):
        with self._lock:
            if not self._name:
                self._name, original_objtype = self._determine_name_and_original_objtype(objtype)
            else:
                thing = objtype.__dict__.get(self._name, None)
                if thing is self:
                    # I can't imagine how this can happen
                    raise AcetoneError()
                return thing

            service = self._container[self._key]
            setattr(original_objtype, self._name, service)

            return service

    def __repr__(self):
        return 'ClassDependency(' + repr(self._key) + ')'
