from .model import Root
from .app import App


@App.html(model=Root)
def root_default(self, request):
    request.include('my_component')
    return ("<!DOCTYPE html><html><head></head><body>"
            "components are inserted in the HTML source</body></html>")
