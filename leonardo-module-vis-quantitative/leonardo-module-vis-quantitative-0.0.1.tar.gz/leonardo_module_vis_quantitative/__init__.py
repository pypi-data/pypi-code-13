
from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig

public = True

default_app_config = 'leonardo_module_vis_quantitative.Config'

LEONARDO_OPTGROUP = 'Quantitative Visualizations'

LEONARDO_PUBLIC = True

LEONARDO_JS_FILES = [
    'vis/js/charts/chart.js',
#    'vendor/js/d3pie.js',
    'vendor/js/nvd3.js',
    'vendor/js/cubism.js',
    'vendor/js/cal-heatmap.js',
    'vendor/js/radial-progress-chart.js',
    'vendor/js/imagesloaded.pkgd.min.js',
    'vendor/js/jquery.animateNumber.min.js'
]

LEONARDO_SCSS_FILES = [
    'vis/scss/gauge.scss',
    'vis/scss/isotype.scss',
    'vendor/scss/cal-heatmap.scss',
    'vendor/scss/nvd3.scss',
    'vendor/css/cubism.css'
]

LEONARDO_APPS = [
    'leonardo_module_vis_quantitative',
]

LEONARDO_WIDGETS = [
    'leonardo_module_vis_quantitative.widget.angulargauge.models.AngularGaugeWidget',
    'leonardo_module_vis_quantitative.widget.areachart.models.AreaChartWidget',
    'leonardo_module_vis_quantitative.widget.barchart.models.BarChartWidget',
    'leonardo_module_vis_quantitative.widget.donutchart.models.DonutChartWidget',
    'leonardo_module_vis_quantitative.widget.horizonchart.models.HorizonChartWidget',
    'leonardo_module_vis_quantitative.widget.isotype.models.IsotypeWidget',
    'leonardo_module_vis_quantitative.widget.linechart.models.LineChartWidget',
    'leonardo_module_vis_quantitative.widget.progressbar.models.ProgressBarWidget',
    'leonardo_module_vis_quantitative.widget.systemchart.models.SystemChartWidget',
    'leonardo_module_vis_quantitative.widget.textnumber.models.TextNumberWidget',
    'leonardo_module_vis_quantitative.widget.timetable.models.TimeTableWidget',
]


LEONARDO_PLUGINS = [
    ('leonardo_module_vis_quantitative.apps.data', 'Vislab: Data View'),
]


class Config(AppConfig):

    name = 'leonardo_module_vis_quantitative'
    verbose_name = _(LEONARDO_OPTGROUP)
