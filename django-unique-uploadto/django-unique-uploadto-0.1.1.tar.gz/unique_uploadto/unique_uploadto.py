from __future__ import absolute_import, print_function, unicode_literals

import os
from datetime import datetime
from uuid import uuid4

from django.utils.deconstruct import deconstructible


@deconstructible
class UniqueFileName(object):
    """Provide a path, a random datestamped filename will be returned."""
    def __init__(self, path, default_extension='', *args, **kwargs):
        """Store the arguments."""
        super(UniqueFileName, self).__init__(*args, **kwargs)
        self.path = path
        self.default_extension = default_extension

    def __call__(self, instance, filename):  # pylint: disable=unused-argument
        """Generate the name of the file."""
        if '.' in filename:
            extension = filename.split('.')[-1]
        else:
            extension = self.default_extension
        timestamp = datetime.utcnow().isoformat() + 'Z'
        filename = '{0}_{1}.{2}'.format(timestamp, uuid4().hex, extension)
        return os.path.join(self.path, filename)
