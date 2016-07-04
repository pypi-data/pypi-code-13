
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from leonardo_module_vis_quantitative.models import NumericWidget

    
class AngularGaugeWidget(NumericWidget):
    """
    Widget which shows angular gauge.
    """
    major_ticks = models.IntegerField(verbose_name=_('Major ticks'), default=5)
    minor_ticks = models.IntegerField(verbose_name=_('Minor ticks'), default=2)
    warning_threshold = models.IntegerField(
        verbose_name=_('Warning threshold'), default=70)
    critical_threshold = models.IntegerField(
        verbose_name=_('Critical threshold'), default=90)

    @cached_property
    def get_chart_params(self):

        super_data = super(NumericWidget, self).get_chart_params
        data = {
           'label': 'Angular',
           'min': 0,
           'max': 100
        }
        final_data = super_data.copy()
        final_data.update(data)
        return final_data

    class Meta:
        abstract = True
        verbose_name = _("Angular gauge")
        verbose_name_plural = _("Angular gauges")
