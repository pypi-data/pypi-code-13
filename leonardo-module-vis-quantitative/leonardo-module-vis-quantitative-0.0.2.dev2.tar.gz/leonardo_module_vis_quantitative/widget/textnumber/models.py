
from django.utils.translation import ugettext_lazy as _
from django.db import models
from leonardo_module_vis_quantitative.models import NumericWidget

TIME_UNITS = (
    ('second', _('seconds')),
    ('minute', _('minutes')),
    ('hour', _('hours')),
    ('day', _('days')),
)

class TextNumberWidget(NumericWidget):
    """
    Widget which shows number in text format.
    """

    duration_length = models.IntegerField(
        verbose_name=_('duration length'), default=2)
    duration_unit = models.CharField(max_length=55, verbose_name=_(
        'duration unit'), choices=TIME_UNITS, default="hour")

    class Meta:
        abstract = True
        verbose_name = _("Text number")
        verbose_name_plural = _("Text numbers")
