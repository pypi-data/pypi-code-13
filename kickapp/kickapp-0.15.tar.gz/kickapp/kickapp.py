#!/usr/bin/env python

import sys
import os
import shutil

from .info import VERSION
from .kickinit import kickinit
from .kicktools import parcefiles, getname

TEMPLATE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "template")
RECIPES_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "recipes")
DJANGOAPPS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "djangoapps")
#CWD_PATH = os.getcwd()

HELP = """Kickapp {VERSION}

Easy Django to Android deployment.
python-for-android scripts collection.

[init]
Generate new template with a Django project.
\t[--material, material]: Add Material Design Lite (mdl) to project https://getmdl.io


[create]
Generate source tree for python-for-android (p4a), must 'init' first.


[installactivity, installpythonactivity]
Replace p4a activity with custom Kickapp, must 'create' first.


[debug]
Generate .apk for debugging, must 'create' first.
\t[--install, install]: If 'adb' is available and device is connected install apk.
\t[--run, run]: If install then run app.
\t[--logcat, logcat]: Print logs fron device on terminal.


[genkeystore]
Generate .keystore for sign packages, must 'debug' first.


[signapk]
After generate .keystore sign package, must 'genkeystore' first.

""".format(VERSION=VERSION)

if '--help' in sys.argv or '-h' in sys.argv or len(sys.argv) <= 1:
    print(HELP)
    sys.exit()

assert os.path.exists(TEMPLATE_PATH), "{} not exist.".format(TEMPLATE_PATH)

if os.path.exists(sys.argv[1]):
    #debug
    CURDIR = sys.argv[1]
    MAINCOMMAND = sys.argv[2]
    try:
        NAMEPRETTY = sys.argv[3]
    except:
        NAMEPRETTY = None

else:
    MAINCOMMAND = sys.argv[1]
    try:
        NAMEPRETTY = sys.argv[2]
    except:
        NAMEPRETTY = None

    CURDIR = os.path.abspath(os.curdir)

#----------------------------------------------------------------------
def getconfigfile():
    """"""
    return os.path.join(CURDIR, ".p4a")

#----------------------------------------------------------------------
def getconfig(key):
    """"""
    file = open(getconfigfile(), "r")
    lines = file.readlines()
    file.close()
    lines = "".join(lines)
    value = lines[lines.find(key)+len(key)+1:lines.find("\n", lines.find(key))]

    return value.replace(" ", "").replace("\"", "").replace("'", "")


if MAINCOMMAND == "init":
    kickinit(NAMEPRETTY, CURDIR, TEMPLATE_PATH, RECIPES_PATH, DJANGOAPPS_PATH)
    sys.exit()


if MAINCOMMAND == "create":
    os.system("p4a create")
    sys.exit()


if MAINCOMMAND in ["installactivity", "installpythonactivity"]:
    dist_name = getconfig("--dist_name")

    ACTIVITY = os.path.join(os.path.abspath(os.path.dirname(__file__)), "org", "PythonActivity.java")
    KICKACTIVITY = os.path.join(CURDIR, ".build", "dists", dist_name, "src", "org", "kivy", "android", "PythonActivity.java")

    assert os.path.exists(KICKACTIVITY), "Must run 'p4a create' first"

    os.remove(KICKACTIVITY)
    shutil.copyfile(ACTIVITY, KICKACTIVITY)

    print("Instaled Python-KickApp activity in {}".format(KICKACTIVITY))
    statusbarcolor = getconfig("--statusbarcolor")
    print("Added statusbar color: {}".format(statusbarcolor))
    parcefiles([KICKACTIVITY], {"STATUS_BAR_COLOR": statusbarcolor,})
    sys.exit()


if MAINCOMMAND == "debug":
    name = getname(getconfig("--name"))
    APPDIR = os.path.join(CURDIR, "app", name)
    os.chdir(APPDIR)
    COLLECTSTATIC = "{} manage.py collectstatic --noinput".format(sys.executable)
    os.system(COLLECTSTATIC)

    os.chdir(CURDIR)
    os.system("p4a apk")

    if "install" in sys.argv or "--install" in sys.argv:
        os.system("adb start-server")
        os.system("adb install -r *.apk")

    if "run" in sys.argv or "--run" in sys.argv:
        package = getconfig("--package")
        os.system("adb shell monkey -p {PACKAGE} -c android.intent.category.LAUNCHER 1".format(PACKAGE=package))

    if "logcat" in sys.argv or "--logcat" in sys.argv:
        os.system("adb logcat")

    sys.exit()


if MAINCOMMAND == "genkeystore":
    name = getname(getconfig("--name"))
    keystore = os.path.join(CURDIR, '{}.keystore'.format(name))
    os.chdir(CURDIR)
    os.system("keytool -genkey -v -keystore {} -alias {} -keyalg RSA -keysize 2048 -validity 10000".format(keystore, name))
    sys.exit()


if MAINCOMMAND == "signapk":
    storage_dir = getconfig("--storage-dir")
    dist_name = getconfig("--dist_name")
    name = getconfig("--name")
    verbose_name = getname(getconfig("--name"))
    version = getconfig("--version")
    keystore = os.path.join(CURDIR, '{}.keystore'.format(verbose_name))
    sdk_dir = getconfig("--sdk_dir")

    os.chdir(CURDIR)

    release_unsigned_on_bin = os.path.join(storage_dir, 'dists', dist_name, 'bin', '{}-{}-release-unsigned.apk'.format(name, version))
    release_unsigned = os.path.join(CURDIR, '{}-{}-release-unsigned.apk'.format(name, version))
    release_signed = os.path.join(CURDIR, '{}-{}.apk'.format(name, version))

    shutil.copyfile(release_unsigned_on_bin, release_unsigned)
    os.system("jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore {} {} {}".format(keystore, release_unsigned, verbose_name))
    os.system("jarsigner -verify -verbose -certs {}".format(release_unsigned))
    os.system("{}/build-tools/21.1.2/zipalign -v 4 {} {}".format(sdk_dir, release_unsigned, release_signed))
    os.remove(release_unsigned)
    sys.exit()

print("It Seems you need help.")
print(HELP)