"""A fullscreen program that displays an animated, twisting tessellation of whirls."""

# Copyright 2016 David Nickerson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import pygame
import numpy as np
from scipy.spatial import Delaunay
from matplotlib.tri import Triangulation
from pgu import gui
from typing import Tuple

PYGAME_WHITE = pygame.Color('white')
PYGAME_BLACK = pygame.Color('black')
PGU_WHITE = (255, 255, 255)
PGU_BLACK = (0, 0, 0)
PGU_LEFT = -1
PGU_RIGHT = 1
PGU_TOP = -1


class App:
    """Encapsulate the window, main loop, and events."""

    def __init__(self, title: str, inner_point_count: int, inner_border: int,
                 window_size: Tuple[int, int] = None) -> None:
        """Create a new App.

        Args:
            title: The title of the window.
            inner_point_count: The number of points to generate, not including the four corners.
            inner_border: The minimum gap (in pixels) between the inner points and the edge of the screen.
            window_size: If defined, this is the pixel width and height of the contents of the window. If None, the app
                is run in fullscreen mode.
        """
        pygame.init()
        if window_size is None:
            self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            window_size = self._screen.get_size()
        else:
            self._screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(title)
        self._slider_gui = SliderGui()
        outer_border = 2
        self._painter = Painter(window_size, self._slider_gui, inner_point_count, inner_border, outer_border)
        self._clock = pygame.time.Clock()
        self._fps = 30
        self._app = gui.App()
        self._container = gui.Container(align=PGU_LEFT, valign=PGU_TOP)
        self._app.init(self._container)
        self._gui_enabled = False

    def main_loop(self) -> None:
        """Display the window and run for the lifetime of the application.

        This method does not return.
        """
        while True:
            for event in pygame.event.get():
                if not self._handle_event(event):
                    self._app.event(event)
            self._painter.paint(self._screen)
            self._slider_gui.update_status(round(self._clock.get_fps()), self._painter.lines)
            self._app.paint()
            pygame.display.flip()
            self._clock.tick(self._fps)

    def _handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events that are not part of PGU.

        Args:
            event: An event to attempt to handle.

        Returns:
            True if the event has been handled, False otherwise
        """
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._gui_enabled:
                if event.pos[0] > self._slider_gui.rect.w or event.pos[1] > self._slider_gui.rect.h:
                    self._container.remove(self._slider_gui)
                    self._gui_enabled = False
                    return True
            else:
                self._container.add(self._slider_gui, 0, 0)
                self._gui_enabled = True
                self._painter.partial_draw = False
                return True
        return False


class Painter:
    """Encapsulate calculating and drawing the tessellation."""

    def __init__(self, screen_size: Tuple[int, int], slider_gui: 'SliderGui', inner_point_count: int, inner_border: int,
                 outer_border: int) -> None:
        """Create a new Painter.

        Args:
            screen_size: The pixel width and height of the tessellation.
            slider_gui: The GUI containing the sliders
            inner_point_count: The number of points to generate, not including the four corners.
            inner_border: The minimum gap (in pixels) between the inner points and the edge of the screen.
            outer_border: The gap (in pixels) between the points in the four corners and the edge of the screen.
        """
        # Settings that cannot be tweaked during animation.
        self._slider_gui = slider_gui
        self._inner_point_count = inner_point_count
        self._poll_gui()

        # Settings that are modified as a part of the animation.
        self._convolution_offset = 0
        self._angles = (2 * np.pi) * np.random.rand(inner_point_count)

        # Initialization
        screen_size = np.array(screen_size)
        inner_points = translate(np.random.rand(inner_point_count, 2), screen_size, inner_border)
        outer_points = translate(np.array(((0, 0), (0, 1), (1, 0), (1, 1))), screen_size, outer_border)
        self._points = np.concatenate((inner_points, outer_points))
        self._triangles = Delaunay(self._points).simplices
        self._edges = Triangulation(self._points[:, 0], self._points[:, 1], self._triangles).edges
        self._max_lines = 0
        self.partial_draw = True  # type: bool
        """If True, only a limited number of lines will be drawn each frame."""
        self.lines = 0  # type: int
        """The number of lines that were drawn in the last frame."""

    def _poll_gui(self) -> None:
        """Cache the relevant settings from the GUI.

        We do this before calculation to prevent multithreading inconsistency bugs.
        """
        self._twist_factor = self._slider_gui.twist_factor.value
        self._twist_speed = self._slider_gui.twist_speed.value
        self._depth = self._slider_gui.depth.value
        self._warp_speed = self._slider_gui.warp_speed.value
        self._warp_size = self._slider_gui.warp_size.value

    def _move(self) -> None:
        """Make the changes needed to step the animation by one frame."""
        self._convolution_offset = (self._convolution_offset + self._twist_speed) % self._twist_factor
        self._angles = (self._angles + self._warp_speed) % (2 * np.pi)  # Modulus not necessary, but prevents drifting.
        if self.partial_draw:
            self._max_lines = self._max_lines * 1.01 + 0.03

    def paint(self, screen: pygame.Surface) -> None:
        """Draw the picture on the given screen.

        Args:
            screen: The surface on which to draw.
        """
        self._poll_gui()
        self._move()
        self.lines = 0
        points = self._points.copy()
        offset = np.array((np.sin(self._angles), np.cos(self._angles))).T * self._warp_size
        points[:self._inner_point_count] += offset
        screen.fill(PYGAME_WHITE)
        for start, end in points[self._edges]:
            pygame.draw.aaline(screen, PYGAME_BLACK, start, end)
            self.lines += 1
            if self.partial_draw and self.lines > self._max_lines:
                return
        # max(np.ptp(triangle, axis=0))
        for triangle in points[self._triangles]:
            triangle = convolve(triangle, self._convolution_offset)
            for _ in range(self._depth):
                pygame.draw.aalines(screen, PYGAME_BLACK, True, triangle)
                self.lines += 3
                if self.partial_draw and self.lines > self._max_lines:
                    return
                triangle = convolve(triangle, self._twist_factor)
            pygame.draw.lines(screen, PYGAME_BLACK, True, triangle, 2)
            pygame.draw.polygon(screen, PYGAME_BLACK, triangle)
        self.partial_draw = False


class SliderGui(gui.Table):
    """Encapsulate the user interface."""

    def __init__(self, **kwargs) -> None:
        """Create a new SliderGui.

        Args:
            **kwargs: Keyword arguments passed to gui.Table.
        """
        super().__init__(background=PGU_WHITE, **kwargs)
        self._slider_size = 20
        self._slider_width = 300
        self._slider_height = 16
        self.twist_factor = self._float_slider('Density ', value=0.075, min_=0.15, max_=0.001)  # type: FloatHSlider
        """The density slider."""
        self.twist_speed = self._float_slider('Twist Speed ', value=0.001, min_=-0.002,
                                              max_=0.002)  # type: FloatHSlider
        """The twist speed slider."""
        self.depth = self._slider('Depth ', value=25, min_=0, max_=50)  # type: gui.HSlider
        """The depth slider."""
        self.warp_speed = self._float_slider('Warp Speed ', value=0.01, min_=0, max_=0.02)  # type: FloatHSlider
        """The warp speed slider."""
        self.warp_size = self._float_slider('Warp Size ', value=10, min_=0, max_=20)  # type: FloatHSlider
        """The warp size slider."""
        self._fps = self._status('FPS ')
        self._lines = self._status('Lines ')
        self._lines_per_sec = self._status('Lines/Sec ')

    def _slider(self, name: str, value: int, min_: int, max_: int) -> gui.HSlider:
        """Create a horizontal slider and add it to the table.

        Args:
            name: The name of the slider.
            value: The initial position of the slider.
            min_: The minimum value of the slider.
            max_: The minimum value of the slider.

        Returns:
            The created slider.
        """
        self.tr()
        self.td(gui.Label(name, color=PGU_BLACK), align=PGU_RIGHT)
        slider = gui.HSlider(value, min_, max_, size=self._slider_size, width=self._slider_width,
                             height=self._slider_height)
        self.td(slider)
        return slider

    def _float_slider(self, name: str, value: float, min_: float, max_: float) -> 'FloatHSlider':
        """Create a floating-point horizontal slider and add it to the table.

        Args:
            name: The name of the slider.
            value: The initial position of the slider.
            min_: The minimum value of the slider.
            max_: The minimum value of the slider.

        Returns:
            The created slider.
        """
        self.tr()
        self.td(gui.Label(name, color=PGU_BLACK), align=PGU_RIGHT)
        float_slider = FloatHSlider(value, min_, max_, size=self._slider_size, width=self._slider_width,
                                    height=self._slider_height)
        self.td(float_slider.slider)
        return float_slider

    def _status(self, name: str) -> gui.Label:
        """Create a status field and add it to the table.

        Args:
            name: The name of the status field.

        Returns:
            The created status field.
        """
        self.tr()
        self.td(gui.Label(name, color=PGU_BLACK), align=PGU_RIGHT)
        value = gui.Label('', color=PGU_BLACK)
        self.td(value, align=PGU_LEFT)
        return value

    def update_status(self, fps: int, lines: int) -> None:
        """Update the status fields.

        Args:
            fps: The frames per second.
            lines: The number of lines drawn.
        """
        self._fps.set_text(str(fps))
        self._lines.set_text(str(lines))
        self._lines_per_sec.set_text(str(fps * lines))


class FloatHSlider:
    """A horizontal slider that supports floating-point values."""

    # Normally one would want to inherit from gui.HSlider or gui.widget.Widget so that this class would be a widget that
    # could be added directly to the view. Unfortunately, we can't inherit from HSlider because gui._slider defines a
    # strict '__setattr__', and inheriting from gui.widget.Widget would require massive duplication of the _slider code
    # base. Therefore we instead wrap an HSlider and bind it to the 'slider' field.

    def __init__(self, value: float, min_: float, max_: float, size: float, **kwargs) -> None:
        """Create a new FloatHSlider.

        The minimum and maximum values will be exactly as specified, but, due to the internal representation, the
        initial value will be approximate.

        Args:
            value: The approximate initial position of the slider.
            min_: The minimum value of the slider.
            max_: The minimum value of the slider.
            size: The length of the slider bar in pixels.
        """
        self._min = min_
        self._max = max_
        int_value = interp(value, min_, max_, 0, 1000)
        self.slider = gui.HSlider(int_value, 0, 1000, size, **kwargs)  # type: gui.HSlider
        """The GUI widget that should be added to the view. Do not use the 'value' property of this object."""

    @property
    def value(self) -> float:
        """The value that the slider is set to."""
        return interp(self.slider.value, 0, 1000, self._min, self._max)


def interp(value: float, from_min: float, from_max: float, to_min: float, to_max: float) -> float:
    """Linear interpolation from a source range to a destination range.

    Maps the source range to the destination range, and returns the corresponding value.  If the value is between
    from_min and from_max, then the returned value is between to_min and to_max.  If the value is equal to from_min,
    then the returned value is equal to to_min.  Likewise, if the value is equal to from_max, then the returned value is
    equal to to_max.  If the value is not between from_min and from_max, then the returned value is not between to_min
    and to_max. From_max may be less than from_min and to_max may be less than to_min.  from_min may not equal from_max.

    Args:
        value: The value to interpolate.
        from_min: A value that maps to to_min.
        from_max: A value that maps to to_max.
        to_min: A value that maps from from_min.
        to_max: A value that maps from from_max.

    Returns:
        The corresponding value.
    """
    from_range = from_max - from_min
    to_range = to_max - to_min
    value_scaled = (value - from_min) / from_range
    return value_scaled * to_range + to_min


def translate(points: np.ndarray, size: np.ndarray, border: int) -> np.ndarray:
    """Return the points translated to the area within the border within the target rectangle.

    Args:
        points: An array of points whose coordinates are in the range [0, 1).
        size: The width and height of the target rectangle.
        border: The border within the target rectangle.

    Returns:
        The translated points.
    """
    return points * (size - 2 * border) + border


def convolve(polygon: np.ndarray, factor: float) -> np.ndarray:
    """Return a new polygon whose vertices are between the adjacent vertices of the given polygon.

    Args:
        polygon: An array of points.
        factor: Where the new vertices should be placed.  If 0, the convolved polygon will be identical to the given
            polygon.  If 0.5, the vertices of the convolved polygon will be halfway between the adjacent vertices of the
            given polygon.

    Returns:
        The convolved polygon.
    """
    return (1 - factor) * polygon + factor * np.roll(polygon, -1, axis=0)


def main() -> None:
    """Run the program in fullscreen.

    This function does not return.
    """
    window_size = None  # For windowed mode, change to: (1280, 720)
    window = App(title='Whirls', inner_point_count=20, inner_border=50, window_size=window_size)
    window.main_loop()


if __name__ == '__main__':
    main()


# C:\py\env1\Scripts\python -m cProfile -s cumtime whirls.py > profile.txt 2>&1