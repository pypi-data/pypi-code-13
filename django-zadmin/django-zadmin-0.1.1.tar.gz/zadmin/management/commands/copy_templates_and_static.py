from __future__ import unicode_literals
import os
import shutil
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.utils.encoding import smart_text
from django.utils.functional import cached_property
from django.utils.six.moves import input


class Command(BaseCommand):
    """
    Command that allows to copy template files to settings.TEMPLATES and static files to settings.STATIC_ROOT
    for covering template files and static files in Django's admin app.
    """
    help = "Copy zadmin's template files and static files."
    requires_system_checks = False

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.static_root = None
        self.templates = None

    def check(self):
        if not settings.STATIC_ROOT:
            raise CommandError('"STATIC_ROOT" must be setted in settings.py to place admin\'s static files')
        self.static_root = settings.STATIC_ROOT

        template_dirs = []
        for template in settings.TEMPLATES:
            if template['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
                template_dirs.extend(template.get('DIRS'))
        if not template_dirs:
            raise CommandError('"DIRS" in TEMPLATES must be setted in settings.py to place admin\'s template files')
        self.templates = template_dirs[0]

    def handle(self, *args, **options):
        self.check()
        zadmin_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        print 'zadmin_dir', zadmin_dir
        static_dir = os.path.join(zadmin_dir, 'static')
        print 'static_dir', static_dir
        templates_dir = os.path.join(zadmin_dir, 'templates')
        print 'templates_dir', templates_dir

        shutil.copytree(static_dir, self.static_root)
        shutil.copytree(templates_dir, self.templates)
