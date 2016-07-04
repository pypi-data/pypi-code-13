
import time
import json

from django.db import models
from django.utils.translation import ugettext_lazy as _

from leonardo_module_vis_quantitative.models import TimeSeriesWidget


class CalendarHeatmapWidget(TimeSeriesWidget):
    """
    Widget which shows time-series data in calendar heat-map.
    """

    interpolation = models.CharField(max_length=55, verbose_name=_(
        "Interpolation"), default='linear', choices=INTERPOLATION_CHOICES)

    class Meta:
        abstract = True
        verbose_name = _("Calendar heatmap")
        verbose_name_plural = _("Calendar heatmaps")
