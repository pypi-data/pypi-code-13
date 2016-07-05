#
# The MIT License (MIT)
#
# Copyright (c) 2015 Matthew Antalek Jr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import matplotlib.pyplot as pylab
import matplotlib as mpl
import scipy.cluster.hierarchy as sch
import numpy as np
import random
import functools
from colour import Color


class DendroHeatMap(object):
    """
    Class for quickly and easily plotting heatmaps with dendrograms on the side, as seen in
    http://code.activestate.com/recipes/578175-hierarchical-clustering-heatmap-python/
    """

    def __init__(self, heat_map_data=None, left_dendrogram=None, top_dendrogram=None, margins=(0.05, 0.05, 0.05, 0.05),
                 dendrogram_heights=(0.2, 0.2), dendrogram_margins=(0.02, 0.02), window_size="auto",
                 color_bar_width=0.015, color_bars_displayed=False,
                 heatmap_colors=('blue', 'black', 'red'), cluster_colors=(
            "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00"),
                 color_legend_displayed=True, color_legend_x=0.07, color_legend_y=0.88, color_legend_width=0.2,
                 color_legend_height=0.09,
                 color_legend_ticks=7, left_dendrogram_displayed=True, top_dendrogram_displayed=True,
                 row_labels=None, col_labels=None, max_row_labels=100, label_size=12, label_color='black',
                 label_family='monospace',
                 max_col_labels=100, dendrogram_color='black', heatmap_norm=None, left_clusters=None,
                 right_clusters=None,
                 verbose=False):

        self.figure = None
        self.verbose = verbose

        self.heatmap_norm = heatmap_norm
        self.heat_map_data = heat_map_data
        self.top_dendrogram = top_dendrogram
        self.left_dendrogram = left_dendrogram

        self.window_size = window_size
        if window_size == "auto":
            self.window_width = len(heat_map_data) / 2.0
            self.window_height = len(heat_map_data) / 2.0
        else:
            assert type(window_size) == list or type(window_size) == tuple
            self.window_height = window_size[1]
            self.window_width = window_size[0]
        self.color_bar_width = color_bar_width

        self.margin_left = margins[0]
        self.margin_top = margins[1]
        self.margin_right = margins[2]
        self.margin_bottom = margins[3]
        self.dendrogram_left_width = dendrogram_heights[0]
        self.dendrogram_top_height = dendrogram_heights[1]
        self.dendrogram_left_margin = dendrogram_margins[0]
        self.dendrogram_top_margin = dendrogram_margins[0]

        self.dendrogram_color = dendrogram_color
        self.dendrogram_left_clusters = left_clusters
        self.dendrogram_top_clusters = right_clusters
        self.dendrogram_left_root, self.dendrogram_left_tree_map = (
        None, None) if left_dendrogram is None else sch.to_tree(left_dendrogram, True)
        self.dendrogram_top_root, self.dendrogram_top_tree_map = (
        None, None) if top_dendrogram is None else sch.to_tree(top_dendrogram, True)
        self.dendrogram_left_displayed = left_dendrogram_displayed
        self.dendrogram_top_displayed = top_dendrogram_displayed

        assert type(cluster_colors) == list or type(cluster_colors) == tuple
        cluster_colors = list(cluster_colors)
        random.shuffle(cluster_colors)

        self.cluster_colors = cluster_colors
        self.cluster_cb_colors = mpl.colors.ListedColormap(cluster_colors)

        self.color_legend_displayed = color_legend_displayed
        self.color_legend_x = color_legend_x
        self.color_legend_y = color_legend_y
        self.color_legend_width = color_legend_width
        self.color_legend_height = color_legend_height
        self.color_legend_ticks = color_legend_ticks

        self.color_bars_displayed = color_bars_displayed

        self.label_family = label_family
        self.label_color = label_color
        self.row_labels = row_labels
        self.label_size = label_size
        self.max_row_labels = max_row_labels
        self.col_labels = col_labels
        self.max_col_labels = max_col_labels

        color_cold = Color(heatmap_colors[0])
        color_neutral = Color(heatmap_colors[1])
        color_hot = Color(heatmap_colors[2])

        self.colormap = DendroHeatMap.__createColorMap(color_cold, color_neutral, color_hot)

        self.left_dendro_title = ''
        self.top_dendro_title = ''
        self.title = ''
        self.color_legend_title = ''
        self.plotRendered = False

        self.exportDPI = 600

    def __link_color_func(self, linkage_id, clusters, tree_map):
        if self.dendrogram_top_clusters != None:
            tree = tree_map[linkage_id]
            children = tree.pre_order(lambda x: x.id)
            assert len(children) > 0
            cluster_id = clusters[children[0]]
            isUnified = all(map(lambda x: clusters[x] == cluster_id, tree.pre_order(lambda x: x.id)))

            if isUnified:
                return self.cluster_colors[cluster_id % len(self.cluster_colors)]

        return self.dendrogram_color

    def analyze_clusters(self, threshold=0.5):
        if self.left_dendrogram is not None:
            self.dendrogram_left_clusters = sch.fcluster(self.left_dendrogram, threshold)

        if self.top_dendrogram is not None:
            self.dendrogram_top_clusters = sch.fcluster(self.top_dendrogram, threshold)

    def render_plot(self, showFrames=False):
        self.resetPlot()

        if (self.verbose):
            print 'Rendering plot...'

        self.figure = pylab.figure(figsize=[self.window_width, self.window_height])

        # plot the top dendrogram
        if (not self.top_dendrogram is None and self.dendrogram_top_displayed):
            self.top_dendro_axes = self.figure.add_axes(
                    [self.margin_left + ((
                                         self.dendrogram_left_width + self.dendrogram_left_margin) if self.dendrogram_left_displayed else 0),
                     self.margin_bottom + self.heatmap_height + self.dendrogram_top_margin, self.dendrogram_top_width,
                     self.dendrogram_top_height],
                    frame_on=showFrames)

            self.top_dendro_plot = sch.dendrogram(self.top_dendrogram,
                                                  link_color_func=lambda x: self.__link_color_func(x,
                                                                                                   self.dendrogram_top_clusters,
                                                                                                   self.dendrogram_top_tree_map),
                                                  ax=self.top_dendro_axes)
            self.top_dendro_axes.set_xticks([])
            self.top_dendro_axes.set_yticks([])
            self.top_dendro_axes.set_title(self.top_dendro_title)

        # plot the left dendrogram
        if (not self.left_dendrogram is None and self.dendrogram_left_displayed):
            self.left_dendro_axes = self.figure.add_axes(
                    [self.margin_left, self.margin_bottom, self.dendrogram_left_width, self.dendrogram_left_height],
                    frame_on=showFrames)

            self.left_dendro_plot = sch.dendrogram(self.left_dendrogram, orientation='right',
                                                   link_color_func=lambda x: self.__link_color_func(x,
                                                                                                    self.dendrogram_left_clusters,
                                                                                                    self.dendrogram_left_tree_map),
                                                   ax=self.left_dendro_axes)
            self.left_dendro_axes.set_xticks([])
            self.left_dendro_axes.set_yticks([])
            self.left_dendro_axes.set_title(self.left_dendro_title, rotation='vertical')

        # plot the heat map
        if (not self.heat_map_data is None):
            hm_w, hm_h = self.heatmap_size
            self.heat_map_axes = self.figure.add_axes([self.margin_left + (
            (self.dendrogram_left_margin + self.dendrogram_left_width) if self.dendrogram_left_displayed else 0),
                                                       self.margin_bottom, hm_w, hm_h],
                                                      frame_on=showFrames)
            self.heat_map_plot = self.heat_map_axes.matshow(self.heat_map_data, aspect='auto', origin='upper',
                                                            cmap=self.colormap, norm=self.cmap_norm)

            if self.col_labels:
                self.heat_map_axes.set_xticks(range(len(self.heat_map_data)))
                self.heat_map_axes.set_xticklabels(self.col_labels, rotation=270, size=self.label_size,
                                                   color=self.label_color,
                                                   family=self.label_family)
            else:
                self.heat_map_axes.set_xticks([])

            if self.row_labels:
                self.heat_map_axes.set_yticks(range(len(self.heat_map_data)))
                self.heat_map_axes.set_yticklabels(self.row_labels, color=self.label_color,
                                                   size=self.label_size,
                                                   family=self.label_family)
            else:
                self.heat_map_axes.set_yticks([])

            self.heat_map_axes.xaxis.tick_bottom()
            self.heat_map_axes.yaxis.tick_right()
            self.heat_map_rows = self.heat_map_data.shape[0]
            self.heat_map_cols = self.heat_map_data.shape[1]

        # plot the column colorbar
        if (not self.top_dendrogram is None and self.color_bars_displayed):
            self.col_cb_axes = self.figure.add_axes(
                    [self.col_cb_x, self.col_cb_y, self.col_cb_width, self.col_cb_height], frame_on=True)
            # print self.top_colorbar_labels.shape
            # print 'Col cb'
            # print [self.col_cb_x, self.col_cb_y, self.col_cb_width, self.col_cb_height]
            self.col_cb_plot = self.col_cb_axes.matshow(self.top_colorbar_labels, aspect='auto', origin='lower',
                                                        cmap=self.cluster_cb_colors)
            self.col_cb_axes.set_xticks([])
            self.col_cb_axes.set_yticks([])

        # plot the row colorbar
        if (not self.left_dendrogram is None and self.color_bars_displayed):
            self.row_cb_axes = self.figure.add_axes(
                    [self.row_cb_x, self.row_cb_y, self.row_cb_width, self.row_cb_height], frame_on=True)
            # print self.left_colorbar_labels.shape
            # print 'Row cb'
            # print [self.row_cb_x, self.row_cb_y, self.row_cb_width, self.row_cb_height]
            self.row_cb_plot = self.row_cb_axes.matshow(self.left_colorbar_labels, aspect='auto', origin='lower',
                                                        cmap=self.cluster_cb_colors)
            self.row_cb_axes.set_xticks([])
            self.row_cb_axes.set_yticks([])

        # plot the color legend
        if (not self.heat_map_data is None and self.color_legend_displayed):
            self.color_legend_axes = self.figure.add_axes(
                    [self.color_legend_x, self.color_legend_y, self.color_legend_width, self.color_legend_height],
                    frame_on=showFrames)
            self.color_legend_plot = mpl.colorbar.ColorbarBase(self.color_legend_axes, cmap=self.colormap,
                                                               norm=self.cmap_norm, orientation='horizontal')
            tl = mpl.ticker.MaxNLocator(nbins=self.color_legend_ticks)
            self.color_legend_plot.locator = tl
            self.color_legend_plot.update_ticks()
            self.color_legend_axes.set_title(self.color_legend_title)
            self.heat_map_axes.format_coord = self.__formatCoords

        self.figure.suptitle(self.title)

        self.plotRendered = True

        if (self.verbose):
            print 'Plot rendered...'

    def show(self):
        self.resetPlot()
        self.render_plot()
        pylab.show()

    def export(self, filename):
        self.resetPlot()
        if ('.' not in filename):
            filename += '.png'
        else:
            filename = filename[:-4] + '.png'

            if (self.verbose):
                print 'Saving plot to: ', filename
            self.render_plot()
            pylab.savefig(filename, dpi=self.exportDPI)

    @property
    def heat_map_data(self):
        return self.__heat_map_data

    @heat_map_data.setter
    def heat_map_data(self, heat_map_data):
        self.__heat_map_data = heat_map_data
        self.resetPlot()
        if ((isinstance(heat_map_data, np.ndarray)) | (isinstance(heat_map_data, np.matrix))):
            hm_min = heat_map_data.min()
            hm_max = heat_map_data.max()
            self.cmap_norm = mpl.colors.Normalize(hm_min, hm_max) if self.heatmap_norm is None else self.heatmap_norm
        else:
            raise TypeError('Data for the heatmap must be a numpy.ndarray or numpy.matrix object!')

    def resetPlot(self):
        self.plotRendered = False
        if (self.figure):
            pylab.close(self.figure)
            self.figure = None
        else:
            self.figure = None

    @property
    def figure(self):
        return self.__figure

    @figure.setter
    def figure(self, figure):
        self.__figure = figure
        if ((not isinstance(figure, pylab.Figure)) & (isinstance(figure, object))):
            # this force's the figure to either be "None" type or a pylab.Figure object
            self.__figure = None

    @property
    def row_labels(self):
        return self.__row_labels

    @row_labels.setter
    def row_labels(self, row_labels):
        if (not isinstance(self.heat_map_data, np.ndarray) or not isinstance(self.heat_map_data, np.matrix)):
            if (self.verbose):
                print """Warning: data for heat map not yet specified, be sure that the number of elements in row_labels
                is equal to the number of rows in heat_map_data.
                """
            self.__row_labels = row_labels
        else:
            if (len(row_labels) != self.heat_map_data.shape[0]):
                print """Invalid entry for row_labels. Please be sure that the number of elements in row_labels is equal
                to the number of rows in heat_map_data."""
                self.__row_labels = None
            else:
                self.__row_labels = row_labels

    @property
    def col_labels(self):
        return self.__col_labels

    @property
    def heatmap_size(self):
        return (1 - self.margin_left - self.margin_right - (
        (self.dendrogram_left_width - self.dendrogram_left_margin) if self.dendrogram_left_displayed else 0),
                1 - self.margin_top - self.margin_bottom - (
                (self.dendrogram_top_height - self.dendrogram_top_margin) if self.dendrogram_top_displayed else 0))

    @property
    def heatmap_height(self):
        return self.heatmap_size[1]

    @property
    def heatmap_width(self):
        return self.heatmap_size[0]

    @property
    def dendrogram_left_height(self):
        return self.heatmap_height

    @property
    def dendrogram_top_width(self):
        return self.heatmap_width

    @col_labels.setter
    def col_labels(self, col_labels):
        if (not isinstance(self.heat_map_data, np.ndarray) or not isinstance(self.heat_map_data, np.matrix)):
            if (self.verbose):
                print """Warning: data for heat map not yet specified, be sure that the number of elements in col_labels
                is equal to the number of columns in heat_map_data.
                """
            self.__col_labels = col_labels
        else:
            if (len(col_labels) != self.heat_map_data.shape[0]):
                print """Invalid entry for col_labels. Please be sure that the number of elements in col_labels is equal
                to the number of columns in heat_map_data."""
                self.__col_labels = None
            else:
                self.__col_labels = col_labels

    @property
    def colormap(self):
        return self.__colormap

    @colormap.setter
    def colormap(self, colormap):
        self.__colormap = colormap
        self.resetPlot()

    @property
    def top_dendrogram(self):
        return self.__top_dendrogram

    @top_dendrogram.setter
    def top_dendrogram(self, top_dendrogram):
        if (isinstance(top_dendrogram, np.ndarray)):
            self.__top_dendrogram = top_dendrogram
            self.resetPlot()
            self.top_colorbar_labels = np.array(
                    sch.fcluster(top_dendrogram, 0.7 * max(top_dendrogram[:, 2]), 'distance'), dtype=int)
            self.top_colorbar_labels.shape = (1, len(self.top_colorbar_labels))
            temp_dendro = sch.dendrogram(top_dendrogram, no_plot=True)
            self.top_colorbar_labels = self.top_colorbar_labels[:, temp_dendro['leaves']]
        elif top_dendrogram is None:
            self.__top_dendrogram = top_dendrogram
            self.resetPlot()
        else:
            raise TypeError(
                    'Dendrograms must be a n-1 x 4 numpy.ndarray as per the scipy.cluster.hierarchy implementation!')

    @property
    def left_dendrogram(self):
        return self.__left_dendrogram

    @left_dendrogram.setter
    def left_dendrogram(self, left_dendrogram):

        if isinstance(left_dendrogram, np.ndarray):
            self.__left_dendrogram = left_dendrogram
            self.resetPlot()
            self.left_colorbar_labels = np.array(
                    sch.fcluster(left_dendrogram, 0.7 * max(left_dendrogram[:, 2]), 'distance'), dtype=int)
            self.left_colorbar_labels.shape = (len(self.left_colorbar_labels), 1)
            temp_dendro = sch.dendrogram(left_dendrogram, no_plot=True)
            self.left_colorbar_labels = self.left_colorbar_labels[temp_dendro['leaves'], :]
        elif left_dendrogram is None:
            self.__left_dendrogram = left_dendrogram
            self.resetPlot()

        else:
            raise TypeError(
                    'Dendrograms must be a n-1 x 4 numpy.ndarray as per the scipy.cluster.hierarchy implementation!')

    @staticmethod
    def __createColorMap(cold, neutral, hot):
        def __createTuple(d, color, element='red'):
            degree = eval('color.{}'.format(element))
            return (d, degree, degree)

        def __createGradientTuples(c1, c2, c3, element='red'):
            return (__createTuple(0, c1, element),
                    __createTuple(0.5, c2, element),
                    __createTuple(1.0, c3, element))

        cdict = dict([(element, __createGradientTuples(cold, neutral, hot, element)) for element in
                      ["red", "green", "blue"]])
        return mpl.colors.LinearSegmentedColormap('custom_colormap', cdict, 256)

    def save(self, fname):
        self.resetPlot()
        self.render_plot()
        self.figure.savefig(fname)

    def __formatCoords(self, x, y):
        col = int(x + 0.5)
        row = int(y + 0.5)
        if col >= 0 and col < self.heat_map_cols and row >= 0 and row < self.heat_map_rows:
            z = self.heat_map_data[row, col]
            return 'x=%1.4f, y=%1.4f, z=%1.4f' % (x, y, z)
        else:
            return 'x=%1.4f, y=%1.4f' % (x, y)
