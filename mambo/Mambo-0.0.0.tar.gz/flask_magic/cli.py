"""
________________________________________________________________________________

flask.

 /$$      /$$  /$$$$$$   /$$$$$$  /$$$$$$  /$$$$$$
| $$$    /$$$ /$$__  $$ /$$__  $$|_  $$_/ /$$__  $$
| $$$$  /$$$$| $$  \ $$| $$  \__/  | $$  | $$  \__/
| $$ $$/$$ $$| $$$$$$$$| $$ /$$$$  | $$  | $$
| $$  $$$| $$| $$__  $$| $$|_  $$  | $$  | $$
| $$\  $ | $$| $$  | $$| $$  \ $$  | $$  | $$    $$
| $$ \/  | $$| $$  | $$|  $$$$$$/ /$$$$$$|  $$$$$$/
|__/     |__/|__/  |__/ \______/ |______/ \______/

https://github.com/mardix/flask-magic

________________________________________________________________________________
"""

import os
import re
import sys
import traceback
import logging
import importlib
import pkg_resources
import click
import yaml
import functools
import multiprocessing
import sh
from werkzeug import import_string
from . import utils
from .__about__ import *

CWD = os.getcwd()
SKELETON_DIR = "skel"
APPLICATION_DIR = "%s/application" % CWD
APPLICATION_DATA_DIR = "%s/_data" % APPLICATION_DIR


def get_project_dir_path(project_name):
    return "%s/%s" % (APPLICATION_DIR, project_name)


def copy_resource(src, dest):
    """
    To copy package data to destination
    """
    dest = (dest + "/" + os.path.basename(src)).rstrip("/")
    if pkg_resources.resource_isdir("flask_magic", src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for res in pkg_resources.resource_listdir(__name__, src):
            copy_resource(src + "/" + res, dest)
    else:
        if not os.path.isfile(dest) \
                and os.path.splitext(src)[1] not in [".pyc"]:
            with open(dest, "wb") as f:
                f.write(pkg_resources.resource_string(__name__, src))
        else:
            print("File exists: %s " % dest)


def create_project(project_name, no_assets=True):
    """
    Create the project
    """
    project_dir = get_project_dir_path(project_name)
    app_tpl = pkg_resources.resource_string(__name__, '%s/serve.py' % (SKELETON_DIR))
    propel_tpl = pkg_resources.resource_string(__name__, '%s/propel.yml' % (SKELETON_DIR))
    magic_tpl = pkg_resources.resource_string(__name__, '%s/magic.yml' % (SKELETON_DIR))
    config_tpl = pkg_resources.resource_string(__name__, '%s/config.py' % (SKELETON_DIR))
    model_tpl = pkg_resources.resource_string(__name__, '%s/model.py' % (SKELETON_DIR))
    manage_tpl = pkg_resources.resource_string(__name__, '%s/magic.py' % (SKELETON_DIR))
    gitignore_tpl = pkg_resources.resource_string(__name__, '%s/gitignore' % (SKELETON_DIR))
    views_tpl = pkg_resources.resource_string(__name__, '%s/views.py' % (SKELETON_DIR))

    serve_file = "%s/serve.py" % CWD
    requirements_txt = "%s/requirements.txt" % CWD
    propel_yml = "%s/propel.yml" % CWD
    magic_yml = "%s/magic.yml" % CWD
    config_py = "%s/config.py" % APPLICATION_DIR
    model_py = "%s/model.py" % APPLICATION_DIR
    manage_py = "%s/magic.py" % CWD
    gitignore = "%s/.gitignore" % CWD
    views = "%s/views.py" % project_dir

    dirs = [
        APPLICATION_DIR,
        APPLICATION_DATA_DIR,
        project_dir
    ]
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)

    files = [
        ("%s/__init__.py" % APPLICATION_DIR, "# flask-Magic"),
        ("%s/__init__.py" % project_dir, "# flask-Magic"),
        (config_py, config_tpl),
        (model_py, model_tpl),
        (serve_file, app_tpl.format(project_name=project_name)),
        (requirements_txt, "%s==%s" % (__title__, __version__)),
        (propel_yml, propel_tpl.format(project_name=project_name)),
        (magic_yml, magic_tpl.format(project_name=project_name)),
        (manage_py, manage_tpl),
        (gitignore, gitignore_tpl),
        (views, views_tpl)
    ]
    for f in files:
        if not os.path.isfile(f[0]):
            with open(f[0], "wb") as f0:
                f0.write(f[1])

    if not no_assets:
        copy_resource("%s/assets/" % SKELETON_DIR, project_dir)
    copy_resource("%s/_data/" % SKELETON_DIR, APPLICATION_DATA_DIR)

# ------------------------------------------------------------------------------


def get_magic_config(cwd, key):
    with open("%s/%s" % (cwd, "magic.yml")) as f:
        config = yaml.load(f)

    if key not in config:
        raise Exception("Missing '%s' in magic.yml" % key)
    return config[key]


def get_push_remotes_list(cwd, key=None):
    """
    Returns the remote hosts in propel
    :param cwd:
    :param key:
    :param file:
    :return: list
    """
    config = get_magic_config(cwd, "push")
    return config[key] if key else [v for k, l in config.items() for v in l]


