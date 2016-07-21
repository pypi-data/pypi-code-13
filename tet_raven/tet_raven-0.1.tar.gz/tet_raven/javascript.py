from pyramid.events import subscriber, BeforeRender
from tet.util.json import js_safe_dumps
from tet.viewlet import BeforeViewletRender

script_template = '''\
<script src="{url}"></script>
<script>Raven.config({dsn}).install();</script>
'''


class RavenJSTemplate(object):
    def __init__(self, raven_js, request):
        self.request = request
        self.raven_js = raven_js

    def __call__(self, *plugins):
        if not self.raven_js.dsn or self.raven_js.dsn == 'null':
            return ''

        template = str(self)
        for i in plugins:
            url = self.request.static_url('tet_raven:static/plugins/{}.js'.format(i))
            template += '<script src="{}"></script>\n'.format(url)

        return template

    def __str__(self):
        if self.raven_js.dsn is None:
            return ''

        raven_js_url = self.request.static_url('tet_raven:static/raven.js')
        return script_template.format(url=raven_js_url, dsn=self.raven_js.dsn)


class RavenJS(object):
    def __init__(self, dsn):
        self.dsn = js_safe_dumps(dsn)

    def add_js_injection(self, system):
        request = system['request']
        system['raven_js'] = self.get_injection_script(request)

    def get_injection_script(self, request):
        return RavenJSTemplate(self, request)


def includeme(config, dsn=None, static_view_url=None):
    static_view_url = static_view_url or config.registry.settings.get('raven_js.static_view') or 'tet_raven'
    config.add_static_view(name=static_view_url, path='tet_raven:static')

    dsn = dsn or config.registry.settings.get('raven_js.dsn')
    raven_js = RavenJS(dsn=dsn)
    config.registry.raven_js = raven_js
    config.add_subscriber(raven_js.add_js_injection, BeforeRender)
    config.add_subscriber(raven_js.add_js_injection, BeforeViewletRender)
