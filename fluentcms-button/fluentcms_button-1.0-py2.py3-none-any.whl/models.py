from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import PluginHtmlField, PluginUrlField
from fluent_contents.models import ContentItem

from . import appsettings


@python_2_unicode_compatible
class ButtonItem(ContentItem):
    """
    Pager item, to show a previous/next page.
    The pages are auto determined, but can be overwritten
    """
    title = models.CharField(_("Title"), max_length=200)
    url = PluginUrlField(_("URL"))

    style = models.CharField(_("Style"), max_length=50, choices=appsettings.FLUENTCMS_BUTTON_STYLES)
    size = models.CharField(_("Size"), blank=True, default='', max_length=10, choices=appsettings.FLUENTCMS_BUTTON_SIZES)

    block = models.BooleanField(_("Span the full width"), default=False, blank=True)

    class Meta:
        verbose_name = _("Button")
        verbose_name_plural = _("Button")

    def __str__(self):
        return self.title

    @property
    def css_classes(self):
        classes = ['btn', self.style, self.size or '']
        if self.block:
            classes.append('btn-block')
        return ' '.join(classes).rstrip().replace('  ', ' ')
