from functools import partial
import importlib
from threading import Lock

from acetone.exceptions import AcetoneAlreadyRegisteredError, AcetoneLoadError, AcetoneNotFoundError
from .dependency import Dependency, ClassDependency


class AcetoneContainer(object):
    def __init__(self):
        self._dependencies = {}
        self._lock = Lock()

        self.Dependency = partial(Dependency, container=self)
        self.ClassDependency = partial(ClassDependency, container=self)

    def register_factory(self, key, factory_functor):
        with self._lock:
            if key in self._dependencies:
                raise AcetoneAlreadyRegisteredError(key)

            self._dependencies[key] = factory_functor

    def register_instance(self, key, service):
        self.register_factory(key, lambda: service)

    def load_from_dicts(self, descriptions):
        for description in descriptions:
            name = description['name']
            name_type = description.get('name_type', 'type')

            module_name = description['module']
            factory_name = description['factory']
            args = description.get('args', [])
            kwargs = description.get('kwargs', {})
            single = description.get('singleton', False)

            try:
                module = importlib.import_module(module_name)
                factory = getattr(module, factory_name)
            except ImportError:
                raise AcetoneLoadError("Module '{0}' can't be imported".format(module_name))
            except AttributeError:
                raise AcetoneLoadError(
                    "Factory '{0}' not found in '{1}'".format(factory_name, module_name)
                )

            if single:
                instance = factory(*args, **kwargs)
                self.register_instance(name, instance)
            else:
                def factory_method():
                    return factory(*args, **kwargs)
                self.register_factory(name, factory_method)

    def clear(self):
        with self._lock:
            self._dependencies.clear()

    def __getitem__(self, key):
        try:
            return self._dependencies[key]()
        except KeyError:
            # Pass and raise the proper exception later to avoid
            # exception raised during 'except'.
            pass

        raise AcetoneNotFoundError(key)
