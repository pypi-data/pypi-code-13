#!/usr/bin/env python3

from core import Interpreter

i = Interpreter()
i.config()
i.ingest()
i.structure()
i.write()