#!/usr/bin/env python3

from core import interpreter

i = interpreter()
i.config()
i.ingest()
i.structure()
i.write()