#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import subprocess
import time
from .core import core, Timer
from .targets import Target
from .option import is_option
from .variable import Variable
from .exceptions import (FaffError, RuleError)
# TODO: Refactor this for readability/stability.

# Error messages.
ENORMALISE = "rule `{}` argument `{}` unexpected input"
EARG_LEN = "rule `{}` argument {} has more than two elements"
EARG = "rule `{}` argument {} unexpected input"
EARG_DEPENDS = "rule `{}` target {} dependency {} unexpected input"
EDEPEND = "rule `{}` dependency {} not a `Target` instance"
EOPTION = "rule `{}` option {} not an `Option` instance"
ETARGET = "rule `{}` target {} not a `Target` instance"
ETARGET_DEPENDS = "rule `{}` target {} dependencies not a tuple"
ETARGET_DEPEND = "rule `{}` target {} dependency {} not a `Target` instance"
ETARGET_EXISTS = "rule `{}` target {} does not exist"
ETARGET_RULE_DEPEND_UPDATED = "rule `{}` target {} out of date compared to rule dependency {}"  # noqa
ETARGET_DEPEND_UPDATED = "rule `{}` target {} out of date compared to dependency {}"  # noqa
EEXECUTE = "execute `{}`"


class Rule(object):
    """Default rule function decorator, decorated function is called based on
    the state of targets, their dependencies and other keyword arguments to
    the decorator.

    `func`
        Decorated function.
    `*args`
        Target arguments in a defined rule pattern.
    `**kwargs`
        `depends`
            Optional additional dependencies applied to all rule arguments.
        `options`
            Optional decorated option functions for command line configuration.
        `args`
            Optional arguments passed to decorated function on call.
        `context`
            Optional variable context.

    Decorated functions must have the arguments::

        @rule(...)
        def func(target, depends, args):
            ...

    Where ``target`` is an out of date ``Target`` instance, ``depends`` is a
    list of ``Target`` instance dependencies associated with the target, and
    ``args`` is the value passed to the keyword argument of the same name in
    the decorator.

    When instance is called, rule function will run based on state of targets
    and dependencies, returning a boolean indicating success and results
    dictionary containing more information.
    """

    # Private methods.

    def __init__(self, func, *args, **kwargs):
        # Name, function and description from decorator.
        self._name = func.__name__
        self._func = func
        self._desc = func.__doc__

        # Optional rule dependencies (`depends` keyword argument).
        self._rule_depends = self._normalise("depends", kwargs, Target)

        # Optional rule options (`options` keyword argument).
        self._rule_options = self._normalise("options", kwargs, is_option)

        # Optional rule arguments (`args` keyword argument.)
        self._rule_args = kwargs.get("args", None)

        # Optional variable context argument.
        self._context = kwargs.get("context", None)

        # Targets and dependencies.
        self._targets = []
        self._depends = []

        # Process decorator positional arguments.
        for i, arg in enumerate(args):
            # Break loop if true is not returned.
            if not self._process(i, arg):
                break

        # Cast to tuples internally.
        self._targets = tuple(self._targets)
        self._depends = tuple(self._depends)

        # Check internal data.
        self._check()

    def __call__(self):
        # Internal rule execution method.
        def _execute(target=None, depends=None):
            results = {}
            # Call time elapsed timer.
            with Timer() as t:
                core.debug(__name__, EEXECUTE, self._name)

                # Overridable call method returns none for success.
                results["error"] = self.call(target, depends)

            results["time"] = t.seconds
            return results

        # Rule results dictionary.
        results = {
            # Total number of targets, updated targets.
            "total": len(self._targets),
            "updated": 0,
            # Run results.
            "results": {},
        }

        # Total elapsed timer.
        with Timer() as t:

            if not self.exists():
                results["results"][0] = {"error": "depend error"}
                return self._results(0, results)

            # Check rule dependencies exist, get updated time.
            rd_updates = []

            for i, depend in enumerate(self._rule_depends):
                rd_updates.append(depend.updated())

            # If no target, RulePattern1.
            if results["total"] == 0:
                # Set total counter to 1 for semantics.
                results["total"] = 1

                # Execute rule function.
                results["results"][0] = _execute()

            # Else iterate over targets.
            else:
                # Track which targets to update.
                updates = []

                for i, pair in enumerate(zip(self._targets, self._depends)):
                    target, depends = pair

                    # If depends is none, use empty list.
                    depends = depends if depends else []

                    # Check target dependencies exist, get updated time.
                    d_updates = []

                    for j, depend in enumerate(depends):
                        if target == depend:
                            results["results"][i] = {"error": "circular error"}
                            break
                        else:
                            d_updates.append(depend.updated())

                    # Exit loop if dependency updates not equal.
                    if len(d_updates) != len(depends):
                        break

                    # If target does not exist, update required.
                    if not target.exists():
                        core.debug(__name__, ETARGET_EXISTS, self._name, i)
                        updates.append(True)
                        continue

                    # Get target updated time.
                    updated = target.updated()

                    # Target was just updated.
                    tx = updated - time.time()
                    if abs(tx) < 0.05:
                        updates.append(True)
                        continue

                    # Compare target updated time to rule dependencies.
                    for j, rd_updated in enumerate(rd_updates):
                        if updated <= rd_updated:
                            core.debug(
                                __name__, ETARGET_RULE_DEPEND_UPDATED,
                                self._name, i, j)
                            updates.append(True)
                            break

                    # Compare target updated time to dependencies.
                    for j, d_updated in enumerate(d_updates):
                        if updated <= d_updated:
                            core.debug(
                                __name__, ETARGET_DEPEND_UPDATED,
                                self._name, i, j)
                            updates.append(True)
                            break

                    # Target does not require update.
                    if len(updates) != (i + 1):
                        updates.append(False)

                # Do not execute if error occurred.
                if len(updates) == len(self._targets):
                    # Execute rule function for target updates.
                    for i, pair in enumerate(zip(self._targets, self._depends)):
                        target, depends = pair
                        update = updates[i]

                        # If update required, run rule function.
                        if update:
                            ctx = Variable.save("_", self._context)

                            # Automatic target, dependency variables.
                            Variable("_T", str(target), self._context)
                            if depends is not None:
                                Variable("_D", " ".join([str(x) for x in depends]), self._context)

                            # Call using internal function.
                            results["results"][i] = _execute(target, depends)

                            # Restore variable values.
                            Variable.restore(ctx, self._context)

        return self._results(t.seconds, results)

    def _normalise(self, key, kwargs, cls):
        # Get value from keyword arguments, default to empty list.
        arg = kwargs.get(key, [])

        # Wrap argument as tuple for consistency.
        if isinstance(arg, list) or isinstance(arg, tuple):
            return tuple(arg)
        elif isinstance(cls, type):
            if isinstance(arg, cls):
                return tuple([arg])
        elif cls(arg):
            return tuple([arg])

        # Raise error for unexpected input.
        core.raise_exception(
            ENORMALISE, self._name, key, cls=RuleError)

    def _process(self, i, arg):
        # If argument is Target instance, RulePattern2.
        if isinstance(arg, Target):
            self._targets.append(arg)
            self._depends.append(None)
            return True

        # Else if argument is list or tuple.
        elif isinstance(arg, list) or isinstance(arg, tuple):

            # Raise error if list length is greater than two.
            if len(arg) > 2:
                core.raise_exception(
                    EARG_LEN, self._name, i, cls=RuleError)

            # Extract targets, dependencies from argument list.
            targets = arg[0] if len(arg) > 0 else None
            depends = arg[1] if len(arg) > 1 else None

            # If targets is Target instance.
            if isinstance(targets, Target):
                self._targets.append(targets)

                # If dependencies is Target instance, RulePattern3.
                if isinstance(depends, Target):
                    self._depends.append(tuple([depends]))
                    return True

                # Else if dependencies is list or tuple, RulePattern4.
                elif isinstance(depends, list) or isinstance(depends, tuple):
                    self._depends.append(tuple(depends))
                    return True

            # Else if targets is list or tuple.
            elif isinstance(targets, list) or isinstance(targets, tuple):

                # If dependencies is a Target instance, RulePattern5.
                if isinstance(depends, Target):
                    for target in targets:
                        self._targets.append(target)
                        self._depends.append(tuple([depends]))
                    return True

                # Else if dependencies is list or tuple.
                elif isinstance(depends, list) or isinstance(depends, tuple):

                    # If not equal in length, RulePattern7.
                    if len(targets) != len(depends):
                        for target in targets:
                            self._targets.append(target)
                            self._depends.append(tuple(depends))
                        return True

                    # If equal in length.
                    for j, pair in enumerate(zip(targets, depends)):
                        target, depend = pair
                        self._targets.append(target)

                        # If dependency is Target, RulePattern6.
                        if isinstance(depend, Target):
                            self._depends.append(tuple([depend]))

                        # Else if dependency is list or tuple, RulePattern8.
                        elif (isinstance(depend, list) or
                              isinstance(depend, tuple)):
                            self._depends.append(tuple(depend))

                        # Unknown dependency argument.
                        else:
                            core.raise_exception(
                                EARG_DEPENDS, self._name, i, j,
                                cls=RuleError)
                    return True

        # No arguments, RulePattern1.

        # Raise error for unknown argument.
        core.raise_exception(
            EARG, self._name, i, cls=RuleError)

    def _check(self):
        # Rule dependencies must be list of Target instances.
        for i, depend in enumerate(self._rule_depends):
            if not isinstance(depend, Target):
                core.raise_exception(
                    EDEPEND, self._name, i, cls=RuleError)

        # Rule options must be list of options.
        for i, opt in enumerate(self._rule_options):
            if not is_option(opt):
                core.raise_exception(
                    EOPTION, self._name, i, cls=RuleError)

        # Targets must be a list of Target instances.
        for i, pair in enumerate(zip(self._targets, self._depends)):
            target, depends = pair
            if not isinstance(target, Target):
                core.raise_exception(
                    ETARGET, self._name, i, cls=RuleError)

            # Skip dependencies checks.
            if depends is None:
                continue

            # Target dependencies must be a list of lists of Target instances.
            if not isinstance(depends, tuple):
                core.raise_exception(
                    ETARGET_DEPENDS, self._name, i, cls=RuleError)
            for j, depend in enumerate(depends):
                if not isinstance(depend, Target):
                    core.raise_exception(
                        ETARGET_DEPEND, self._name, i, j, cls=RuleError)

    def _results(self, seconds, results):
        # Process results dictionary to determine success.
        success = True

        for i, result in results["results"].items():
            # Write error messages to stderr.
            if result["error"] is not None:
                core.write_stderr(result["error"])
                success = False
            else:
                results["updated"] += 1

        results["time"] = seconds
        return (success, results)

    # Public methods.

    def exists(self):
        """Return true if rule dependencies exist."""
        # Check rule dependencies exist.
        for depend in self._rule_depends:
            if not depend.exists():
                return False

        # Check dependencies of each target.
        for depends in self._depends:
            if depends is not None:
                for depend in depends:
                    if not depend.exists():
                        return False

        # Dependencies exist.
        return True

    def call(self, target=None, depends=None):
        """TODO: Documentation."""
        # TODO: Make this overridable for subclasses.
        try:
            self._func(target, depends, self._rule_args)
        except KeyboardInterrupt:
            return "keyboard interrupt"
        except subprocess.CalledProcessError as e:
            # Subprocess error during function call.
            return e.output
        except FaffError as e:
            return e.message
        # TODO: Catch unknown exceptions.

    def add_options(self, parser):
        """Add rule options to argument parser instance.

        `parser`
            Instance of ArgumentParser.
        """
        for opt in self._rule_options:
            opt.add(parser)

    def call_options(self, args):
        """Call rule options with arguments returned by argument parser.

        `args`
            Instance of argparse.Namespace.
        """
        for opt in self._rule_options:
            opt(getattr(args, opt.name()))

    def description(self):
        """Return rule description string."""
        return self._desc

    def targets(self):
        """Return list of rule targets."""
        return self._targets


def rule(*args, **kwargs):
    """Rule function decorator, function and arguments used to create a
    ``Rule`` instance.

    `*args`
        Positional arguments to ``Rule`` class.
    `**kwargs`
        Keyword arguments to ``Rule`` class.
    """
    def _decorator(func):
        # TODO: Use rule subclasses here, keyword argument?
        _rule = Rule(func, *args, **kwargs)

        @functools.wraps(func)
        def _func():
            return _rule()

        _func._rule = _rule
        return _func
    return _decorator


def is_rule(obj):
    """Return true if object is a rule instance.

    `obj`
        Object instance.
    """
    if hasattr(obj, "_rule"):
        return isinstance(obj._rule, Rule)
    return False
