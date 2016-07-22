# -*- coding: utf-8 -*-
from jschema.make._options import Options
from jschema.make._golang_maker import GolangMaker


def make_golang(schema, options):
    maker = GolangMaker(schema, Options(options))
    maker.find_structs()
    maker.save_structs()
