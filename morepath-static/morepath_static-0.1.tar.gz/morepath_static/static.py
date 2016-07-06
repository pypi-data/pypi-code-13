import bowerstatic
import os

from .app import App


bower = bowerstatic.Bower()


components = bower.components(
    'app', os.path.join(os.path.dirname(__file__), 'bower_components'))


local = bower.local_components('local', components)


local.component(os.path.join(os.path.dirname(__file__), 'my_component'),
                version=None)


@App.static_components()
def get_static_components():
    return local
