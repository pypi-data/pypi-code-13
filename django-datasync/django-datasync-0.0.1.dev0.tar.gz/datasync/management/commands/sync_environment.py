import os
import tempfile
from datetime import datetime
from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
    
    make_option('-k', '--with-key',
        action='store_true',
        dest='with_key',
        default=False,
        help='Execute using ssh key instead of ssh password'),
        
    make_option('-d', '--debug',
        action='store_true',
        dest='debug',
        default=False,
        help='Show configuration without executing')
    )
    
    def sync_database(self):
        self.stdout.write(u"Syncing database")
        REMOTE_DB = settings.DATASYNC['DATABASE']
        LOCAL_DB = settings.DATABASES['default']

        with tempfile.NamedTemporaryFile('wb') as f:
            cmd = (
                u"PGPASSWORD='{0}'"
                u" pg_dump -Fc -h {1} -U {2} -d {3} -p {4} > {5}"
            ).format(
                REMOTE_DB['PASSWORD'], REMOTE_DB['HOST'], REMOTE_DB['USER'],
                REMOTE_DB['NAME'], REMOTE_DB['PORT'], f.name
            )
            self.stdout.write(u"Running: {0}".format(cmd))
            os.system(cmd)

            cmd = (
                u"PGPASSWORD='{0}'"
                u" pg_restore -h {1} -U {2} -p {3} -n public -c -1 -d {4} {5}"
            ).format(
                LOCAL_DB['PASSWORD'], LOCAL_DB['HOST'], LOCAL_DB['USER'],
                LOCAL_DB['PORT'], LOCAL_DB['NAME'], f.name
            )
            self.stdout.write(u"Running: {0}".format(cmd))
            os.system(cmd)

    def sync_media(self, with_key=False):
        self.stdout.write(u"Syncing media files")
        REMOTE_MEDIA = settings.DATASYNC['MEDIA_REMOTE']
        LOCAL_MEDIA = settings.DATASYNC['MEDIA_TARGET']
        
        if with_key:
            
            cmd = (
                u"rsync  -zvr -e 'ssh -p {0}' {1}@{2}:{3} {4}"
            ).format(
                settings.DATASYNC['PORT'], settings.DATASYNC['USER'], 
                settings.DATASYNC['HOST'], REMOTE_MEDIA, LOCAL_MEDIA
            )
            
        else:
            cmd = (
                u"sshpass -p '{0}' rsync  -zvr -e 'ssh -p {1}' {2}@{3}:{4} {5}"
            ).format(
                settings.DATASYNC['PASSWORD'], setting.DATASYNC['PORT'], 
                settings.DATASYNC['USER'], settings.DATASYNC['HOST'], 
                REMOTE_MEDIA, LOCAL_MEDIA
            )
            
        self.stdout.write(u"Running: {0}".format(cmd))
        os.system(cmd)

    def handle(self, *args, **options):
        with_key = options.get('with_key', False)
        debug = options.get('debug', False)
        
        if debug:
            print(u'Showing config and exiting: ')
            print(settings.DATASYNC)
            exit()
        
        self.stdout.write(u"Starting sync: {0}".format(
            str(datetime.now())
        ))
        self.sync_database()
        self.sync_media(with_key=with_key)
        self.stdout.write(u"Stopping sync: {0}".format(
            str(datetime.now())
        ))
