from ua2.patch.backends.base import BaseBackend

from django.core.managment.commands.loaddata import Command


class Backend(BaseBackend):

    def run(self, patch):
        print("* ...run load json ")
