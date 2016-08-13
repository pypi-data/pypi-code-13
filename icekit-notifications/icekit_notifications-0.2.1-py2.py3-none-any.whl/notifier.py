from django.contrib.admin.sites import AlreadyRegistered, NotRegistered
from django.db.models.base import ModelBase


class Notifier(object):
    """
    Send notifications for object saves.

    Models are registered with `Notifier` using the register() method.
    """
    def __init__(self):
        self._registry = list()

    def register(self, model_or_iterable):
        """
        Registers the given model(s).

        The model(s) should be Model classes, not instances.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyRegistered(
                    'Model "%s" is already registered for notifications' % model.__name__
                )

            self._registry.append(model)

    def unregister(self, model_or_iterable):
        """
        Unregisters the given model(s).

        If a model isn't registered, this will raise NotRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if model in self._registry:
                self._registry.remove(model)
            else:
                raise NotRegistered(
                    'Model "%s" is not registered for notifications' % model.__name__
                )

    def get_registered_models(self):
        """
        Returns a list of all registered models.
        """
        return self._registry

notifier = Notifier()
