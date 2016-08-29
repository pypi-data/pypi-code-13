# amplikyzer2.graphics
# (c) Sven Rahmann, 2011--2013

"""
This module provides plotting routines for amplikyzer2.
It does not implement a subcommand.
"""

import sys


###################################################################################################
# safe import of plotting library

BACKENDS = dict(png="Agg", pdf="Agg", svg="svg")
_OUTPUT_FORMAT = None  # global memory of output format during initial import


def import_pyplot_with_format(output_format):
    """Import `matplotlib` with a format-specific backend;
    globally set `mpl` and `plt` module variables.
    """
    if _OUTPUT_FORMAT is None:
        _import_matplotlib(output_format)  # globally sets plt = matplotplib.pyplot
    if BACKENDS[output_format] != BACKENDS[_OUTPUT_FORMAT]:
        raise RuntimeError(
            "Cannot use different formats ({}/{}) in the same run.\n"
            "Please restart amplikyzer.".format(_OUTPUT_FORMAT, output_format))


def _import_matplotlib(output_format):
    global np, mpl, plt
    # using "pdf" (instead of "Agg") for pdf results in strange %-symbols
    import numpy as np
    import matplotlib as mpl
    mpl.use(BACKENDS[output_format])
    import matplotlib.pyplot as plt
    global _OUTPUT_FORMAT
    _OUTPUT_FORMAT = output_format


###################################################################################################
# # if creation of figures or axes is slow, pickling can be used instead
# import pickle
# from threading import Lock
#
#
# _figure_cache_lock = Lock()
#
#
# def _create_figure(rect, xticks=(), figure_cache=[]):
#     global _figure_cache_lock
#     if not figure_cache:
#         assert _OUTPUT_FORMAT is not None
#         fig = plt.figure()
#         ax = fig.add_axes(rect, xticks=[], yticks=[])
#     else:
#         with _figure_cache_lock:
#             pickled_figure = figure_cache[0]
#         fig = pickle.loads(pickled_figure)
#         ax = fig.get_axes()[0]
#         ax.set_position(rect)
#
#     num_xticks_old = len(ax.xaxis.get_major_ticks())
#     num_xticks_new = len(ax.set_xticks(xticks))
#
#     if (figure_cache is not None) and (num_xticks_new > num_xticks_old):
#         pickled_figure = pickle.dumps(fig, pickle.HIGHEST_PROTOCOL)
#         with _figure_cache_lock:
#             figure_cache[:] = [pickled_figure]
#
#     return fig, ax
#
# # xticks = range(n)
# # fig, ax = _create_figure([left, bottom, width, height], xticks=xticks)
#
#
###################################################################################################
# individual methylation plot

