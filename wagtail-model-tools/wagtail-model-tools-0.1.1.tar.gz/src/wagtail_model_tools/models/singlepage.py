from django.db.models.manager import ManagerDescriptor
from django.contrib.contenttypes.models import ContentType
from wagtail.wagtailcore.models import Page, PageManager


__all__ = ['SinglePage', 'SinglePageMixin', 'SinglePageManager']


class MixinManagerDescriptor(ManagerDescriptor):
    def __init__(self, manager_class, name='objects'):
        self.manager_class = manager_class
        self.name = name

    def __get__(self, instance, type=None):
        if instance is not None:
            return super().__get__(instance, type)

        descriptor = ManagerDescriptor(self.manager_class(model=type))
        setattr(type, self.name, descriptor)
        return descriptor.__get__(None, type)


class SinglePageManager(PageManager):
    """
    A PageManager with the .instance() method to retrieve the single instance
    object.
    """

    def instance(self):
        """
        Return the single instance for the SingleModel.
        """

        return self.model.get_instance()


class SinglePageMixin:
    """
    The mixin version of SimplePage.
    """

    __instance_id = None
    objects = MixinManagerDescriptor(SinglePageManager)

    @classmethod
    def get_instance(cls):
        """
        Return the single instance.
        """

        try:
            content_type = get_content_type(cls)
            instance = cls.objects.get(content_type=content_type).specific

        except cls.DoesNotExist:
            instance = cls(**cls.get_state())
            parent = cls.get_parent()
            parent.add_child(instance=instance)
            instance.save()
            instance = instance

        cls.__instance = instance
        return instance

    @classmethod
    def get_parent(cls):
        """
        Return the parent page instance.
        """

        return Page.objects.get(path='00010001')

    @classmethod
    def get_state(cls):
        """
        Return a dictionary with the instance state. The state dictionary must
        provide initialization data such as the page title, slug, seo_title,
        etc.

        Must be overridden in subclasses.
        """

        raise NotImplementedError

    def save(self, *args, **kwargs):
        instance_id = self.__instance_id
        if (self.id is None and instance_id is not None or
                    instance_id is not None and instance_id != self.id):
            name = self.__class__.__name__
            raise ValueError(
                'Trying to create a second instance of %(cls)s\n'
                'Please do not try to create or instantiate %(cls)s objects '
                'explicitly. Instead, use the %(cls)s.objects.instance() '
                'interface.' % {'cls': name}
            )

        super().save(*args, **kwargs)
        self.__instance_id = self.id


class SinglePage(SinglePageMixin, Page):
    """
    A page subclass that has a single entry in the database.

    This implementation do not prevent the page object from being instantiated
    several times. Instead, all instances must point to the same entry in the
    database.

    Subclasses should implement the ``cls.get_state()`` and (optionally) the
    ``cls.get_parent()`` class methods.
    """

    class Meta:
        abstract = True

    objects = SinglePageManager()


def get_content_type(cls):
    return ContentType.objects.get_for_model(cls, for_concrete_model=True)
