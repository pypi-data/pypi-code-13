"""
flask-Magic
"""

from flask_magic import (Magic, page_meta, get_config, flash_success, flash_error,
                         abort, request, url_for, redirect,
                         # decorators
                         get, post, set_nav, render_json,
                         # ext
                         storage, mail, csrf, cache, recaptcha)

# ------------------------------------------------------------------------------


class Index(Magic):

    @set_nav("Home", order=1)
    def index(self):
        page_meta(title="Hello View!")

        return {}

    @get("/hello-json/")
    @render_json
    def hello(self):
        return {"Hello": "World"}


