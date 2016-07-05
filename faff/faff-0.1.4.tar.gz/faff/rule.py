#!/usr/bin/env python
"""
Rule class function decorator.
"""
import subprocess
from .core import core, Timer
from .targets import Target
from .option import Option
from .variable import Variable
from .exceptions import (
    InvalidTargetError,
    InvalidOptionError,
)


class Rule(object):
    """
    Rule function decorator class.
    """
    class InternalRule(object):
        """
        Internal rule class.
        """
        # Error messages.
        EKWARG_DEPENDS = "rule `{}` argument `depends` is not an instance of `Target` class or a list"  # noqa
        EKWARG_OPTIONS = "rule `{}` argument `options` is not an instance of `Option` class or a list"  # noqa
        EARG_LEN = "rule `{}` argument {} is a list of length greater than two"  # noqa
        EARG_DEPEND = "rule `{}` argument {} dependencies is not an instance of `Target` class or a list"  # noqa
        EARG_TARGET = "rule `{}` argument {} targets is not an instance of `Target` class or a list"  # noqa
        EDEPEND = "rule `{}` dependency {} is not an instance of `Target` class"  # noqa
        EOPTION = "rule `{}` option {} is not an instance of `Option` class"
        ETARGET = "rule `{}` target {} is not an instance of `Target` class"
        ETARGET_DEPENDS = "rule `{}` target {} dependencies is not a list"
        ETARGET_DEPEND = "rule `{}` target {} dependency {} is not an instance of `Target` class"  # noqa

        def __init__(self, *args, **kwargs):
            """
            Construct internal data from decorator arguments.
            """
            # Name, callback and description provided by default.
            self._name = kwargs.get("name")
            self._callback = kwargs.get("callback")
            self._description = kwargs.get("description")

            # Optional rule dependencies (`depends` keyword argument).
            rule_depends = kwargs.get("depends", [])

            # Wrap argument in list for easier handling.
            if isinstance(rule_depends, Target):
                self._rule_depends = [rule_depends]
            # Set attribute now (checked later).
            elif isinstance(rule_depends, list):
                self._rule_depends = rule_depends
            # Else raise an error for invalid argument.
            else:
                core.raise_exception(
                    self.EKWARG_DEPENDS, self._name,
                    cls=InvalidTargetError,
                )

            # Optional rule command line options (`options` keyword argument).
            rule_options = kwargs.get("options", [])

            # Wrap argument in list for easier handling.
            if Option.is_option(rule_options):
                self._rule_options = [rule_options]
            # Set attribute now (checked later).
            elif isinstance(rule_options, list):
                self._rule_options = rule_options
            # Else raise error for invalid argument.
            else:
                core.raise_exception(
                    self.EKWARG_OPTIONS, self._name,
                    cls=InvalidOptionError,
                )

            # Optional rule arguments (`args` keyword argument).
            self._args = kwargs.get("args", None)

            # Targets and target dependencies attributes.
            self._targets = []
            self._depends = []

            # Decorator positional arguments.
            for i, arg in enumerate(args):
                # If argument is a Target instance, RulePattern2.
                if isinstance(arg, Target):
                    self._targets.append(arg)
                    self._depends.append(None)

                # Else if argument is list.
                elif isinstance(arg, list):

                    # Raise error if list has more than two elements.
                    if len(arg) > 2:
                        core.raise_exception(
                            self.EARG_LEN, self._name, i,
                            cls=InvalidTargetError,
                        )

                    # Extract target, dependencies from argument list.
                    targets = arg[0] if len(arg) > 0 else None
                    depends = arg[1] if len(arg) > 1 else None

                    # If targets is a Target instance.
                    if isinstance(targets, Target):
                        self._targets.append(targets)

                        # If depends is a Target instance, RulePattern3.
                        if isinstance(depends, Target):
                            self._depends.append([depends])
                        # Else if depends is a list, RulePattern4.
                        elif isinstance(depends, list):
                            self._depends.append(depends)
                        # Else raise error for invalid argument.
                        else:
                            core.raise_exception(
                                self.EARG_DEPEND, self._name, i,
                                cls=InvalidTargetError,
                            )

                    # Else if targets is a list of Target instances.
                    elif isinstance(targets, list):

                        # If depends is a Target instance, RulePattern5.
                        if isinstance(depends, Target):
                            for target in targets:
                                self._targets.append(target)
                                self._depends.append([depends])

                        # Else if depends is a list.
                        elif isinstance(depends, list):

                            # If lists are equal in length.
                            if len(targets) == len(depends):
                                for target, depend in zip(targets, depends):
                                    self._targets.append(target)

                                    # If depend is a Target, RulePattern6.
                                    if isinstance(depend, Target):
                                        self._depends.append([depend])
                                    # Else if depend is a list, RulePattern8.
                                    elif isinstance(depend, list):
                                        self._depends.append(depend)
                                    # Else unknown depends argument.
                                    else:
                                        core.raise_exception(
                                            self.EARG_DEPEND, self._name, i,
                                            cls=InvalidTargetError,
                                        )

                            # Else, RulePattern7.
                            else:
                                for target in targets:
                                    self._targets.append(target)
                                    self._depends.append(depends)
                        # Else unknown depends argument.
                        else:
                            core.raise_exception(
                                self.EARG_DEPEND, self._name, i,
                                cls=InvalidTargetError,
                            )
                    # Else unknown targets argument.
                    else:
                        core.raise_exception(
                            self.EARG_TARGET, self._name, i,
                            cls=InvalidTargetError,
                        )
                # Else unknown primary argument.
                else:
                    core.raise_exception(
                        self.EARG_TARGET, self._name, i,
                        cls=InvalidTargetError,
                    )

            # No arguments, RulePattern1.

            # Test internal data for correctness.
            # Rule dependencies must be a list of Target instances.
            for i, depend in enumerate(self._rule_depends):
                assert isinstance(depend, Target), (
                    self.EDEPEND.format(self._name, i)
                )
            # Rule options must be a list of Option instances.
            for i, option in enumerate(self._rule_options):
                assert Option.is_option(option), (
                    self.EOPTION.format(self._name, i)
                )
            # Targets must be a list of Target instances.
            # Target dependencies must be a list of lists of Target instances.
            pairs = zip(self._targets, self._depends)
            for i, pair in enumerate(pairs):
                target, depends = pair
                assert isinstance(target, Target), (
                    self.ETARGET.format(self._name, i)
                )
                if depends is not None:
                    assert isinstance(depends, list), (
                        self.ETARGET_DEPENDS.format(self._name, i)
                    )
                    for j, depend in enumerate(depends):
                        assert isinstance(depend, Target), (
                            self.ETARGET_DEPEND.format(self._name, i, j)
                        )

        def __call__(self):
            """
            Return tuple of (success, updated, total, elapsed). Where success
            is boolean indicating whether an error occurred during a callback.
            Updated is the number of successfully updated targets, total is the
            total number of targets and elapsed is time taken in seconds.
            """
            # TODO: Rule callback concurrency using deco?
            def _rule_callback(callback, target=None, depends=None, args=None):
                """
                Execute rule callback.
                """
                result = {"error": None}

                with Timer() as timer:
                    try:
                        callback(target, depends, args)
                    except KeyboardInterrupt:
                        result["error"] = "keyboard interrupt"
                    except subprocess.CalledProcessError as e:
                        # Subprocess error during callback.
                        result["error"] = e.output
                    except Exception as e:
                        # Catch generic/unknown exceptions.
                        result["error"] = str(e)

                # Record time taken in seconds.
                result["time"] = timer.seconds
                return result

            def _rule_single(callback, args=None):
                """
                Execute single rule callback without target/dependencies.
                """
                return {
                    0: _rule_callback(callback, args=args),
                }

            def _rule_multiple(callback, targets, depends, args, update=False):
                """
                Execute multiple rule callbacks with targets/dependencies.
                """
                # For each Target instance and dependencies list.
                pairs = zip(targets, depends)
                results = {}

                for i, pair in enumerate(pairs):
                    target, depends = pair

                    # Use update override.
                    upd = update

                    # Save current automatic variables context.
                    ctx = Variable.save()

                    # Use target class method to populate automatic variables.
                    Target.set_variables(target, depends)

                    # Update if target out of date.
                    if target.out_of_date():
                        upd = True

                    # Update if target out of date compared to dependencies.
                    if depends is not None:
                        for depend in depends:
                            if target.out_of_date(depend):
                                upd = True

                    # If update required, run rule callback.
                    if upd:
                        results[i] = _rule_callback(
                            callback, target, depends, args
                        )

                    # Restore variable context.
                    Variable.restore(ctx)

                return results

            # Rule keyword argument dependencies override update.
            update = False

            # Check rule dependencies are up to date.
            for depend in self._rule_depends:
                if depend.out_of_date():
                    update = True

            # Total number of targets. updated.
            total = len(self._targets)

            # If targets list empty, single thread rule callback.
            if total == 0:
                # Adjust total to one for output readability.
                total = 1
                results = _rule_single(
                    self._callback,
                    self._args,
                )
            # Else pass target list to multiple threaded rule callback.
            else:
                results = _rule_multiple(
                    self._callback,
                    self._targets,
                    self._depends,
                    self._args,
                    update,
                )

            # Track success, number of updated targets and time taken.
            success = True
            updated = 0
            elapsed = 0

            for i, result in results.items():
                # Write error messages to stderr.
                if result["error"] is not None:
                    core.write_stderr(result["error"])
                    success = False
                else:
                    updated += 1

                # Increment elapsed counter.
                elapsed += result["time"]

            return (success, updated, total, elapsed)

        def add_options(self, parser):
            """
            Add rule option arguments to parser provided by argparse.
            """
            for opt in self._rule_options:
                opt.add_argument(parser)

        def call_options(self, args):
            """
            Call rule options with arguments returned by argparse.
            """
            for opt in self._rule_options:
                opt(getattr(args, opt.get_name()))

        def get_description(self):
            """
            Return rule description.
            """
            return self._description

        def get_targets(self):
            """
            Return internal list of rule targets.
            """
            return self._targets

    def __init__(self, *args, **kwargs):
        """
        Positional and keyword arguments passed to call method.
        """
        self._args = args
        self._kwargs = kwargs

    def __call__(self, callback):
        """
        Construct an internal rule instance from decorator arguments.
        """
        self._kwargs.setdefault("name", callback.__name__)
        self._kwargs.setdefault("callback", callback)
        self._kwargs.setdefault("description", callback.__doc__)
        return self.InternalRule(*self._args, **self._kwargs)

    @staticmethod
    def is_rule(obj):
        """
        Test if object is a rule instance.
        """
        if isinstance(obj, Rule.InternalRule):
            return True
        return False
