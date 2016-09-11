"""
MamboAdmin
"""
from mambo import Mambo, register_package

register_package(__package__)

__version__ = "1.0.0"

def main(**kwargs):

    decorators = kwargs.get("decorators", [])
    options = kwargs.get("options", {})

    Mambo.g(TITLE=options.get("title", "Admin"),
            THEME=options.get("theme", "yeti"))
    Mambo.base_layout = "MamboAdmin/layout.html"
    if decorators:
        Mambo.decorators += decorators





