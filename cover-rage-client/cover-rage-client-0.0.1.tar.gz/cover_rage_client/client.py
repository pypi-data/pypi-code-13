#!/usr/bin/env python

import sys

from cover_rage_client import main


if __name__ == "__main__":  # pragma: no cover

    if len(sys.argv) != 5:
        print('Usage: {} <cover_rage_server_url> <cover_rage_app_token> </path/to/git/root> </path/to/coverage.xml>'.format(sys.argv[0]))
        exit(1)

        main(*sys.argv[1:5])
