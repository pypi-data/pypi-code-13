#! /usr/bin/env python3
"""It is a part fron bcc2to package
(c)2016 Vidmantas Balčytis <vidma@lema.lt>
"""

import sys

if len(sys.argv) > 1 and sys.argv[1] == 'install':
    from bcc2to.parts import install
    install.main()
elif len(sys.argv) > 1 and sys.argv[1] == 'cleanup':
    from bcc2to.parts import cleanup
    cleanup.main()
else:
    import bcc2to
    bcc2to.main()
