"""Decorate a module's main function.

Copyright 2015, 2016 Dana Scott

This file is part of Clops.

Clops is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.

Clops is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with Clops. If not, see <http://www.gnu.org/licenses/>.

"""
import json
import logging
import logging.config
import os
import sys


logger = logging.getLogger(__name__)


class UpdateDict:
    """Populate a dict with values from a user via JSON.

    Args:
        d: The dict to be updated.
        doc: The __doc__ special attribute of the main module.

    """

    _windows_doc = ("Windows requires a .py file extension "
                    "to run a Python script.\n\n"
                    "For a JSON string argument on a Windows command line:\n"
                    "    Don't quote the outermost braces.\n"
                    "    Exclude spaces.\n"
                    "    Quote string types with three quotation marks.\n"
                    "    Escape path delimiters with a single backslash.\n")

    _logging_doc = ("Logging config:\n"
                    "    \"level\": Don't log events "
                    "that are < this integer.\n"
                    "    CRITICAL 50\n"
                    "    ERROR 40\n"
                    "    WARNING 30\n"
                    "    INFO 20\n"
                    "    DEBUG 10\n"
                    "    NOTSET 0\n")

    _logging_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'yaml': {
                'format': ('---\n'
                           'Datetime: %(asctime)s\n'
                           'Level: %(levelname)s\n'
                           'Logger: %(name)s\n'
                           'Line: %(lineno)d\n'
                           'Message: %(message)s\n')
            },
        },
        'handlers': {
            'stream': {
                'class': 'logging.StreamHandler',
                'formatter': 'yaml',
            },
        },
        'loggers': {
            '': {
                'handlers': ['stream'],
                'level': logging.WARNING,
            },
        }
    }

    def __init__(self, d, doc):
        """Customize an UpdateDict object."""
        self.d = d
        self.doc = doc

    def __call__(self, func):
        """Run a module's main function conditionally.

        Args:
            func: A callable object.

        Returns:
            A function.

        """
        def wrapper():
            if len(sys.argv) == 1:
                # No args.
                pass
            elif len(sys.argv) > 1 and sys.argv[1] == '--help':
                self._print_usage()
            elif len(sys.argv) > 1 and sys.argv[1] == '--json':
                json_string = sys.argv[2]
                self._add_user_values(json_string)
            elif len(sys.argv) > 1 and sys.argv[1] == '--json-file':
                json_file = sys.argv[2]
                with open(json_file) as f:
                    json_string = f.read()
                self._add_user_values(json_string)
            else:
                self._print_usage()
            logging.config.dictConfig(self._logging_dict)
            return func()
        return wrapper

    def _print_usage(self):
        print(*("Usage: {} [ --help | --json STR | --json-file PATH ]\n"
                .format(os.path.basename(sys.argv[0])),
                self.doc,
                "Default values:",
                json.dumps(self.d,
                           sort_keys=True,
                           indent=4,
                           separators=(',', ': ')),
                self._windows_doc,
                self._logging_doc,
                "Default values:",
                json.dumps(self._logging_dict,
                           sort_keys=True,
                           indent=4,
                           separators=(',', ': '))),
              sep='\n')
        sys.exit()

    def _add_user_values(self, json_string):
        try:
            user_values = json.loads(json_string)
        except ValueError:
            sys.exit(2)
        else:
            default_user_values = {k: v
                                   for k, v in user_values.items()
                                   if k in self.d}
            self.d.update(default_user_values)
            logging_user_values = {k: v
                                   for k, v in user_values.items()
                                   if k not in self.d}
            self._logging_dict = _update_nested_dict(self._logging_dict,
                                                     logging_user_values)


def _update_nested_dict(old, new):
    updated = {}
    old_keys = set(old.keys())
    default_and_additional_keys = old_keys.symmetric_difference(new.keys())
    keys_to_update = old_keys.intersection(new.keys())
    for k in default_and_additional_keys:
        try:
            updated[k] = old[k]
        except KeyError:
            logger.error("{} must be an addition".format(k))
            updated[k] = new[k]
    for k in keys_to_update:
        v = new[k]
        if isinstance(v, dict):
            updated[k] = _update_nested_dict(old[k], v)
        else:
            updated[k] = v
    return updated
