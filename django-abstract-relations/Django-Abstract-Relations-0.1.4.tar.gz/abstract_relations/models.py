import sys

from django.core.exceptions import ImproperlyConfigured
from django.db import models


class AbstractManyToManyField(models.ManyToManyField):
    def __init__(self, to, **kwargs):
        """
        Retains `to` argument and keeps it in order to use it later
        during creation of new intermediary model.

        Raises an error when used without `through` argument,
        because in that case ManyToManyField should be used.
        """
        self._to = to

        if kwargs.get('through') is None:
            raise ImproperlyConfigured(
                "%s definition must include 'through' argument. "
                "Otherwise, resort to using %s" % (
                    self.__class__.__name__, models.ManyToManyField.__name__))

        super(AbstractManyToManyField, self).__init__(to, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """
        If the field has been defined inside non-abstract class,
        tries to dynamically create a new intermediary model.
        """
        if not cls._meta.abstract:
            self._recreate_through_model(cls)
        super(AbstractManyToManyField, self).contribute_to_class(
            cls, name, **kwargs)

    def _recreate_through_model(self, cls):
        """
        Overwrites the `through` attribute with new intermediary model.

        Makes the class available in same module,
        where the original intermediary model was defined.
        """
        if hasattr(self._to, '_meta'):  # Don't proceed during migrations
            self.remote_field.through = through = self._get_through_model(
                self.remote_field.through, cls, self._to)
            setattr(sys.modules[through.__module__], through.__name__, through)

    def _get_through_model(self, abstract_through, from_model, to_model):
        """
        Returns the newly generated intermediary model.

        Returns:
            models.Model: Dynamically created intermediary model
        """
        return type(abstract_through)(
            '{}{}'.format(from_model.__name__, to_model.__name__),
            (abstract_through,),
            {
                '__module__': abstract_through.__module__,
                'abstract_item': property(
                    lambda this: getattr(this, from_model._meta.model_name)),
                from_model._meta.model_name: models.ForeignKey(from_model),
            }
        )
