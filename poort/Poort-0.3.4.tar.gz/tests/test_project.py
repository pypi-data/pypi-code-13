# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from os import path
from os import stat
from os import walk
from pandora import absfilename
from stat import S_IXUSR


class TestWebsite(object):
    def test_files_have_correct_header(self):
        filenames = list()

        for root, dirnames, basenames in walk(absfilename('.')):
            if 'src' not in root or 'tests' not in root:
                continue

            for basename in basenames:
                if basename.endswith('.py'):
                    filenames.append(path.join(root, basename))

        filenames.sort()

        allowed_normal = [
            '# -*- coding: utf-8 -*-',
            'from __future__ import absolute_import, division, print_function',
            ''
        ]
        allowed_executable = [
            '#!/usr/bin/env python',
            '# -*- coding: utf-8 -*-',
            'from __future__ import absolute_import, division, print_function',
            ''
        ]

        for filename in filenames:
            with open(filename) as stream:
                lines = [l.rstrip() for l in stream.read().split('\n')][:4]

            if S_IXUSR & stat(filename).st_mode:
                headers = allowed_executable
            else:
                headers = allowed_normal

            msg = '.{:s} does not have the correct header lines.'.format(
                filename[len(absfilename('.')):])
            msg += '\nFOUND:\n'
            msg += '\n'.join(lines)
            msg += '\nEXPECTED:\n'
            msg += '\n'.join(headers)

            assert len(lines) >= len(headers), msg
            for lx, line in enumerate(headers):
                assert line == lines[lx], msg