def plot_individual(analysis, fname, output_format="pdf", style="color", options=None):
    """Create and save an individual methylation plot.
    `analysis`:      an instance of `methylation.IndividualAnalysis`
    `fname`:         filename of the resulting image file
    `output_format`: image format (e.g., 'png', 'pdf', 'svg')
    `style`:         image style ('color' or 'bw')
    `options`:       options dictionary with the following keys:
      'show': `list` of xtick label types ["index", "position", "c-index", "coverage"]
      'dpi`:  dpi resolution of plots
    """
    import_pyplot_with_format(output_format)
    (dpi, xtick_types) = _get_options(options)
    # determine colormap
    if style == "color":
        colors = ["#3333ee", "#777777", "#cc4444"]  # (blue -> red)
    else:
        colors = ["#ffffff", "#000000"]
    colormap = mpl.colors.LinearSegmentedColormap.from_list("colormap", colors)

    # column-wise methylation rates
    m, n = analysis.shape

    (title_lines, subtitle) = analysis.get_titles()
    subtitle = ", ".join([subtitle, "{:.1%} methylation".format(analysis.total_meth_rate)])
    left = 0.05
    width = 0.9
    num_xtick_lines = len(xtick_types) * len(analysis.pattern) + 1
    xfontsize = max(2, 8 - (n // 11))
    fig, ax = _create_figure(title_lines, subtitle, left, width, num_xtick_lines, xfontsize)

    # There would be no need to shrink for PDFs, but libpng fails on very
    # large images. Furthermore a large amount of rows does not aid visual
    # perception and causes huge RAM consumption, so also cap the size here.
    # Size can be more generously chosen than for raster images to still
    # allow zoom and / or interpolation when viewing.
    # Depending on the PDF viewer the max displayable image height can be as
    # low as 32730 pixels => set 'sample_size' slightly below this limit.
    sample_size = 32000
    if output_format == "png":
        sample_size = int(fig.get_size_inches()[1] * dpi * ax.get_position().height)
    array = analysis.as_matrix(sample_size, average=False)
    _plot_image(ax, array, colormap)

    # NOTE: We might want to display the number of sampled reads like this:
    # if sample_size < m:
    #     ylabel = "{} ({} of {} shown)".format(ylabel, sample_size, m)
    # NOTE: This description would not be accurate if we opt to compute averages!
    ax.set_ylabel("individual reads")
    ax.set_yticks([])  # no yticks

    _add_xlabels(
        ax, analysis, analysis.meth_rates, "methylation rates",
        xtick_types, xfontsize)
    _save_figure(fig, fname, output_format, dpi)


###################################################################################################
# comparative methylation plot

def plot_comparative(analysis, fname, output_format="pdf", style="color", options=None):
    """Create and save a comparative methylation plot.

    `analysis`:      an instance of `methylation.ComparativeAnalysis`
    `fname:`         filename of the resulting image file
    `output_format:` image format (e.g., 'png', 'pdf', 'svg')
    `style:`         image style ('color' or 'bw')
    `options`:       options dictionary with the following keys:
      'show': `list` of xtick label types ["index", "position", "c-index", "coverage"]
      'dpi`:  dpi resolution of plots
    """
    if analysis.meth_positions is None:
        return  # inconsistent CpGs / GpCs

    import_pyplot_with_format(output_format)
    (dpi, xtick_types) = _get_options(options)
    # determine colormap
    if style == "color":
        def fontcolor(meth_rate):
            return "#ffffff"
        colors = ["#4444dd", "#dd4444"]  # (blue -> red)
    else:
        def fontcolor(meth_rate):
            return "#ffffff" if meth_rate > 0.5 else "#000000"
        colors = ["#ffffff", "#000000"]  # (white -> black)
    colormap = mpl.colors.LinearSegmentedColormap.from_list("colormap", colors)

    # column-wise methylation rates
    m, n = analysis.shape
    assert n is not None
    array = analysis.as_matrix()

    (title_lines, subtitle) = analysis.get_titles()
    # if there is not enough space for labels at the left side,
    # increase the 'left' coordinate and reduce the 'width' in the following line
    left = 0.14
    width = 0.84
    # if m >= 24:  # center plot since we put total_meth_rate and nreads on right axis
    right = ((1.0 - width) - left)
    width = width - max(0, left - right)
    num_xtick_lines = len(xtick_types) * len(analysis.pattern) + 1
    xfontsize = max(2, 8 - (n // 11))
    yfontsize = max(2, 8 - (m // 16))
    fig, ax = _create_figure(title_lines, subtitle, left, width, num_xtick_lines, xfontsize)

    _plot_image(ax, array, colormap)
    lfontsize = min(xfontsize, yfontsize)
    for i in range(m):
        for j in range(n):
            x = array[i, j]
            x_text = "{:3.0%}".format(x)
            x_color = fontcolor(x)
            ax.text(j, i, x_text, fontsize=lfontsize, color=x_color, ha="center", va="center")

    yticklabels1 = list(analysis.sample_names())
    yticklabels2 = ["{:.1%} ({:d})".format(s.total_meth_rate, s.nreads) for s in analysis._samples]
    # if m < 24:
    #     yticklabels = ["\n".join(ys) for ys in zip(yticklabels1, yticklabels2)]
    #     ax.set_yticklabels(yticklabels, fontsize=yfontsize)
    #     title_x = 0.54  # was the previous value for the right-adjusted / asymmetric plots

    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax.set_yticks(range(m))
    ax2.set_yticks(range(m))
    ax.set_yticklabels(yticklabels1, fontsize=yfontsize)
    ax2.set_yticklabels(yticklabels2, fontsize=yfontsize)

    _add_xlabels(
        ax, analysis, np.mean(array, axis=0), "average methylation rates",
        xtick_types, xfontsize)
    _save_figure(fig, fname, output_format, dpi)


###################################################################################################
# common functions used by both `plot_individual` and `plot_comparative`

def _get_options(options):
    """Extract 'dpi' and 'show' options from dict `options`."""
    if options is None:
        options = dict()
    dpi = options.get("dpi", 300)
    xtick_types = options.get("show", ["index"])
    return dpi, xtick_types


def _create_figure(title_lines, subtitle, left, width, num_xtick_lines, xfontsize):
    """Create and return a `matplotlib` `Figure` with an `Axis` to plot in.

    Add `title_lines` and `subtitle` to figure and position the plot under them while leaving
    enough space for `num_xtick_lines` xtick lines with font size `xfontsize` and the xlabel.
    `left` and `width` define the plot's horizontal positioning.
    """
    height = 0.87
    height -= 0.03 * len(title_lines)
    height -= 0.022 * num_xtick_lines * (xfontsize / 8)
    bottom = 0.06 + 0.022 * num_xtick_lines * (xfontsize / 8)
    title_fontsize = 14
    subtitle_fontsize = 12

    fig = plt.figure()
    ax = fig.add_axes([left, bottom, width, height])
    fig.suptitle("\n".join(title_lines), fontsize=title_fontsize)
    ax.set_title(subtitle, fontsize=subtitle_fontsize)
    return fig, ax


def _plot_image(ax, array, colormap):
    """Plot `array` (matrix of methylation rates [0..1]) with `colormap` to `ax`."""
    if array.size > 0:
        ax.imshow(array, origin="upper", cmap=colormap, interpolation="none", vmin=0.0, vmax=1.0)
    ax.set_aspect("auto")


def _add_xlabels(ax, analysis, meth_rates, meth_rates_label, xtick_types, xfontsize):
    """Add label and ticklabels to x-axis of `ax`."""
    (xlabel, xtick_lines) = _get_xlabels(analysis, meth_rates_label, meth_rates, xtick_types)
    ax.set_xlabel(xlabel)
    xticklabels = ["\n".join(xs) for xs in zip(*xtick_lines)]
    ax.set_xticks(range(len(xticklabels)))
    ax.set_xticklabels(xticklabels, fontsize=xfontsize)
    if len(analysis.pattern) > 1:
        _add_pattern_labels(ax, analysis, xtick_types, xfontsize)


def _get_xlabels(analysis, meth_rates_label, meth_rates, xtick_types):
    """Return label and ticklabels for x-axis."""
    xlabel_dict = {
        "index": "ranks",
        "position": "positions",
        "c-index": "cytosine ranks",
        "coverage": "coverage [%]"}
    xtick_lines = [["{:.0%}".format(m) for m in meth_rates]]
    xtick_lines.extend(analysis.format_column_headers(xtick_types, blank="$-$"))
    xlabels = ["{} [%]".format(meth_rates_label)]
    xlabels.extend(xlabel_dict[t] for t in xtick_types)

    xlabel = "{} of {}".format(
        " / ".join(xlabels),
        " / ".join(["{}s".format(p.text) for p in analysis.pattern]))
    return xlabel, xtick_lines


def _add_pattern_labels(ax, analysis, xtick_types, xfontsize):
    """Add pattern labels to the left of xticklabels. Use to distinguish different patterns."""
    xticktext = list(next(zip(*analysis.format_column_headers(xtick_types, firstcolumn=True))))
    xticktext = "\n".join([""] + xticktext)
    fig = ax.figure
    fig.draw(fig.canvas.get_renderer())
    xticklabels = ax.get_xticklabels()[0]
    _, y = xticklabels.get_transform().transform(xticklabels.get_position())
    x, _ = ax.transAxes.transform((0, 0))
    x, y = fig.transFigure.inverted().transform([x, y])
    fig.text(x, y, xticktext, ha='right', va='top', fontsize=xfontsize)


def _save_figure(fig, fname, output_format, dpi):
    # save to file
    if fname == "-":
        fname = sys.stdout
    fig.savefig(fname, format=output_format, dpi=dpi)  # bbox_inches="tight" cuts off title!
    plt.close(fig)
