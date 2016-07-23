#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

# Core instance and timer utility.
from .core import (core, Timer)

# Reusable parser arguments and main command line interface.
from .main import (version_argument, logging_arguments, target_arguments, main)

# Exceptions for handling.
from .exceptions import (FaffError, InvalidInputFileError,
                         ImportInputFileError, InvalidTargetError,
                         InvalidOptionError)

# Input file classes.
from .include import Include
from .variable import Variable
from .option import Option
from .targets import (Target, RuleTarget, FileTarget)
from .rule import Rule
from .run import Run
