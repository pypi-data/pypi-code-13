import os

import numpy as np
from mock import patch, MagicMock
from matplotlib.colors import ColorConverter

from glue import custom_viewer
from glue.core import HubListener, Application, Data, DataCollection
from glue.core.message import SettingsChangeMessage
from glue.external.qt import QtGui
from glue.app.qt.preferences import PreferencesDialog
from glue.app.qt import GlueApplication
from glue.viewers.scatter.qt import ScatterWidget
from glue.viewers.image.qt import ImageWidget
from glue.viewers.histogram.qt import HistogramWidget
from glue.plugins.dendro_viewer.qt.viewer_widget import DendroWidget

rgb = ColorConverter().to_rgb


class TestPreferences():

    def setup_method(self, method):
        self.app = Application()

    def test_no_change(self):

        # If we don't change anything, settings should be preserved

        with patch('glue.config.settings') as settings:

            settings.FOREGROUND_COLOR = 'red'
            settings.BACKGROUND_COLOR = (0, 0.5, 1)
            settings.DATA_COLOR = (1, 0.5, 0.25)
            settings.DATA_ALPHA = 0.3

            dialog = PreferencesDialog(self.app)
            dialog.show()

            assert dialog.theme == 'Custom'

            dialog.accept()

            assert rgb(settings.FOREGROUND_COLOR) == (1, 0, 0)
            assert rgb(settings.BACKGROUND_COLOR) == (0, 0.5, 1)
            assert rgb(settings.DATA_COLOR) == (1, 0.5, 0.25)
            assert settings.DATA_ALPHA == 0.3

    def test_theme_autodetect(self):

        # If we don't change anything, settings should be preserved

        with patch('glue.config.settings') as settings:

            settings.FOREGROUND_COLOR = 'white'
            settings.BACKGROUND_COLOR = 'black'
            settings.DATA_COLOR = '0.75'
            settings.DATA_ALPHA = 0.8

            dialog = PreferencesDialog(self.app)
            dialog.show()
            assert dialog.theme == 'White on Black'
            dialog.accept()

            settings.FOREGROUND_COLOR = 'black'
            settings.BACKGROUND_COLOR = 'white'
            settings.DATA_COLOR = '0.35'
            settings.DATA_ALPHA = 0.8

            dialog = PreferencesDialog(self.app)
            dialog.show()
            assert dialog.theme == 'Black on White'
            dialog.accept()

    def test_themes(self):

        # Check that themes work

        with patch('glue.config.settings') as settings:

            settings.FOREGROUND_COLOR = 'red'
            settings.BACKGROUND_COLOR = (0, 0.5, 1)
            settings.DATA_COLOR = (1, 0.5, 0.25)
            settings.DATA_ALPHA = 0.3

            dialog = PreferencesDialog(self.app)
            dialog.show()
            dialog.theme = 'White on Black'
            dialog.accept()

            assert rgb(settings.FOREGROUND_COLOR) == (1, 1, 1)
            assert rgb(settings.BACKGROUND_COLOR) == (0, 0, 0)
            assert rgb(settings.DATA_COLOR) == (0.75, 0.75, 0.75)
            assert settings.DATA_ALPHA == 0.8

            dialog = PreferencesDialog(self.app)
            dialog.show()
            dialog.theme = 'Black on White'
            dialog.accept()

            assert rgb(settings.FOREGROUND_COLOR) == (0, 0, 0)
            assert rgb(settings.BACKGROUND_COLOR) == (1, 1, 1)
            assert rgb(settings.DATA_COLOR) == (0.35, 0.35, 0.35)
            assert settings.DATA_ALPHA == 0.8

    def test_custom_changes(self):

        # Check that themes work

        with patch('glue.config.settings') as settings:

            settings.FOREGROUND_COLOR = 'red'
            settings.BACKGROUND_COLOR = (0, 0.5, 1)
            settings.DATA_COLOR = (1, 0.5, 0.25)
            settings.DATA_ALPHA = 0.3

            dialog = PreferencesDialog(self.app)
            dialog.show()
            dialog.foreground = (0, 1, 1)
            dialog.accept()

            assert rgb(settings.FOREGROUND_COLOR) == (0, 1, 1)
            assert rgb(settings.BACKGROUND_COLOR) == (0, 0.5, 1)
            assert rgb(settings.DATA_COLOR) == (1, 0.5, 0.25)
            assert settings.DATA_ALPHA == 0.3

            dialog = PreferencesDialog(self.app)
            dialog.show()
            dialog.background = (1, 0, 1)
            dialog.accept()

            assert rgb(settings.FOREGROUND_COLOR) == (0, 1, 1)
            assert rgb(settings.BACKGROUND_COLOR) == (1, 0, 1)
            assert rgb(settings.DATA_COLOR) == (1, 0.5, 0.25)
            assert settings.DATA_ALPHA == 0.3

            dialog = PreferencesDialog(self.app)
            dialog.show()
            dialog.data_color = (1, 1, 0.5)
            dialog.accept()

            assert rgb(settings.FOREGROUND_COLOR) == (0, 1, 1)
            assert rgb(settings.BACKGROUND_COLOR) == (1, 0, 1)
            assert rgb(settings.DATA_COLOR) == (1, 1, 0.5)
            assert settings.DATA_ALPHA == 0.3

            dialog = PreferencesDialog(self.app)
            dialog.show()
            dialog.data_alpha = 0.4
            dialog.accept()

            assert rgb(settings.FOREGROUND_COLOR) == (0, 1, 1)
            assert rgb(settings.BACKGROUND_COLOR) == (1, 0, 1)
            assert rgb(settings.DATA_COLOR) == (1, 1, 0.5)
            assert settings.DATA_ALPHA == 0.4

    def test_custom_pane(self):

        settings = MagicMock()

        class CustomPreferences(QtGui.QWidget):

            def __init__(self, parent=None):

                super(CustomPreferences, self).__init__(parent=parent)

                self.layout = QtGui.QFormLayout()

                self.option1 = QtGui.QLineEdit()
                self.option2 = QtGui.QLineEdit()

                self.layout.addRow("Option 1", self.option1)
                self.layout.addRow("Option 2", self.option2)

                self.setLayout(self.layout)

            def finalize(self):
                settings.OPTION1 = "Monty"
                settings.OPTION2 = "Python"

        preference_panes = [('Custom', CustomPreferences)]

        with patch('glue.config.preference_panes', preference_panes):

            dialog = PreferencesDialog(self.app)
            dialog.show()
            dialog.accept()

            assert settings.OPTION1 == "Monty"
            assert settings.OPTION2 == "Python"

    def test_settings_change_message(self):

        # Make sure that a SettingsChangeMessage gets emitted when settings
        # change in the dialog

        class TestListener(HubListener):

            def __init__(self, hub):
                hub.subscribe(self, SettingsChangeMessage,
                              handler=self.receive_message)
                self.received = []

            def receive_message(self, message):
                self.received.append(message)

        listener = TestListener(self.app._hub)

        with patch('glue.config.settings') as settings:

            settings.FOREGROUND_COLOR = 'red'
            settings.BACKGROUND_COLOR = (0, 0.5, 1)
            settings.DATA_COLOR = (1, 0.5, 0.25)
            settings.DATA_ALPHA = 0.3

            dialog = PreferencesDialog(self.app)
            dialog.show()
            dialog.foreground = (0, 1, 1)
            dialog.accept()

        assert len(listener.received) == 1
        assert listener.received[0].settings == ('FOREGROUND_COLOR', 'BACKGROUND_COLOR')

    def test_save_to_disk(self, tmpdir):

        with patch('glue.config.settings') as settings:
            with patch('glue.config.CFG_DIR', tmpdir.strpath):

                settings.FOREGROUND_COLOR = 'red'
                settings.BACKGROUND_COLOR = (0, 0.5, 1)
                settings.DATA_COLOR = (1, 0.5, 0.25)
                settings.DATA_ALPHA = 0.3

                dialog = PreferencesDialog(self.app)
                dialog.show()
                dialog.save_to_disk = False
                dialog.accept()

                assert not os.path.exists(os.path.join(tmpdir.strpath, 'settings.cfg'))

                dialog = PreferencesDialog(self.app)
                dialog.show()
                dialog.save_to_disk = True
                dialog.accept()

                assert os.path.exists(os.path.join(tmpdir.strpath, 'settings.cfg'))


