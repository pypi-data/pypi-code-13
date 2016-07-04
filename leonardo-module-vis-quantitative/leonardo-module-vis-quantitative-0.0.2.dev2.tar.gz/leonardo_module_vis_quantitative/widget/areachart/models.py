
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from leonardo_module_vis_quantitative.models import TimeSeriesWidget

DISPLAY_CHOICES = (
    ('stack', _('Stacked')),
    ('stream', _('Stream')),
    ('expand', _('Expanded')),
)

INTERPOLATION_CHOICES = (
    ('cardinal', _('Cardinal')),
    ('linear', _('Linear')),
    ('step', _('Step')),
)

class AreaChartWidget(TimeSeriesWidget):
    """
    Widget which shows area chart.
    """

    display = models.CharField(max_length=55, verbose_name=_(
        "Display style"), default='stack', choices=DISPLAY_CHOICES)
    interpolation = models.CharField(max_length=55, verbose_name=_(
        "Interpolation"), default='linear', choices=INTERPOLATION_CHOICES)

    @cached_property
    def get_chart_params(self):

        super_data = super(AreaChartWidget, self).get_chart_params
        data = {
           'style': self.display,
           'interpolation': self.interpolation,
           'chartSelector': "#vis_%s svg" % self.fe_identifier
        }
        final_data = super_data.copy()
        final_data.update(data)
        return final_data


    class Meta:
        abstract = True
        verbose_name = _("Area chart")
        verbose_name_plural = _("Area charts")
