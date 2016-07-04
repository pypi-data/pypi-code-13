
from django.utils.translation import ugettext_lazy as _

from django.db import models

from leonardo_module_vis_quantitative.models import NumericWidget


class ScatterPlotWidget(NumericWidget):
    """
    Widget which shows time series in scatter plot.
    """

    doughnut_ration = models.IntegerField()

    class Meta:
        abstract = True
        verbose_name = _("Scatter plot")
        verbose_name_plural = _("Scatter plots")
