#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

# Core package instance.
from .core import core

# Reusable parser arguments and main command line interface.
from .main import (version_argument, logging_arguments, target_arguments, main)

# Exceptions for handling.
from .exceptions import (FaffError, IncludeError, VariableError,
                         RuleTargetError, RuleError)

# Input file classes.
from .include import Include
from .variable import (VariableContext, Variable)
from .option import (option, is_option)
from .targets import (Target, RuleTarget, FileTarget)
from .rule import (rule, is_rule)
from .run import (dry_run, run)
