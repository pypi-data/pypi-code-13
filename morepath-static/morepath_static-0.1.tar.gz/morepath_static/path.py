from .app import App
from .model import Root


@App.path(model=Root, path='/')
def get_root():
    return Root()
