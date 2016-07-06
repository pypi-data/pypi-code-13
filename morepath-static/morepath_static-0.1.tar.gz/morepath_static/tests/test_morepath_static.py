from webtest import TestApp as Client
from .. import App
from ..__main__ import run


def test_static_assets():
    c = Client(App())

    r = c.get('/')

    scripts = r.html.select('script')
    assert len(scripts) == 2

    for s in scripts:
        c.get(s['src'])


def test_run(monkeypatch):
    import morepath
    instances = []
    monkeypatch.setattr(morepath, 'run', lambda app: instances.append(app))

    run()

    app, = instances
    assert isinstance(app, App)
