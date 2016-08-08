import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from draw_helper import get_color, get_hatch, get_marker, to_percent, to_scf, label_all
from matplotlib.ticker import FuncFormatter, MultipleLocator


def make_fig(large):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    if large:
        fig, ax = plt.subplots(1, 1, sharex=True, figsize=(18, 3))
        return fig, ax
    else:
        fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4))
        return fig, ax


def output(fig, path):
    fig.savefig(path, format='pdf', dpi=1000, bbox_inches='tight')


def draw_stack(fig, ax, data, legends, xaxis, y_name, **kwargs):
    benches = len(data[0])
    bars = len(data)
    ind = np.arange(start=0, stop=benches*3, step=3)
    width = 3.0/(2)
    for i in range(bars):
        ax.bar(ind + width/2.0,
               data[i],
               width,
               color=kwargs.setdefault('color', 'w'),
               bottom=np.sum(data[:i], axis=0),
               edgecolor=get_color(i),
               hatch=get_hatch(i),
               label=legends[i])
    ax.set_ylabel(y_name)
    ax.set_xticks(ind+bars/2.0*width)
    fig.gca().set_ylim(kwargs.setdefault('y_start', 0), kwargs.setdefault('y_end', 1.2))
    fig.gca().set_xlim(0, benches*3)
    ax.set_xticklabels(
        xaxis,
        rotation=kwargs.setdefault('rotate', 0),
        fontsize=kwargs.setdefault('xaxis_fs', 9),
        va=kwargs.setdefault('xaxis_va', 'top'),
        ha=kwargs.setdefault('xaxis_ha', 'center'))
    ax.legend(ncol=kwargs.setdefault('lgd_col', '8'),
              bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 0.99999, 1., .105)),
              fontsize=kwargs.setdefault('lgd_fs', 9),
              loc='upper center')
    if kwargs.setdefault('use_percent', '0'):
        formatter = FuncFormatter(to_percent)
        fig.gca().yaxis.set_major_formatter(formatter)


def draw_hist(fig, ax, data, legends, xaxis, y_name, **kwargs):
    benches = len(data[0])
    bars = len(data)
    ind = np.arange(start=0, stop=benches*3, step=3)
    width = 3.0/(bars+2)
    rects = []
    for i in range(bars):
        tmp = ax.bar(ind+i*width+width,
                     data[i],
                     width,
                     color=kwargs.setdefault('color', 'w'),
                     edgecolor=get_color(i),
                     hatch=get_hatch(i),
                     linewidth=1,
                     label=legends[i])
        rects.append(tmp)
    ax.set_ylabel(y_name)
    ax.set_xticks(ind+bars/2.0*width+width)
    fig.gca().set_ylim(kwargs.setdefault('y_start', 0), kwargs.setdefault('y_end', 1.2))
    fig.gca().set_xlim(0, benches*3)
    ax.set_xticklabels(
        xaxis,
        rotation=kwargs.setdefault('rotate', 0),
        fontsize=kwargs.setdefault('xaxis_fs', 9),
        va=kwargs.setdefault('xaxis_va', 'top'),
        ha=kwargs.setdefault('xaxis_ha', 'center'))
    ax.legend(ncol=kwargs.setdefault('lgd_col', '8'),
              bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1.02, 1., .102)),
              fontsize=kwargs.setdefault('lgd_fs', 9),
              loc='upper center')
    if kwargs.setdefault('use_percent', '0'):
        formatter = FuncFormatter(to_percent)
        # Set the formatter
        fig.gca().yaxis.set_major_formatter(formatter)
    if kwargs.setdefault('use_labelall', 0):
        for rect in rects:
            label_all(ax, rect, kwargs.setdefault('use_labelall_rotate', 0), kwargs.setdefault('use_labelall_percent', 0), kwargs.setdefault('use_labelall_space', 0.05), kwargs.setdefault('y_end', 1.2))


def draw_hist_err(fig, ax, data, legends, xaxis, y_name, **kwargs):
    benches = len(data[0])
    bars = len(data)
    ind = np.arange(start=0, stop=benches*3, step=3)
    width = 3.0/(bars+2)
    for i in range(bars/2):
        ax.bar(ind+i*width+width,
               data[i],
               width,
               color=kwargs.setdefault('color', 'w'),
               edgecolor=get_color(i),
               hatch=get_hatch(i),
               yerr=data[bars/2+i],
               label=legends[i])
    ax.set_ylabel(y_name)
    ax.set_xticks(ind+bars/2.0*width+width)
    fig.gca().set_ylim(kwargs.setdefault('y_start', 0), kwargs.setdefault('y_end', 1.2))
    fig.gca().set_xlim(0, benches*3)
    ax.set_xticklabels(
        xaxis,
        rotation=kwargs.setdefault('rotate', 0),
        fontsize=kwargs.setdefault('xaxis_fs', 9),
        va=kwargs.setdefault('xaxis_va', 'top'),
        ha=kwargs.setdefault('xaxis_ha', 'center'))
    ax.legend(ncol=kwargs.setdefault('lgd_col', '8'),
              bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1.02, 1., .102)),
              fontsize=kwargs.setdefault('lgd_fs', 9),
              loc='upper center')
    if kwargs.setdefault('use_percent', '0'):
        formatter = FuncFormatter(to_percent)
        fig.gca().yaxis.set_major_formatter(formatter)


