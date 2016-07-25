import imp

from ua2.patch.backends.base import BaseBackend
from django.db import transaction


class Backend(BaseBackend):

    def run(self, patch):
        print("* ...run Python ")
        module = imp.load_source('main', patch.fullname)
        with transaction.atomic():
            return module.main()
