
from flask_magic import Magic, get_config, register_app, abort

register_app(__package__)


def setup(**kwargs):
    """
    Create the Maintenance view
    Must be instantiated

    import maintenance_view
    m = maintenance_view()

    :param template_: The directory containing the view pages
    :return:
    """

    template = "MaintenancePage/index.html"

    class MaintenancePage(Magic):

        @classmethod
        def _register(cls, app, **kw):

            super(cls, cls)._register(app, **kw)

            if kwargs.get("is_on", False) is True:
                @app.before_request
                def on_maintenance():
                    return cls.render(_layout=template), 503

    return MaintenancePage
