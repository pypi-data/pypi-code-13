import sys
import os
import logging
import pytest
import py


class Pdb(py.std.pdb.Pdb, object):
    def __init__(self, stdin=sys.__stdin__, stdout=sys.__stdout__, *argv, **kwargv):
        return super(Pdb, self).__init__(stdin=stdin, stdout=stdout, *argv, **kwargv)

py.std.pdb.Pdb = Pdb


def pytest_addoption(parser):
    group = parser.getgroup("gae", "google app engine plugin")
    group.addoption('--with-gae', action='store_true', dest='use_gae',
                    default=False, help='Use pytest_gae plugin')
    group.addoption('--gae-path', action='store', dest='gae_path',
                    metavar='PATH', default='./google_appengine/',
                    help="Google App Engine's root PATH")
    group.addoption('--gae-project-path', action='store', dest='gae_prj_path',
                    metavar='PATH', default='./',
                    help="Your project's source code's PATH")


def pytest_configure(config):
    if not config.option.use_gae:
        return

    _update_syspath(config)

    _validate_gae_path(config.option.gae_path)
    _validate_project_path(config.option.gae_prj_path)


def pytest_runtest_teardown(item):
    # There is some problems with GAE and py.test miscomunication that causes
    # closed stream handler to be flushed.
    #
    # Which causes Exception and some nasty errors at the end of testing.
    #
    # This nasty hack prevents that error to be displayed.
    for h in logging.getLogger().handlers:
        if isinstance(h, logging.StreamHandler):
            _attach_save_flush(h)


def _update_syspath(config):
    """Add Project modules and GAE module and libs to sys.path"""
    # Google App Engine module
    sys.path.insert(0, config.option.gae_path)

    # Dynamically add libs that comes with GAE
    import dev_appserver
    dev_appserver.fix_sys_path()

    # Project module
    sys.path.insert(0, config.option.gae_prj_path)


def _validate_gae_path(path):
    try:
        import google.appengine
    except ImportError:
        raise pytest.UsageError(
            "google.appengine lib can not be imported. Try to use "
            "--gae-path option. Current path: <{0}> ".format(path))


def _validate_project_path(path):
    # Google App Engine projects must contain app.yaml at their roots.
    # So, this code just checks if app.yaml exists
    if not os.path.exists(os.path.join(path, 'app.yaml')):
        raise pytest.UsageError(
            "Your AppEngine's project can not be found. Try to use "
            "--gae-project-path option. Current path: <{0}> ".format(path))


def _attach_save_flush(handler):
    def save_flush():
        if not handler.stream.closed:
            handler.stream.flush()

    handler.flush = save_flush