def assert_axes_background(axes, color):
    assert axes.patch.get_facecolor() == color
    assert axes.figure.get_facecolor() == color


def assert_axes_foreground(axes, color):

    if hasattr(axes, 'coords'):
        # TODO: fix this in WCSAxes
        assert axes.coords.frame._color == color
        for coord in axes.coords:
            assert coord.ticks.get_color() == color
            assert coord.ticklabels.get_color() == color
            assert coord.axislabels.get_color() == color
    else:
        for spine in axes.spines.values():
            assert spine.get_edgecolor() == color
        for tick in axes.xaxis.get_ticklines() + axes.yaxis.get_ticklines():
            assert tick.get_color() == color
        for label in axes.xaxis.get_ticklabels() + axes.yaxis.get_ticklabels():
            assert label.get_color() == color
        assert axes.xaxis.label.get_color() == color
        assert axes.yaxis.label.get_color() == color


def _generate_custom_viewer():

    example = custom_viewer('Test Plot', x='att(x)', y='att(y)')

    @example.plot_data
    def plot_data(axes, x, y, style):
        axes.plot(x, y)

    @example.plot_subset
    def plot_subset(axes, x, y, style):
        axes.plot(x, y)

    @example.setup
    def setup(axes):
        pass

    from glue.config import qt_client
    for viewer in qt_client.members:
        if viewer.LABEL == 'Test Plot':
            return viewer

    raise Exception("Failed to find custom viewer in qt_client")


