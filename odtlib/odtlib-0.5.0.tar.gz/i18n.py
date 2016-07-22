"""utility to create/update .po and also compile .po to .mo files
i18n <update|compile>
"""
import os
from os.path import dirname, abspath, normpath, join, isdir, exists
import shutil
from tempfile import mkdtemp

from logilab.common import STD_BLACKLIST
from logilab.common.fileutils import ensure_fs_mode
from logilab.common.shellutils import find, rm

HERE = normpath(dirname(__file__))
I18NPOPATH = join(HERE, 'i18n')

LANGS = ('en', 'fr')

def execute(cmd):
    """display the command, execute it and raise an Exception if returned
    status != 0
    """
    from subprocess import call
    print cmd.replace(os.getcwd() + os.sep, '')
    status = call(cmd, shell=True)
    if status != 0:
        raise Exception('status = %s' % status)

def update():
    toedit = []
    here = HERE
    if not isdir(here):
        raise Exception('unknown path %s' % repr(here))
    print '*' * 72
    print 'updating odtlib ...'
    os.chdir(here)
    print '******** merging main pot file with existing translations'
    odtfiles = find('.', '.py', blacklist=STD_BLACKLIST+('test',))
    tempdir = mkdtemp()
    potfile = join(tempdir, 'odtlib.pot')
    print os.getcwd()
    assert exists(tempdir)
    execute('xgettext --no-location --omit-header -k_ -o %s %s' %  (potfile , ' '.join(odtfiles)))
    print '******** merging pot file with existing translations'
    os.chdir('i18n')
    toedit = []
    for lang in LANGS:
        print '****', lang
        langpo = '%s.po' % lang
        if not exists(langpo):
            shutil.copy(potfile, langpo)
        else:
            execute('msgmerge -N -s %s %s > %snew' % (langpo, potfile, langpo))
            ensure_fs_mode(langpo)
            shutil.move('%snew' % langpo, langpo)
        toedit.append(abspath(langpo))
    # cleanup
    rm(tempdir)
    print '*' * 72
    print 'you can now edit the following files:'
    print '* ' + '\n* '.join(toedit)

def compile(srcdir, destdir):
    """generate .mo files for a set of languages into the `destdir` i18n directory"""
    print 'compiling %s catalog from %s...' % (destdir, srcdir)
    errors = []
    for lang in LANGS:
        langdir = join(destdir, lang, 'LC_MESSAGES')
        if not exists(langdir):
            from cubicweb.toolsutils import create_dir
            create_dir(langdir)
        pofile = join(srcdir, '%s.po' % lang)
        try:
            applmo = join(langdir, 'odtlib.mo')
            try:
                ensure_fs_mode(applmo)
            except OSError:
                pass # suppose not exists
            execute('msgfmt %s -o %s' % (pofile, applmo))
        except Exception, ex:
            errors.append('while handling language %s: %s' % (lang, ex))
    return errors

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(__doc__)
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("you must give, one (no less, no more) command")
    if 'update' in args:
        update()
    elif 'compile' in args:
        compile(I18NPOPATH, I18NPOPATH)
    else:
        parser.error("wrong command, replay again")
