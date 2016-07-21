from __future__ import absolute_import

from pyramid.request import Request
from raven import Client as RavenClient
from raven.utils.wsgi import get_current_url, get_headers, get_environ


def raven_tween_factory(handler, registry):
    client = registry.raven

    def raven_tween(request):
        client.http_context(get_http_context(request.environ))
        try:
            response = handler(request)

        except Exception:
            handle_exception(request.environ)
            raise

        finally:
            client.context.clear()

        return response

    def get_http_context(request: Request):
        environ = request.environ
        return dict(method=environ.get('REQUEST_METHOD'),
                    url=get_current_url(environ, strip_querystring=True),
                    query_string=environ.get('QUERY_STRING'),
                    headers=dict(get_headers(environ)),
                    env=dict(get_environ(request.environ)))

    def handle_exception(environ=None):
        return client.captureException()

    return raven_tween


def includeme(config, over=None, under=None):
    settings = config.registry.settings
    if 'raven.dsn' in settings:
        config.registry.raven = RavenClient(settings['raven.dsn'])
        if over is not None:
            config.add_tween('tet_raven.raven_tween_factory', over=over)
        elif under is not None:
            config.add_tween('tet_raven.raven_tween_factory', under=under)
        else:
            config.add_tween('tet_raven.raven_tween_factory', under=(
                'pyramid.tweens.excview_tween_factory',
                'INGRESS'
            ))
