
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from leonardo_module_vis_quantitative.models import NumericWidget

DISPLAY_CHOICES = (
    ('full_circle', _('Full circle')),
    ('half_circle_top', _('Half circle')),
)

class DonutChartWidget(NumericWidget):
    """
    Widget which shows donut chart.
    """

    display = models.CharField(max_length=55, verbose_name=_(
        "Display style"), default='full_circle', choices=DISPLAY_CHOICES)

    donut_ratio = models.IntegerField(
        verbose_name=_('Donut ratio'), default=33)

    @cached_property
    def get_chart_params(self):

        super_data = super(NumericWidget, self).get_chart_params
        data = {
           'donut_ratio': self.donut_ratio,
           'display': self.display,
           'chartSelector': "#vis_%s svg" % self.fe_identifier
        }
        final_data = super_data.copy()
        final_data.update(data)
        return final_data

    class Meta:
        abstract = True
        verbose_name = _("Doughnut chart")
        verbose_name_plural = _("Doughnut charts")
