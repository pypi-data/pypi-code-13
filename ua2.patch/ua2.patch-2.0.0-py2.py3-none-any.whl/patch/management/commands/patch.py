"""
Database patch apply managment system

"""
from __future__ import print_function

import getpass
import importlib
import os
import random
import re
import stat
import sys
from datetime import datetime
from functools import reduce
from optparse import make_option

from django.conf import settings
from django.core.management.base import LabelCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections, transaction

from ua2.patch.models import PatchLog


patch_re = re.compile("(\d{1,5})(\d*)(\-(\w+)\-(\d+))?\.([\w\d]+)$")

db_name_re = re.compile("^\-\-\ ?database\:\ ?(\w+)")


def atoi(value, default=None):
    try:
        rc = int(value)
    except (ValueError, TypeError):
        rc = default
    return rc


def _patch_root_dir():
    patch_dir = getattr(settings, 'DB_PATCH_ROOT',
                        os.path.join(settings.BASE_DIR, 'patches/'))
    if not os.path.exists(patch_dir):
        os.mkdir(patch_dir)
    return patch_dir


class PatchFile(object):
    ALLOWED_EXT = ['sh', 'py', 'sql', 'php', 'json']

    def __init__(self, filename=None):
        self.filename = filename

    def __str__(self):
        return "<Patch %d %s>" % (self.index or 0, self.filename)

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return str(self)

    def __cmp__(self, other):
        return cmp(self.prefix, other.prefix)

    def open(self, mode="r"):
        return open(self.fullname, mode)

    @property
    def fullname(self):
        return os.path.join(_patch_root_dir(), self.filename)

    @property
    def basename(self):
        return os.path.basename(self.filename)

    @property
    def size(self):
        return os.stat(self.fullname)[stat.ST_SIZE]

    def touch(self):
        fd = self.open("w")
        fd.close()

    def copy_stdin(self):
        fd = self.open("w")
        if not sys.stdin.isatty():
            for byte in sys.stdin.read():
                fd.write(byte)
        fd.close()

    @property
    def num(self):
        m = patch_re.search(self.filename)
        if not m:
            return None

        prefix = m.group(1)
        prefix2 = m.group(2) or ''
        suffix = m.group(5) or ''
        return int(prefix + prefix2 + suffix)

    @property
    def extension(self):
        return os.path.splitext(self.basename)[1][1:]

    @property
    def prefix(self):
        m = patch_re.search(self.filename)
        if not m:
            return None
        return int(m.group(1))

    @staticmethod
    def gen_user(**options):
        return options.get('user') or getpass.getuser()

    @staticmethod
    def gen_suffix():
        random.seed()
        return "%03d" % (random.randrange(0, 999))

    @classmethod
    def create_by_number(cls, number, **options):
        patch = cls("%05d-%s-%s.%s" % (number,
                                       cls.gen_user(**options),
                                       cls.gen_suffix(),
                                       options.get('ext', 'sql')))
        return patch

    def is_exist(self):
        return os.path.isfile(self.fullname)

    def is_reserved(self):
        return self.size == 0

    def is_applied(self):
        return PatchLog.objects.filter(patch=self.basename).count() > 0

    def is_valid(self):
        m = patch_re.search(self.filename)
        if not m:
            return False
        return m.group(6) in self.ALLOWED_EXT

    def set_applied(self):
        patch_log = PatchLog()
        patch_log.patch = self.basename
        patch_log.save()

    def remove_applied(self):
        PatchLog.objects.filter(patch=self.basename).delete()

    def get_database_name(self):
        """
        It read first line of SQL patch and parse it with following format:
        -- database: <name>

        It can be used to specify database where apply patch.
        default database name is "default"
        """
        fd = self.open()
        first_line = fd.readline()
        fd.close()

        m = db_name_re.search(first_line)
        if not m:
            return DEFAULT_DB_ALIAS
        return m.group(1)