def draw_one_cdf(fig, ax, data, one_legend, xaxis, y_name, id, **kwargs):
    n_bins = 10000
    ax.hist(data,
            n_bins,
            normed=1,
            histtype='step',
            cumulative=True,
            edgecolor=get_color(id),
            linewidth=kwargs.setdefault('lw', 1.5),
            label=one_legend)
    ax.set_ylabel(y_name)
    fig.gca().set_ylim(kwargs.setdefault('y_start', 0), kwargs.setdefault('y_end', 1.2))
    fig.gca().set_xlim(kwargs.setdefault('x_start', 0), kwargs.setdefault('x_end', np.max(data)))
    ax.legend(ncol=kwargs.setdefault('lgd_col', '8'),
              bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1.00, 1., .101)),
              fontsize=kwargs.setdefault('lgd_fs', 9),
              loc='upper center')
    if kwargs.setdefault('use_percent', '0'):
        formatter = FuncFormatter(to_percent)
        fig.gca().yaxis.set_major_formatter(formatter)


def draw_cdf(fig, ax, data, legends, xaxis, y_name, **kwargs):
    lines = len(data)
    n_bins = 10000
    for i in range(lines):
        ax.hist(data[i],
                n_bins,
                normed=1,
                histtype='step',
                cumulative=True,
                edgecolor=get_color(i),
                linewidth=kwargs.setdefault('lw', 1.5),
                label=legends[i])
    ax.set_ylabel(y_name)
    fig.gca().set_ylim(kwargs.setdefault('y_start', 0), kwargs.setdefault('y_end', 1.2))
    fig.gca().set_xlim(kwargs.setdefault('x_start', 0), kwargs.setdefault('x_end', np.max(data)))
    ax.legend(ncol=kwargs.setdefault('lgd_col', '8'),
              bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1.00, 1., .101)),
              fontsize=kwargs.setdefault('lgd_fs', 9),
              loc='upper center')
    if kwargs.setdefault('use_percent', '0'):
        formatter = FuncFormatter(to_percent)
        fig.gca().yaxis.set_major_formatter(formatter)


def draw_line(fig, ax, data, legends, xaxis, y_name, **kwargs):
    benches = 0
    lines = len(data)
    for i in range(len(data)):
        if benches < len(data[i]):
            benches = len(data[i])
    xticks = np.arange(0, (benches+2), 1)
    indi = xticks[1:-1] - 0.5
    for i in range(lines):
        ax.plot(indi[:len(data[i])],
                data[i],
                color=get_color(i),
                linestyle=kwargs.setdefault('ls', '-'),
                linewidth=kwargs.setdefault('lw', 1.0),
                marker=get_marker(i),
                markersize=kwargs.setdefault('mrk_size', 5),
                markevery=kwargs.setdefault('mrk_inv', 1),
                label=legends[i])
    ax.set_ylabel(y_name)
    fig.gca().set_xlim(0, benches)
    fig.gca().set_ylim(kwargs.setdefault('y_start', 0), kwargs.setdefault('y_end', 1.2))
    ax.set_xticks(indi)
    ax.set_xticklabels(xaxis,
                       rotation=kwargs.setdefault('rotate', 0),
                       fontsize=kwargs.setdefault('xaxis_fs', 9),
                       va=kwargs.setdefault('xaxis_va', 'top'),
                       ha=kwargs.setdefault('xaxis_ha', 'center'))
    legend = ax.legend(ncol=4,
                       bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1.02, 1., .102)),
                       fontsize=9,
                       loc='upper center')
    legend.get_frame().set_zorder(20)
    if kwargs.setdefault('use_percent', '0'):
        formatter = FuncFormatter(to_percent)
        # Set the formatter
        plt.gca().yaxis.set_major_formatter(formatter)


def draw_one_line(fig, ax, data, one_legend, xaxis, y_name, id, **kwargs):
    benches = 0
    if benches < len(data):
        benches = len(data)
    xticks = np.arange(0, (benches+2), 1)
    indi = xticks[1:-1] - 0.5
    ax.plot(indi[:len(data)],
            data,
            color=get_color(id),
            linestyle=kwargs.setdefault('ls', '-'),
            linewidth=kwargs.setdefault('lw', 1.0),
            marker=get_marker(id),
            markersize=kwargs.setdefault('mrk_size', 5),
            markevery=kwargs.setdefault('mrk_inv', 1),
            label=one_legend)
    ax.set_ylabel(y_name)
    fig.gca().set_xlim(0, benches)
    fig.gca().set_ylim(kwargs.setdefault('y_start', np.min(data)-1), kwargs.setdefault('y_end', np.max(data)+1))
    ax.set_xticks(indi[::kwargs.setdefault('xaxis_inv', 1)])
    xaxis = [int(i) for i in xaxis]
    xaxis[0] = 1
    ax.set_xticklabels(xaxis[::kwargs.setdefault('xaxis_inv', 1)],
                       rotation=kwargs.setdefault('xaxis_rotate', 0),
                       fontsize=kwargs.setdefault('xaxis_fs', 9),
                       va=kwargs.setdefault('xaxis_va', 'top'),
                       ha=kwargs.setdefault('xaxis_ha', 'center'))
    legend = ax.legend(ncol=4,
                       bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1.02, 1., .102)),
                       fontsize=9,
                       loc='upper center')
    legend.get_frame().set_zorder(20)
    if kwargs.setdefault('use_percent', '0'):
        formatter = FuncFormatter(to_percent)
        # Set the formatter
        plt.gca().yaxis.set_major_formatter(formatter)
