
from django.utils.translation import ugettext_lazy as _


from leonardo_module_vis_quantitative.models import TimeSeriesWidget


class RadarChartWidget(TimeSeriesWidget):
    """
    Widget which shows time series in radar chart.
    """

    class Meta:
        abstract = True
        verbose_name = _("Radar chart")
        verbose_name_plural = _("Radar charts")
