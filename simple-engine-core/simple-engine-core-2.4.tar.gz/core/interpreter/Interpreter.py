#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import os, os.path as p
import json
from core.tools import cvd, wtf, lbl


class Interpreter:

    def __init__(self, loc=os.getcwd()):

        self.loc = loc
        self.rawHtml = ""

        self.options = {}

        self.DOM = ""
        self.JSON = ""

    def config(self):
        print("loading config")

        try:
            with open(p.join(self.loc, "engine.json"), "r") as f:
                self.options = json.loads(f.read())
        except FileNotFoundError:
            print("No engine.json found - generating defaults")

            self.options = {
                "cwd": ".",
                "dest": "./simpleDom.js",
                "toplevelid": "start",
                "src": "game.html"
            }

            print(lbl(self.options))

    def ingest(self):

        s = self.options.get("src", None)
        c = self.options.get("cwd", None)

        if not s:
            self.options["src"] = "game.html"
        elif not c:
            self.options["cwd"] = "."

        path = p.join(self.loc, p.join(self.options["cwd"], self.options["src"]))
        self.rawHtml = bs(open(path), "html.parser")

    def structure(self):
        print("generating JSON")

        i = self.options.get("toplevelid", None)

        if not i:
            self.options["toplevelid"] = "start"

        self.DOM = cvd(self.rawHtml.find(id=self.options["toplevelid"]))
        self.JSON = json.dumps(self.DOM)

    def write(self):

        d = self.options.get("dest", None)

        if not d:
            self.options["dest"] = "simpleDom.js"

        print("writing to {0}".format(self.options["dest"]))
        wtf(self.JSON, path=self.options["dest"])
