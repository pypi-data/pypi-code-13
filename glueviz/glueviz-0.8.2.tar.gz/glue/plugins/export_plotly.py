from __future__ import absolute_import, division, print_function

import logging

import numpy as np

try:
    from plotly import plotly
except ImportError:
    plotly = None

from glue.config import settings
from glue.external.qt import QtGui
from glue.core.layout import Rectangle, snap_to_grid
from glue.utils.qt.widget_properties import TextProperty

SYM = {'o': 'circle', 's': 'square', '+': 'cross', '^': 'triangle-up',
       '*': 'cross'}


def _data(layer, component):
    """
    Extract the data associated with a Component

    For categorical components, extracts the categories and not
    the remapped integers
    """
    result = layer[component]
    comp = layer.data.get_component(component)
    if comp.categorical:
        result = comp.categories[result.astype(np.int)]
    return result


def _sanitize(*arrs):
    mask = np.ones(arrs[0].shape, dtype=np.bool)
    for a in arrs:
        try:
            mask &= (~np.isnan(a))
        except TypeError:  # non-numeric dtype
            pass

    return tuple(a[mask].ravel() for a in arrs)


def _position_plots(viewers, layout):
    rs = [Rectangle(v.position[0], v.position[1],
                    v.viewer_size[0], v.viewer_size[1])
          for v in viewers]
    right = max(r.x + r.w for r in rs)
    top = max(r.y + r.h for r in rs)
    for r in rs:
        r.x = 1. * r.x / right
        r.y = 1. - 1. * (r.y + r.h) / top
        r.w = 1. * r.w / right
        r.h = 1. * r.h / top

    grid = snap_to_grid(rs, padding=0.05)
    grid = dict((v, grid[r]) for v, r in zip(viewers, rs))

    for i, plot in enumerate(viewers, 1):
        g = grid[plot]
        xdomain = [g.x, g.x + g.w]
        ydomain = [g.y, g.y + g.h]
        suffix = '' if i == 1 else str(i)

        xax, yax = 'xaxis' + suffix, 'yaxis' + suffix
        layout[xax].update(domain=xdomain, anchor=yax.replace('axis', ''))
        layout[yax].update(domain=ydomain, anchor=xax.replace('axis', ''))


def _stack_horizontal(layout):
    layout['xaxis']['domain'] = [0, 0.45]
    layout['xaxis2']['domain'] = [0.55, 1]
    layout['yaxis2']['anchor'] = 'x2'


def _grid_2x23(layout):
    opts = {
        'xaxis': {'domain': [0, 0.45]},
        'yaxis': {'domain': [0, 0.45]},
        'xaxis2': {"domain": [0.55, 1]},
        'yaxis2': {"domain": [0, 0.45],
                   "anchor": "x2"
                   },
        'xaxis3': {
            "domain": [0, 0.45],
            "anchor": "y3"
        },
        'yaxis3': {
            "domain": [0.55, 1],
        },
        'xaxis4': {
            "domain": [0.55, 1],
            "anchor": "y4",
        },
        'yaxis4': {
            "domain": [0.55, 1],
            "anchor": "x4"
        }
    }
    for k, v in opts.items():
        if k not in layout:
            continue
        layout[k].update(**v)


def _axis(log=False, lo=0, hi=1, title='', categorical=False):
    if log:
        if lo < 0:
            lo = 1e-3
        if hi < 0:
            hi = 1e-3
        lo = np.log10(lo)
        hi = np.log10(hi)

    result = dict(type='log' if log else 'linear',
                  rangemode='normal',
                  range=[lo, hi], title=title)

    if categorical:
        result.pop('type')
        # about 10 categorical ticks per graph
        result['autotick'] = False
        result['dtick'] = max(int(hi - lo) / 10, 1)

    return result


def _fix_legend_duplicates(traces, layout):
    """Prevent repeat entries in the legend"""
    seen = set()
    for t in traces:
        key = (t.get('name'), t.get('marker', {}).get('color'))
        if key in seen:
            t['showlegend'] = False
        else:
            seen.add(key)


def _color(style):
    r, g, b, a = style.rgba
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return 'rgba(%i, %i, %i, %0.1f)' % (r, g, b, a)


def export_scatter(viewer):
    """Export a scatter viewer to a list of
    plotly-formatted data dictionaries"""
    traces = []
    xatt, yatt = viewer.xatt, viewer.yatt
    xcat = ycat = False

    for layer in viewer.layers:
        if not layer.visible:
            continue
        l = layer.layer
        xcat |= l.data.get_component(xatt).categorical
        ycat |= l.data.get_component(yatt).categorical

        marker = dict(symbol=SYM.get(l.style.marker, 'circle'),
                      color=_color(l.style),
                      size=l.style.markersize)

        x, y = _sanitize(_data(l, xatt), _data(l, yatt))

        trace = dict(x=x, y=y,
                     type='scatter',
                     mode='markers',
                     marker=marker,
                     name=l.label)

        traces.append(trace)

    xaxis = _axis(log=viewer.xlog, lo=viewer.xmin, hi=viewer.xmax,
                  title=viewer.xatt.label, categorical=xcat)
    yaxis = _axis(log=viewer.ylog, lo=viewer.ymin, hi=viewer.ymax,
                  title=viewer.yatt.label, categorical=ycat)

    return traces, xaxis, yaxis


