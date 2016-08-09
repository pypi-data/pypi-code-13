"""
Magic Bower

It's a dev tool for 3rd party assets using bower.

Its main purpose to only keep the necessary files of the 3rd party.

3rdparty vendors are place under /assets/Magic/vendor

Do not put non bower files in the /assets/Magic/vendor directory.

Place your files in /assets/Magic/lib

Dependencies: Bower

To run this file: python magic-bower.py

"""

import os
import sh
import json
from flask_magic import utils

VERSION = "0.1.0"


DEPENDENCIES = {
    "jquery": {
        "version": "~2.2.4",
        "copy": ["dist/jquery.min.js"]
    },
    "bootstrap": {
        "version": "^3.3.6",
        "copy": ["dist/css",
                 "dist/fonts",
                 "dist/js"]
    },
    "font-awesome": {
        "version": "^4.0.0",
        "copy": ["css/", "fonts/"]
    },
    "jquery-form-validator": {
        "version": "~2.2.8",
        "copy": ["form-validator/"]
    },
    "jquery-lazy": {
        "version": "~1.6.5",
        "copy": ["jquery.lazy.min.js"]
    },
    "js-cookie": {
        "version": "~2.1.0",
        "copy": ["src/js.cookie.js"]
    },
    "jssocials": {
        "version": "~1.1.0",
        "copy": ["dist/jssocials.js",
                 "dist/jssocials.css",
                 "dist/jssocials-theme-flat.css"]
    },
    "bootstrap-social": {
        "version": "~4.9.0",
        "copy": ["bootstrap-social.css"]
    },
    "bootstrap-datepicker": {
        "version": "~1.6.1",
        "copy": ["dist/css",
                 "dist/js",
                 "dist/locales"]
    }
}

# ------------------------------------------------------------------------------
# DO NOT CHANGE BELOW
# ------------------------------------------------------------------------------

CWD = os.getcwd()
VENDOR_DIR = "%s/Magic/vendor" % CWD
BOWER_COMPONENTS_DIR = "%s/bower_components" % CWD

print("-" * 80)
print("Flask Magic Bower")
print("")

bower = {
    "name": "Magic",
    "version": VERSION,
    "dependencies": {d:v["version"] for d, v in DEPENDENCIES.items()}
}

if os.path.exists(VENDOR_DIR):
    utils.remove_dir(VENDOR_DIR)

if not os.path.exists(VENDOR_DIR):
    utils.make_dirs(VENDOR_DIR)

print("Saving bower.json ...")
with open("./bower.json", "w+") as f:
    f.write(json.dumps(bower))

print("Running bower install ...")
with sh.pushd(CWD):
    sh.bower("install")

print("Copying files to vendor directories ...")
for name, v in DEPENDENCIES.items():
    vendor_dir = "%s/%s" % (VENDOR_DIR, name)
    if not os.path.exists(vendor_dir):
        utils.make_dirs(vendor_dir)
    if "copy" in v:
        for f in v["copy"]:
            source = "%s/%s/%s" % (BOWER_COMPONENTS_DIR, name, f)
            dest = "%s/%s" % (vendor_dir, f)
            f = f.rsplit("/", 1)[1] if "/" in f else f
            dest = "%s/%s" % (vendor_dir, f)
            if f.endswith(".css") or f.endswith(".js"):

                utils.copy_file(source, dest)
            else:
                utils.copy_dir(source, dest)
                pass

print("Cleaning up...")
if os.path.exists(BOWER_COMPONENTS_DIR):
    utils.remove_dir(BOWER_COMPONENTS_DIR)

print("Done!")

