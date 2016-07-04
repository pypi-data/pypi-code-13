
from django.utils.translation import ugettext_lazy as _

from leonardo_module_vis_quantitative.models import TimeSeriesWidget


class TimeTableWidget(TimeSeriesWidget):
    """
    Widget which shows time-series data in tabular format.
    """

    class Meta:
        abstract = True
        verbose_name = _("Time table")
        verbose_name_plural = _("Time tables")
