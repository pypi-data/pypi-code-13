"""View helpers for the Madcap Flare integration.
"""
from django.core.exceptions import ImproperlyConfigured


class MadcapFlareMixin(object):
    """Mixin for the Madcap Flare integration.

    This provides a context key to pass into your template to automatically
    render the correct help topic URL.
    """

    help_key = None

    def get_help_key(self):
        """Return the help_key or raise ImproperlyConfigured.
        """
        if self.help_key is None:
            raise ImproperlyConfigured(
                u'The help_key attribute must be set on {}'.format(
                    self.__class__))
        return self.help_key

    def get_context_data(self, **kwargs):
        """Attach the help_key to the context.
        """
        context = super(MadcapFlareMixin, self).get_context_data(**kwargs)
        context['help_key'] = self.get_help_key()
        return context
