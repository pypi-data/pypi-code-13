# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import nose

from django.test.runner import DiscoverRunner


class NoseRunner(DiscoverRunner):

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument("--unit", action="store_true", default=False)
        parser.add_argument("--functional", action="store_true", default=False)
        return super(NoseRunner, cls).add_arguments(parser)

    def __init__(self, *args, **kwargs):
        self.unit = kwargs['unit']
        self.functional = kwargs['functional']
        return super(NoseRunner, self).__init__(args, kwargs)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if self.unit:
            test_dirs = self.get_test_dirs("unit")
        elif self.functional:
            test_dirs = self.get_test_dirs("functional")
        nose_args = self.get_nose_args()
        passed = nose.run(argv=nose_args + test_dirs)
        # Convert passed to process exit statuses
        if passed:
            return 0
        else:
            return 1

    def get_test_dirs(self, test_type):
        subdirs = []
        for root, dirs, files in os.walk("."):
            if root.endswith("tests/{}".format(test_type)):
                subdirs.append(root)
        return subdirs

    def get_nose_args(self):
        args = [
            'nosetests', '-s',
            '--verbosity=2',
            '--exe',
            '--logging-clear-handlers',
            '--cover-inclusive',
            '--cover-erase',
        ]
        return args
