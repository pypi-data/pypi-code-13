#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
from .core import core
from .include import Include
from .exceptions import IncludeError
# TODO: Improved error handling.


def _input_file_argument(parser):
    # Input file command line argument.
    input_file_kwargs = {
        "type": str,
        "default": core.default_input_file,
        "metavar": "FILE",
        "help": "python input file",
    }
    parser.add_argument("-f", "--file", **input_file_kwargs)


def _parse_primary_arguments(argv):
    # Parse primary options from command line arguments.
    # Create argument parser and add primary arguments.
    parser = argparse.ArgumentParser(prog=core.name, add_help=False)
    version_argument(parser)
    _input_file_argument(parser)
    # Add target arguments to prevent catching target options.
    target_arguments(parser)

    # Parse known arguments, unhandled arguments passed to secondary parser.
    args, discard = parser.parse_known_args(argv)

    # Returns the input file.
    return args.file


def _parse_secondary_arguments(argv, path):
    # Parse secondary options from command line arguments.
    # Get description from module docstring or fallback on core.
    desc = Include.get_description(path)
    desc = core.description if desc is None else desc

    # Create argument parser, add primary and secondary arguments.
    parser = argparse.ArgumentParser(prog=core.name, description=desc)
    version_argument(parser)
    _input_file_argument(parser)
    logging_arguments(parser)
    # Use included rules in target arguments.
    target_arguments(parser, [key for key in Include.rules()])

    # Parse all arguments, throw exception on unknown.
    args = parser.parse_args(argv)

    # Internal core configuration.
    core.configure(args)

    # Returns argument parser, target name and remainder arguments.
    return (parser, args.target, args.argv)


def _parse_target_arguments(target, rule, argv):
    # Parse target command line arguments using options.
    # Construct program name using target.
    prog = "{} {}".format(core.name, target)
    desc = rule._rule.description

    # Create argument parser for options with target rule description.
    parser = argparse.ArgumentParser(prog=prog, description=desc)

    # Add rule options to parser.
    rule._rule.add_options(parser)

    # Parser remainder argumments using constructed parser.
    args = parser.parse_args(argv)

    # Call rule options with parsed arguments.
    rule._rule.call_options(args)


def version_argument(parser, core=core):
    """Version information command line option, allows override of the core
    class instance where required.

    `parser`
        Instance of ArgumentParser.
    `core`
        Package core instance.
    """
    version_kwargs = {
        "action": "version",
        "version": str("%(prog)s (" + core.version + ")"),
    }
    parser.add_argument("-v", "--version", **version_kwargs)


def logging_arguments(parser, core=core):
    """Logging command line arguments, allows override of the core class
    instance where required.

    `parser`
        Instance of ArgumentParser.
    `core`
        Package core instance.
    """
    # Logging level option.
    log_level_kwargs = {
        "type": str,
        "default": core.DEFAULT_LOG_LEVEL,
        "metavar": "LEVEL",
        "help": "logging level",
    }
    parser.add_argument("-l", **log_level_kwargs)

    # Logging file option.
    log_file_kwargs = {
        "type": str,
        "default": core.DEFAULT_LOG_FILE,
        "metavar": "FILE",
        "help": "logging file",
    }
    parser.add_argument("--log-file", **log_file_kwargs)


def target_arguments(parser, targets=None):
    """Target command line arguments.

    `parser`
        Instance of ArgumentParser.
    """
    # Target name and remainder arguments.
    target_kwargs = {
        "nargs": "?",
        "type": str,
        "help": "target name"
    }
    # Add targets as choices if available.
    if targets is not None:
        target_kwargs["choices"] = targets
    parser.add_argument("target", **target_kwargs)

    # Target remainder arguments.
    argv_kwargs = {
        "nargs": argparse.REMAINDER,
        "help": "target arguments"
    }
    parser.add_argument("argv", **argv_kwargs)


def main(argv=sys.argv[1:], **kwargs):
    """Main command line interface.

    `argv`
        Command line arguments list excluding script name.
    `**kwargs`
        Keyword arguments to internal package core configuration.
    """
    # Default standard output/error streams.
    kwargs.setdefault("stdout", sys.stdout)
    kwargs.setdefault("stderr", sys.stderr)

    # Internal configuration.
    core(**kwargs)

    # Parse primary command line arguments, this supports the `-f/--file`
    # option to load a specified python input file. If not specified the
    # default input file is imported: `$PWD/faffin.py`.
    input_file = _parse_primary_arguments(list(argv))

    # Load available rules from input file using `Include` class.
    try:
        Include(input_file)
    # Catch exceptions for user readability.
    except IncludeError as err:
        # Continue execution to handle help flag.
        core.stderr(err.message)

    # Parse secondary command line arguments, these may depend on rules which
    # have been imported from the input file. Returns the constructed argument
    # parser, target name and remainder arguments.
    parser, target, argv = _parse_secondary_arguments(argv, input_file)

    # If target is not specified, attempt to default to `all`.
    if (target is None) and (Include.get_rule("all") is not None):
        target = "all"

    # If no target, print usage.
    if target is None:
        parser.print_usage()
        return 0

    # Get rule from `Include` class.
    rule = Include.get_rule(target)
    # Write stderr and return if not found.
    if rule is None:
        core.stderr("unknown rule `{}`".format(target))
        return 1

    # Target exists, parse target arguments.
    _parse_target_arguments(target, rule, argv)

    # Call target rule object.
    # TODO: Catch FaffError exceptions.
    success, results = rule()

    # Report information to stdout or stderr based on success.
    info = "`{}` updated ({}/{} {:.3f}s)"
    stream = core.stdout if success else core.stderr
    stream(info, target, results["updated"], results["total"], results["time"])

    # Return code based on rule success.
    return int(success is False)