def test_foreground_background_settings():

    d_1d = Data(x=np.random.random(100), y=np.random.random(100), label='Data 1d')
    d_2d = Data(x=np.random.random((100, 100)), y=np.random.random((100, 100)), label='Data 2d')

    dc = DataCollection([d_1d, d_2d])

    app = GlueApplication(dc)

    # Make sure that settings change existing viewers, so we create a bunch of
    # viewers here.

    scatter1 = app.new_data_viewer(ScatterWidget)
    scatter1.add_data(d_1d)

    image1 = app.new_data_viewer(ImageWidget)
    image1.add_data(d_2d)

    histogram1 = app.new_data_viewer(HistogramWidget)
    histogram1.add_data(d_1d)

    dendrogram1 = app.new_data_viewer(DendroWidget)

    example_custom = _generate_custom_viewer()

    custom1 = app.new_data_viewer(example_custom)

    RED = (1, 0, 0, 0.5)
    GREEN = (0, 1, 0, 0.6)

    app.show()

    with patch('glue.config.settings') as settings:

        settings.FOREGROUND_COLOR = 'black'
        settings.BACKGROUND_COLOR = 'white'
        settings.DATA_COLOR = '0.5'
        settings.DATA_ALPHA = 0.5

        dialog = PreferencesDialog(app)
        dialog.show()
        dialog.background = RED
        dialog.foreground = GREEN
        dialog.accept()

        assert_axes_background(scatter1.axes, RED)
        assert_axes_background(image1.axes, RED)
        assert_axes_background(histogram1.axes, RED)
        assert_axes_background(dendrogram1.axes, RED)
        assert_axes_background(custom1.axes, RED)

        assert_axes_foreground(scatter1.axes, GREEN)
        assert_axes_foreground(image1.axes, GREEN)
        assert_axes_foreground(histogram1.axes, GREEN)
        assert_axes_foreground(dendrogram1.axes, GREEN)
        assert_axes_foreground(custom1.axes, GREEN)

        # Now make sure that new viewers also inherit these settings

        scatter2 = app.new_data_viewer(ScatterWidget)
        scatter2.add_data(d_1d)

        image2 = app.new_data_viewer(ImageWidget)
        image2.add_data(d_2d)

        histogram2 = app.new_data_viewer(HistogramWidget)
        histogram2.add_data(d_1d)

        dendrogram2 = app.new_data_viewer(DendroWidget)
        custom2 = app.new_data_viewer(example_custom)

        assert_axes_background(scatter2.axes, RED)
        assert_axes_background(image2.axes, RED)
        assert_axes_background(histogram2.axes, RED)
        assert_axes_background(dendrogram2.axes, RED)
        assert_axes_background(custom2.axes, RED)

        assert_axes_foreground(scatter2.axes, GREEN)
        assert_axes_foreground(image2.axes, GREEN)
        assert_axes_foreground(histogram2.axes, GREEN)
        assert_axes_foreground(dendrogram2.axes, GREEN)
        assert_axes_foreground(custom2.axes, GREEN)