def git_push_to_master(cwd, hosts, name="all", force=False):
    """
    To push to master
    :param cwd:
    :param hosts:
    :param force:
    :return:
    """

    def process_output(line):
        print(line)

    with sh.pushd(cwd):
        name = "magic_deploy_%s" % name

        if sh.git("status", "--porcelain").strip():
            raise Exception("Repository is UNCLEAN. Commit your changes")

        remote_list = sh.git("remote").strip().split()
        if name in remote_list:
            sh.git("remote", "remove", name)
        sh.git("remote", "add", name, hosts[0])

        if len(hosts) > 1:
            for h in hosts:
                sh.git("remote", "set-url", name, "--push", "--add", h)

        _o = ["push", name, "master"]
        if force:
            _o.append("--force")
        sh.git(*_o, _out=process_output)
        sh.git("remote", "remove", name)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def catch_exception(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            print("-" * 80)
            print("Exception Uncaught")
            print("-" * 80)
            print(ex)
            print("-" * 80)

    return decorated_view


def bg_process(func):
    """
    A multiprocess decorator
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        p.start()
    return wrapper


def cwd_to_sys_path():
    sys.path.append(CWD)


def import_module(project, is_app=False):
    cwd_to_sys_path()
    project = project_name("app_" + project if is_app else project)
    return importlib.import_module(project)


def project_name(name):
    return re.compile('[^a-zA-Z0-9_]').sub("", name)


def header(title=None):
    print(__doc__)
    print("v. %s" % __version__)
    print("_" * 80)
    if title:
        print("** %s **" % title)


def build_assets(mod):
    from webassets.script import CommandLineEnvironment

    module = import_module(mod, True)
    assets_env = module.app.jinja_env.assets_environment

    log = logging.getLogger('webassets')
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)

    cmdenv = CommandLineEnvironment(assets_env, log)
    cmdenv.build()


def _assets2s3(project):
    import flask_s3
    module = import_module(project, True)

    header("Building assets files for project: %s ..." % project)
    print("")
    build_assets(project)

    print("Uploading assets files to S3 ...")
    flask_s3.create_all(module.app)
    print("")


@bg_process
def _assets2s3_m(project):
    """
    For multi processing
    :param project:
    :return:
    """
    _assets2s3(project)


@click.group()
def cli(): pass


@cli.command("create")
@click.argument("app_name")
@click.option("--no-assets", "-x", is_flag=True)
@catch_exception
def create(app_name, no_assets):
    """  Create a new App in the current directory """

    app = project_name(app_name)

    header("Creating new app ...")
    print("")
    print("- Name: %s " % app)

    create_project(app, no_assets)
    print("")
    print("----- That was Magic! ----")
    print("")
    print("- Your new app [ %s ] has been created" % app)
    print("- Location: [ application/%s ]" % app)
    print("")
    print("> What's next?")
    print("- Edit the config [ application/config.py ] ")
    print("- If necessary edit and run the command [ magic setup ]")
    print("- Launch app on development mode, run [ app='%s' magic serve ]" % app)
    print("")
    print("*" * 80)


@cli.command("serve")
@click.option("--port", "-p", default=5000)
@click.option("--no-watch", is_flag=True)
#@catch_exception
def serve(port, no_watch):
    """ Serve application in development mode """

    header("Serving application in development mode ... ")

    print("")
    print("- Port: %s" % port)
    print("")

    cwd_to_sys_path()
    module = importlib.import_module("serve")

    extra_files = []
    if not no_watch:
        extra_dirs = [CWD,]
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in os.walk(extra_dir):
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    if os.path.isfile(filename):
                        extra_files.append(filename)

    module.app.run(debug=True,
                   host='0.0.0.0',
                   port=port,
                   extra_files=extra_files)

@cli.command("setup-models")
def setup_models():
    """ To setup models """
    print("Setting up models...")
    cwd_to_sys_path()
    magic = import_string("magic")
    db = magic.model.db
    db.create_all()
    for m in db.Model.__subclasses__():
        if hasattr(m, "_setup_model"):
            print("Setting up: %s ..." % m.__name__)
            getattr(m, "_setup_model")()

    print("Done")


@cli.command("assets2s3")
@click.option("--project", "-p", default=None)
@catch_exception
def assets2s3(project):
    """ Upload assets files to S3 """

    projects = get_magic_config(CWD, "assets2s3")
    if not project and projects and len(projects) > 1:
        [_assets2s3_m(p) for p in projects]
    elif project or len(projects) == 1:
        _assets2s3(project or projects[0])


@cli.command("push")
@click.option("--remote", "-r", default=None)
@click.option("--force", "-f", is_flag=True, default=False)
@catch_exception
def push(remote, force):
    """ To push application to a git repository """

    remote_name = remote or "ALL"
    print("Pushing application to remote: %s " % remote_name)
    print("...")
    hosts = get_push_remotes_list(CWD, remote or None)
    git_push_to_master(cwd=CWD, hosts=hosts, name=remote_name, force=force)
    print("Done!")



# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def cmd():
    """
    Help to run the command line
    :return:
    """
    if os.path.isfile(os.path.join(os.path.join(CWD, "magic.py"))):
        cwd_to_sys_path()
        print("BKHHAHAHAHHAHAHAHAHAHHAHHAHHAHAHHAHAHAHAH")
        #magic = import_string("magic")
    else:
        print("-" * 80)
        print("** Missing << 'magic.py' >> @ %s" % CWD)
        print("-" * 80)
    cli()

