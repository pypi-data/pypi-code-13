
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from leonardo_module_vis_quantitative.models import NumericWidget


DISPLAY_CHOICES = (
    ('linear', _('Linear')),
    ('radial', _('Radial')),
)


class ProgressBarWidget(NumericWidget):
    """
    Widget which shows progress bar.
    """

    display = models.CharField(max_length=55, verbose_name=_(
        "Display style"), default='radial', choices=DISPLAY_CHOICES)

    @cached_property
    def get_chart_params(self):

        super_data = super(NumericWidget, self).get_chart_params
        data = {
           'display': self.display,
           'series': self.get_charts()
        }
        final_data = super_data.copy()
        final_data.update(data)
        return final_data

    def get_charts(self):
        metrics = self.get_metrics()
        charts = []
        for metric in metrics:
            charts.append(self.create_chart_from_metric(metric))
        return charts

    def create_chart_from_metric(self, metric):
        return {
            "labelStart": metric["name"],
            "value": 0,
            "display":10
        }

    class Meta:
        abstract = True
        verbose_name = _("Progress bar")
        verbose_name_plural = _("Progress bars")
