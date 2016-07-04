
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from leonardo_module_vis_quantitative.models import TimeSeriesWidget

DISPLAY_CHOICES = (
    ('stack', _('Stacked')),
    ('group', _('Grouped')),
)


class BarChartWidget(TimeSeriesWidget):
    """
    Widget for displaying time-series data using bar chart.
    """

    display = models.CharField(max_length=55, verbose_name=_(
        "Display style"), default='stacked', choices=DISPLAY_CHOICES)

    @cached_property
    def get_chart_params(self):

        super_data = super(BarChartWidget, self).get_chart_params
        data = {
           'display': self.display,
           'chartSelector': "#vis_%s svg" % self.fe_identifier
        }
        final_data = super_data.copy()
        final_data.update(data)
        return final_data

    class Meta:
        abstract = True
        verbose_name = _("Bar chart")
        verbose_name_plural = _("Bar charts")
