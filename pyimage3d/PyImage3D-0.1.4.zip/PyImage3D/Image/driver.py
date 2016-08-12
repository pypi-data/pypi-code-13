import abc

from PyImage3D.Image import renderer


class ImageDriver(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._image = None

    @abc.abstractmethod
    def create_image(self, x, y):
        return

    @abc.abstractmethod
    def set_color(self, color):
        return

    @abc.abstractmethod
    def draw_polygon(self, polygon):
        return

    @abc.abstractmethod
    def draw_gradient_polygon(self, polygon):
        return

    @abc.abstractmethod
    def save(self, filename):
        return

    def get_supported_shading(self):
        return renderer.ImageRenderer.SHADE_NO,

    def destroy(self):
        return True
