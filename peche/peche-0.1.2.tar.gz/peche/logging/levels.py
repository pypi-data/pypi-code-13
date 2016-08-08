#!/usr/bin/env python
# -*- coding: utf8 -*-

from enum import Enum


class Level(Enum):
    Debug = 10
    Info = 20
    Warn = 30
    Error = 40
    Critical = 50