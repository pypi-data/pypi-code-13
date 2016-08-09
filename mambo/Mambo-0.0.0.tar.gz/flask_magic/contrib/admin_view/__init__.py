"""
MagicAdmin
"""
from flask_magic import Magic, register_app

register_app(__package__)


def setup(**kwargs):

    Magic.g(ADMIN_BRAND=kwargs.get("brand", "Admin"))
    Magic.base_layout = "MagicAdmin/layout.html"




