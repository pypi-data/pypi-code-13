#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import os, os.path as p
import json
from core.tools import cvd, wtf


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
            print("no engine.json in this directory")

    def ingest(self):

        s = self.options.get("src", None)

        if not s:
            self.options["src"] = "game.html"

        path = p.join(self.loc, p.join(self.options["cwd"], self.options["src"]))
        self.rawHtml = bs(open(path), "html.parser")

    def structure(self):
        print("generating JSON")

        i = self.options.get("toplevelid", None)

        if not i:
            self.DOM = cvd(self.rawHtml.find(id="start"))
        else:
            self.DOM = cvd(self.rawHtml.find(id=self.options["toplevelid"]))

        self.JSON = json.dumps(self.DOM)

    def write(self):

        d = self.options.get("dest", None)
        if not d:
            print("writing to {0}".format("simpleDom.js"))
            wtf(self.JSON, path="simpleDom.js")
        else:
            print("writing to {0}".format(self.options["dest"]))
            wtf(self.JSON, path=self.options["dest"])
