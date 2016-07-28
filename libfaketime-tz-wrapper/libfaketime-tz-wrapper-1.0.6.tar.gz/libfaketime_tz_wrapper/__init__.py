from __future__ import print_function

import dateutil.parser
import libfaketime
import threading
import uuid

from datetime import datetime
from django.utils import timezone


class fake_time(libfaketime.fake_time):
    def __init__(self, datetime_spec, *args, **kwargs):
        datetime_spec = self._prepare(datetime_spec)
        super(fake_time, self).__init__(datetime_spec=datetime_spec, *args, **kwargs)

    def _should_fake(self):
        # Changed to `not ... or ...` instead of `... and ...` + generalized main thread detection
        return not self.only_main_thread or isinstance(threading.current_thread(), threading._MainThread)

    def _should_patch_uuid(self):
        # Changed order of `_should_fake()` and `not self._prev_spec` compared to the super method
        return hasattr(uuid, '_uuid_generate_time') and \
                self._should_fake() and \
                not self._prev_spec


    def _prepare(self, spec):
        dt = spec if isinstance(spec, datetime) else dateutil.parser.parse(spec)

        if timezone.is_aware(dt):
            return timezone.make_naive(dt)
        else:
            return dt