def export_histogram(viewer):
    traces = []
    att = viewer.component
    ymax = 1e-3
    for artist in viewer.layers:
        if not artist.visible:
            continue
        layer = artist.layer
        x, y = _sanitize(artist.x[:-1], artist.y)
        trace = dict(
            name=layer.label,
            type='bar',
            marker=dict(color=_color(layer.style)),
            x=x,
            y=y)
        traces.append(trace)
        ymax = max(ymax, artist.y.max())

    xlabel = att.label
    xmin, xmax = viewer.xmin, viewer.xmax
    if viewer.xlog:
        xlabel = 'Log ' + xlabel
        xmin = np.log10(xmin)
        xmax = np.log10(xmax)
    xaxis = _axis(lo=xmin, hi=xmax, title=xlabel)
    yaxis = _axis(log=viewer.ylog, lo=0 if not viewer.ylog else 1e-3,
                  hi=ymax * 1.05)

    return traces, xaxis, yaxis


def build_plotly_call(app):
    args = []
    layout = {'showlegend': True, 'barmode': 'overlay',
              'title': 'Autogenerated by Glue'}

    ct = 1
    for tab in app.viewers:
        for viewer in tab:
            if hasattr(viewer, '__plotly__'):
                p, xaxis, yaxis = viewer.__plotly__()
            else:
                assert type(viewer) in DISPATCH
                p, xaxis, yaxis = DISPATCH[type(viewer)](viewer)

            xaxis['zeroline'] = False
            yaxis['zeroline'] = False

            suffix = '' if ct == 1 else '%i' % ct
            layout['xaxis' + suffix] = xaxis
            layout['yaxis' + suffix] = yaxis
            if ct > 1:
                yaxis['anchor'] = 'x' + suffix
                for item in p:
                    item['xaxis'] = 'x' + suffix
                    item['yaxis'] = 'y' + suffix
            ct += 1
            args.extend(p)

    _position_plots([v for tab in app.viewers for v in tab], layout)
    _fix_legend_duplicates(args, layout)

    return [dict(data=args, layout=layout)], {}


def can_save_plotly(application):
    """
    Check whether an application can be exported to plotly

    Raises an exception if not
    """
    if not plotly:
        raise ValueError("Plotly Export requires the plotly python library. "
                         "Please install first")

    user = settings.PLOTLY_USER
    apikey = settings.PLOTLY_APIKEY
    if not user or not apikey:
        raise ValueError("Plotly username and API Key required. "
                         "Please enter them in File->Edit Settings")

    for tab in application.viewers:
        for viewer in tab:
            if hasattr(viewer, '__plotly__'):
                continue

            if not isinstance(viewer, (ScatterWidget, HistogramWidget)):
                raise ValueError("Plotly Export cannot handle viewer: %s"
                                 % type(viewer))

    if len(application.viewers) != 1:
        raise ValueError("Plotly Export only supports a single tab. "
                         "Please close other tabs to export")

    nplot = sum(len(t) for t in application.viewers)
    if nplot == 0:
        raise ValueError("Plotly Export requires at least one plot")

    if nplot > 4:
        raise ValueError("Plotly Export supports at most 4 plots")


def save_plotly(application, label):
    """Save a Glue session to a plotly plot

    This is currently restricted to 1-4 scatterplots or histograms

    :param application: Glue application to save
    :param label: Label for the exported plot
    """
    user = application.get_setting('PLOTLY_USER')
    apikey = application.get_setting('PLOTLY_APIKEY')

    args, kwargs = build_plotly_call(application)
    kwargs['filename'] = label

    logging.getLogger(__name__).debug(args, kwargs)

    plotly.sign_in(user, apikey)
    plotly.plot(*args, **kwargs)


class PlotlyPreferences(QtGui.QWidget):

    user = TextProperty('text_user')
    apikey = TextProperty('text_apikey')

    def __init__(self, parent=None):

        super(PlotlyPreferences, self).__init__(parent=parent)

        self.layout = QtGui.QFormLayout()

        self.text_user = QtGui.QLineEdit()
        self.text_apikey = QtGui.QLineEdit()

        self.layout.addRow("Plotly username", self.text_user)
        self.layout.addRow("Plotly API key", self.text_apikey)

        self.setLayout(self.layout)

        self.user = settings.PLOTLY_USER
        self.apikey = settings.PLOTLY_APIKEY


    def finalize(self):
        settings.PLOTLY_USER = self.user
        settings.PLOTLY_APIKEY = self.apikey


def setup():

    from glue.config import exporters, settings, preference_panes

    if not 'PLOTLY_USER' in settings:
        settings.add('PLOTLY_USER', 'Glue')

    if not 'PLOTLY_APIKEY' in settings:
        settings.add('PLOTLY_APIKEY', 't24aweai14')

    exporters.add('Plotly', save_plotly, can_save_plotly, outmode='label')

    preference_panes.add("Plotly", PlotlyPreferences)


if __name__ == "__main__":

    from glue.external.qt import get_qapp
    app = get_qapp()
    setup()
    widget = PlotlyPreferences()
    widget.show()
    widget.raise_()
    app.exec_()


DISPATCH = {}

try:
    from glue.viewers.scatter.qt import ScatterWidget
    from glue.viewers.histogram.qt import HistogramWidget
except ImportError:
    pass
else:
    DISPATCH[ScatterWidget] = export_scatter
    DISPATCH[HistogramWidget] = export_histogram
