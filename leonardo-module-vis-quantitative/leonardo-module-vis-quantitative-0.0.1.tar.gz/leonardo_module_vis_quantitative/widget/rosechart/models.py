
from django.utils.translation import ugettext_lazy as _

from django.db import models

from leonardo_module_vis_quantitative.models import NumericWidget


class RoseChartWidget(NumericWidget):
    """
    Widget which shows time series in rose chart.
    """

    doughnut_ration = models.IntegerField()

    class Meta:
        abstract = True
        verbose_name = _("Rose chart")
        verbose_name_plural = _("Rose charts")
