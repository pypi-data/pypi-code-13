
from django.db import models
from leonardo.module.media.models import Vector
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from leonardo_module_vis_quantitative.models import NumericWidget


class IsotypeWidget(NumericWidget):
    """
    Widget which shows isotype pictogram grid.
    """

    icon = models.ForeignKey(
        Vector, blank=True, null=True, related_name="%(app_label)s_%(class)s_related")

    @cached_property
    def get_chart_params(self):
        super_data = super(NumericWidget, self).get_chart_params
        #import pdb; pdb.set_trace()
        data = {
           'chartSelector': "#vis_%s" % self.fe_identifier
        }
        if self.icon:
            data.update({'iconUrl': self.icon.url})
        final_data = super_data.copy()
        final_data.update(data)
        return final_data

    class Meta:
        abstract = True
        verbose_name = _("Isotype")
        verbose_name_plural = _("Isotypes")
