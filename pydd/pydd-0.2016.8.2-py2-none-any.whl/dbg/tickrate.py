#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    pydd/dbg/tickrate.py

    @tickrate(var, 1000, fd="sys.stdout")
    def ...

    with tickratecb([var1, var2], "10s", callback=func):   # anytime
    ...

    tickrate((in_speed, out_speed, bytes), "1m", {})


    jedna instancja w wielu miejscach wyswietla raty roznych parametrow
    jednocześnie robiąc rate-limit


"""

