#!/usr/bin/env python

import sys
import os
import shutil

from .kicktools import parcefiles, getname

APPS = ["home"]

#----------------------------------------------------------------------
def kickinit(NAMEPRETTY, CURDIR, TEMPLATE_PATH, RECIPES_PATH, DJANGOAPPS_PATH):
    """"""
    NAME = getname(NAMEPRETTY)
    PACKAGE = "com.kickapp.{}".format(NAME)
    #LOCAL = os.path.join(CURDIR, NAMEPRETTY.replace(" ", "_"))
    LOCAL = os.path.join(CURDIR, NAME)
    APPDIR = os.path.join(LOCAL, "app")
    P4A = os.path.join(LOCAL, ".p4a")
    MAIN = os.path.join(LOCAL, "app", "main.py")

    ICON = os.path.join(APPDIR, "resources", "icon.png")

    ANDROID_SDK = os.path.expanduser("~/dev/android/android-sdk-linux")
    ANDROID_SDK_API = "21"

    CRYSTAX_NDK_VERSION = "10.3.1"
    CRYSTAX_NDK =  os.path.expanduser("~/dev/android/crystax-ndk-{}".format(CRYSTAX_NDK_VERSION))

    PORT = "8000"

    shutil.copytree(TEMPLATE_PATH, LOCAL)
    shutil.copytree(RECIPES_PATH, os.path.join(LOCAL, ".recipes"))
    os.chdir(APPDIR)

    os.rename(os.path.join(LOCAL, "p4a"), P4A)

    STARTPROJECT = "django-admin startproject {}".format(NAME)
    os.system(STARTPROJECT)

    SETTINGS_FILE = os.path.join(APPDIR, NAME, NAME, "settings.py")
    URLS_FILE = os.path.join(APPDIR, NAME, NAME, "urls.py")

    if "--material" in sys.argv or "material" in sys.argv:
        for app in APPS:
            shutil.copytree(os.path.join(DJANGOAPPS_PATH, app), os.path.join(APPDIR, NAME, app))

        settings = open(SETTINGS_FILE, "r")
        lines = settings.readlines()
        settings.close()
        new_lines = "".join(lines)
        new_lines = new_lines.replace("'django.contrib.staticfiles',", "'django.contrib.staticfiles',\n\n    'kickapp.djangoapps.app',\n    'kickapp.djangoapps.mdlenchant',\n    'home',\n")
        new_lines += "\nSTATIC_ROOT = os.path.join(BASE_DIR, 'static')\n"

        settings = open(SETTINGS_FILE, "w")
        settings.write(new_lines)
        settings.close()

        urls = open(URLS_FILE, "r")
        lines = urls.readlines()
        urls.close()
        new_lines = "".join(lines)

        new_lines = new_lines.replace("from django.contrib import admin", "from django.conf.urls.static import static\nfrom . import settings\nfrom home.views import Home")
        new_lines = new_lines.replace("    url(r'^admin/', admin.site.urls),", "    url(r'^$', Home.as_view(), name='home'),")
        new_lines = new_lines.replace("]", "] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)")

        urls = open(URLS_FILE, "w")
        urls.write(new_lines)
        urls.close()

        print("Installed material template as kickapp.djangoapps.app")
        print("Installed material template enchant as kickapp.djangoapps.mdlenchant")
        print("Installed home template, see home")

    parcefiles([P4A, MAIN], locals())