class Command(LabelCommand):
    help = ("incremental database updater")
    args = '\n\tinstall'
    args += '\n\tup'
    args += '\n\trevert <file>'
    args += '\n\tskip <file>'
    args += '\n\tnext [-e <ext>]'
    args += '\n\tlist'
    commands = ('up', 'skip', 'revert', 'list', 'next', 'migrate', 'install')

    requires_model_validation = False
    option_list = LabelCommand.option_list + (
        make_option('-f', '--force',  action='store_true', dest='force',
                    default=False, help='force selected action'),
        make_option('-e', '--ext',
                    action="store",
                    type="string",
                    default='sql', help='default extenstion'),
        make_option('-u', '--user',
                    action="store",
                    type="string",
                    help='overwrite username'),
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self._backends = {}

    def get_file_list(self):
        return os.listdir(_patch_root_dir())

    def patches(self):
        return filter(lambda patch: patch.is_valid(),
                      map(lambda fname: PatchFile(fname),
                          self.get_file_list()))

    def sorted_patches(self):
        return sorted(self.patches(),
                      key=lambda patch: patch.num)

    def iter_patch_list(self, args):
        for patch_name in args:
            yield PatchFile(patch_name)

    def iter_all_patches(self):
        for patch in filter(lambda patch: not patch.is_applied(),
                            self.sorted_patches()):
            yield patch

    def get_backend(self, ext):
        if ext not in self._backends:
            backend_module = importlib.import_module(
                'ua2.patch.backends.%s' % ext
            )
            self._backends[ext] = backend_module.Backend()
        return self._backends[ext]

    @property
    def last_patch_num(self):
        return reduce(lambda x, y: max(x, y.prefix),
                      self.patches(), 0)

    def handle(self, *args, **options):
        if not len(args) or args[0] not in self.commands:
            raise CommandError(
                'Enter one of valid commands %s' % ", ".join(self.commands))
        command = args[0]

        if hasattr(self, 'handle_%s' % command):
            cb = getattr(self, 'handle_%s' % command)
            return cb(*args[1:], **options)

        raise CommandError('Command %s not implemented' % command)

    def handle_skip(self, *args, **options):
        print("Skip patches:")

        for name in args:
            patch = PatchFile(name)
            if not patch.is_valid():
                print("[ERROR]\t%s - invalid patch name" % name)
                continue

            if not patch.is_exist():
                print("[ERROR]\t%s - does not found" % name)
                continue

            if patch.is_applied():
                print("[INFO]\t%s - already allpied" % name)
                continue

            patch.set_applied()
            print("[OK]\t%s" % name)

        print("\t Done.")

    def handle_revert(self, *args, **options):
        print("Revert patches:")

        for name in args:
            patch = PatchFile(name)
            if not patch.is_valid():
                print("[ERROR]\t%s - invalid patch name" % name)
                continue

            if not patch.is_exist():
                print("[ERROR]\t%s - does not found" % name)
                continue

            if not patch.is_applied():
                print("[ERROR]\t%s - not is allpied" % name)
                continue

            patch.remove_applied()
            print("[OK]\t%s" % name)

        print("\t Done.")

    def handle_list(self, *args, **options):
        print("List of patches for apply:")
        todo = [patch
                for patch in self.sorted_patches()
                if not patch.is_applied()]

        if not len(todo):
            print("Nothing to apply")
        else:
            for patch in todo:
                if patch.is_reserved():
                    print('* Reserved patch for future use: %s' % (
                        patch.basename))
                    continue
                print("%d\t%s" % (patch.num, patch.basename))

        print("\t Done.")

    def handle_next(self, *args, **options):
        if len(args) > 0:
            patch_num = atoi(args[0])
        else:
            patch_num = self.last_patch_num + 1

        patch = PatchFile.create_by_number(patch_num, **options)
        if patch in self.patches():
            print("Warning: %s found in list of patches, skipped." % (
                patch.basename))
            return

        patch.copy_stdin()

        print("File %s has been created" % patch.fullname)
        print("\tsize: %d" % patch.size)

    @transaction.atomic
    def handle_migrate(self, *args, **options):
        print("Migrate")
        transaction.set_dirty()
        curs = connections['default'].cursor()
        curs.execute("""insert into patch_log (patch, added)
                        select patch, stamp from db_patch_log""")

    def handle_up(self, *args, **options):
        start = datetime.now()
        print("Update")
        print("+++start %s\n" % datetime.now())

        if len(args):
            patch_iterator = self.iter_patch_list(args)
        else:
            patch_iterator = self.iter_all_patches()

        for patch in patch_iterator:
            if not patch.is_valid():
                print("[ERROR]\t%s - invalid patch name" % patch.filename)
                continue

            if not patch.is_exist():
                print("[ERROR]\t%s - does not found" % patch.filename)
                continue

            if patch.is_applied():
                print("[INFO]\t%s - already allpied" % patch.filename)
                continue

            print("\n")
            print("=" * 80)
            print("= Run patch %d (%s)" % (patch.num, patch.basename))
            print("=" * 80)

            backend = self.get_backend(patch.extension)
            if not backend.run(patch):
                break

            patch.set_applied()
            print("[OK]\t%s\n\n" % patch.basename)

        end = datetime.now()
        print("\n+++stop: %s" % end)
        print("\telapsed time: %s" % (end - start))
