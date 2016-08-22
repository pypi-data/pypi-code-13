#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import subprocess
import time
from .core import core
from .targets import Target
from .option import is_option
from .variable import Variable
from .exceptions import (FaffError, RuleError)
# TODO: Rethink options for handling over multiple rules.

# Error messages.
ENORMALISE = "rule `{}` argument `{}` unexpected input"
EARG_LEN = "rule `{}` argument {} has more than two elements"
EARG = "rule `{}` argument {} unexpected input"
EARG_DEPENDS = "rule `{}` target {} dependency {} unexpected input"
EDEPEND = "rule `{}` dependency {} not a `Target` instance"
EDEPEND_EXISTS = "rule `{}` dependencies do not exist"
EDEPEND_CIRCULAR = "rule `{}` target {} dependency {} is circular"
EOPTION = "rule `{}` option {} not an `Option` instance"
ETARGET = "rule `{}` target {} not a `Target` instance"
ETARGET_DEPENDS = "rule `{}` target {} dependencies not a tuple"
ETARGET_DEPEND = "rule `{}` target {} dependency {} not a `Target` instance"
ETARGET_EXISTS = "rule `{}` target {} does not exist"
ETARGET_RULE_DEPEND_UPDATED = "rule `{}` target {} out of date compared to rule dependency {}"  # noqa
ETARGET_DEPEND_UPDATED = "rule `{}` target {} out of date compared to dependency {}"  # noqa
EKEYBOARD_INT = "rule `{}` keyboard interrupt"


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
        def func(**kwargs):
            ...

    Where keyword arguments contain the following:

    `target`
        Out of date ``Target`` instance.
    `depends`
        List of ``Target`` instance dependencies associated with target.
    `options`
        Dictionary of option decorator argument values.
    `args`
        Optional arguments passed to decorator.

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
        self._description = func.__doc__

        # Optional rule dependencies (`depends` keyword argument).
        self._rule_depends = self._normalise("depends", kwargs, Target)

        # Optional rule options (`options` keyword argument).
        self._rule_options = self._normalise("options", kwargs, is_option)
        self._opt_values = {}

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

    def __call__(self, opt_values=None):
        # Determine which targets, dependencies require update.
        # Rule results dictionary.
        results = {
            # Total number of targets, updated targets.
            "total": len(self._targets),
            "updated": 0,
            # Total time elapsed (calculated in ._results() method).
            "time": time.time(),
            # Individual target results.
            "results": {},
        }
        # Rule keyword arguments.
        kwargs = {
            # Used to pass option values to rule targets .updated() method.
            "options": self._opt_values if opt_values is None else opt_values,
            "args": self._rule_args,
        }

        # If rule dependencies do not exist, return error.
        if not self.exists():
            results["results"][0] = {
                "error": EDEPEND_EXISTS.format(self._name)}
            return self._results(results)

        # Get rule dependencies updated time.
        rdepends_updated = []
        for depend in self._rule_depends:
            rdepends_updated.append(
                depend.updated(opt_values=kwargs["options"]))

        # If RulePattern1 (no targets).
        if results["total"] == 0:
            # Set total counter to 1 for semantics, update rule.
            results["total"] = 1
            results["results"] = self.update(**kwargs)
            return self._results(results)

        # Track targets to update, associated dependencies.
        rtargets = []
        rdepends = []

        # Else iterate over targets.
        for i, pair in enumerate(zip(self._targets, self._depends)):
            target, depends = pair

            # If depends is none, use empty list.
            depends = [] if depends is None else depends

            # Check dependencies are not circular, get updated time.
            tdepends_updated = []
            for j, depend in enumerate(depends):
                if target == depend:
                    results["results"][i] = {
                        "error": EDEPEND_CIRCULAR.format(self._name, i, j)}
                    break
                tdepends_updated.append(
                    depend.updated(opt_values=kwargs["options"]))

            # Exit loop if dependency error.
            if len(tdepends_updated) != len(depends):
                break

            # If target does not exist, update required.
            if not target.exists():
                core.debug(__name__, ETARGET_EXISTS, self._name, i)
                rtargets.append(target)
                rdepends.append(depends)
                continue

            # Judge if the target was just updated.
            updated = target.updated(opt_values=kwargs["options"])
            if abs(updated - time.time()) < 0.05:
                rtargets.append(target)
                rdepends.append(depends)
                continue

            # Continue loop if update required.
            # TODO: Cleaner way to do this.
            update = False

            # Compare target updated time to rule dependencies.
            for j, rd_updated in enumerate(rdepends_updated):
                if updated <= rd_updated:
                    core.debug(
                        __name__, ETARGET_RULE_DEPEND_UPDATED,
                        self._name, i, j)
                    rtargets.append(target)
                    rdepends.append(depends)
                    update = True
                    break

            if update:
                continue

            # Compare target updated time to dependencies.
            for j, td_updated in enumerate(tdepends_updated):
                if updated <= td_updated:
                    core.debug(
                        __name__, ETARGET_DEPEND_UPDATED,
                        self._name, i, j)
                    rtargets.append(target)
                    rdepends.append(depends)
                    break

        # Update rule if targets to update and loop did not exit early.
        if (len(rtargets) > 0) and (len(rtargets) == len(rdepends)):
            results["results"] = self.update(rtargets, rdepends, **kwargs)
        return self._results(results)

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
        core.exception(ENORMALISE, self._name, key, cls=RuleError)

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
                core.exception(EARG_LEN, self._name, i, cls=RuleError)

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
                            core.exception(
                                EARG_DEPENDS, self._name, i, j, cls=RuleError)
                    return True

        # No arguments, RulePattern1.

        # Raise error for unknown argument.
        core.exception(EARG, self._name, i, cls=RuleError)

    def _check(self):
        # Rule dependencies must be list of Target instances.
        for i, depend in enumerate(self._rule_depends):
            if not isinstance(depend, Target):
                core.exception(EDEPEND, self._name, i, cls=RuleError)

        # Rule options must be list of options.
        for i, opt in enumerate(self._rule_options):
            if not is_option(opt):
                core.exception(EOPTION, self._name, i, cls=RuleError)

        # Targets must be a list of Target instances.
        for i, pair in enumerate(zip(self._targets, self._depends)):
            target, depends = pair
            if not isinstance(target, Target):
                core.exception(ETARGET, self._name, i, cls=RuleError)

            # Skip dependencies checks.
            if depends is None:
                continue

            # Target dependencies must be a list of lists of Target instances.
            if not isinstance(depends, tuple):
                core.exception(ETARGET_DEPENDS, self._name, i, cls=RuleError)
            for j, depend in enumerate(depends):
                if not isinstance(depend, Target):
                    core.exception(
                        ETARGET_DEPEND, self._name, i, j, cls=RuleError)

    def _results(self, results):
        # Process results dictionary to determine success.
        success = True

        for i, result in results["results"].items():
            # Write error messages to stderr.
            if result["error"] is not None:
                core.stderr(result["error"])
                success = False
            else:
                results["updated"] += 1

        results["time"] = time.time() - results["time"]
        return (success, results)

    # Public properties, methods.

    @property
    def name(self):
        """Return rule name string."""
        return self._name

    @property
    def description(self):
        """Return rule description string."""
        return self._description

    @property
    def targets(self):
        """Return list of rule targets."""
        return self._targets

    def add_options(self, parser):
        """Add rule options to argument parser instance.

        `parser`
            Instance of ArgumentParser.
        """
        for opt in self._rule_options:
            opt._option.add(parser)

    def call_options(self, args):
        """Call rule options with arguments returned by argument parser.

        `args`
            Instance of argparse.Namespace.
        """
        for opt in self._rule_options:
            value = getattr(args, opt._option.name)
            self._opt_values[opt._option.name] = value
            opt._option(value)

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

    # Reimplemented methods.

    def update(self, targets=None, depends=None, **kwargs):
        """Update rule targets and dependencies, serial implementation.

        `targets`
            List of out of date targets.
        `depends`
            List of lists of dependencies associated with targets.
        """
        def _update(kwargs):
            # Rule function call.
            result = {
                # Elapsed time for this target.
                "time": time.time(),
                "error": None,
            }
            try:
                self._func(**kwargs)
            except KeyboardInterrupt:
                result["error"] = EKEYBOARD_INT.format(self._name)
            except subprocess.CalledProcessError as err:
                result["error"] = err.output
            except FaffError as err:
                result["error"] = err.message
            # TODO: Catch generic exceptions?

            # Calculate elapsed time, set result.
            result["time"] = time.time() - result["time"]
            return result

        # Update results, keyword arguments.
        results = {}

        # RulePattern1, no targets.
        if (targets is None) and (depends is None):
            results[0] = _update(kwargs)
            return results

        # Iterate over targets, dependencies lists.
        for i, pair in enumerate(zip(targets, depends)):
            target, depends = pair
            kwargs["target"] = target
            kwargs["depends"] = depends

            # Save variable context, set automatic variables.
            ctx = Variable.save("_", self._context)
            Variable("_T", str(target), self._context)
            Variable("_D", " ".join([str(x) for x in depends]), self._context)

            # Update rule function.
            results[i] = _update(kwargs)

            # Restore variable values.
            Variable.restore(ctx, self._context)

        return results


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
        def _func(*args):
            return _rule(*args)

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
