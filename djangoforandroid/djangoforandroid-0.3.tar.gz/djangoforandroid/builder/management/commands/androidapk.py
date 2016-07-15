from django.core.management.base import BaseCommand, CommandError
import os
import shutil

from ._tools import get_p4a_args, update_apk, parcefiles, overwrite_p4a

class Command(BaseCommand):
    help = 'Generate .apk for debug'
    can_import_settings = True

    #----------------------------------------------------------------------
    def add_arguments(self, parser):
        """"""

        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=True,
            help='Debug apk with',
        )

        parser.add_argument(
            '--release',
            action='store_true',
            dest='release',
            default=False,
            help='Release unsigned apk',
        )

        parser.add_argument(
            '--install',
            action='store_true',
            dest='install',
            default=False,
            help='Install apk with adb.',
        )

        parser.add_argument(
            '--run',
            action='store_true',
            dest='run',
            default=False,
            help='Run apk with adb.',
        )

        parser.add_argument(
            '--logcat',
            action='store_true',
            dest='logcat',
            default=False,
            help='Log apk with adb.',
        )



    #----------------------------------------------------------------------
    def handle(self, *args, **options):
        """"""
        from django.conf import settings

        update_apk(settings)
        overwrite_p4a(settings)


        NAME = os.path.split(settings.BASE_DIR)[-1]
        build_dir = os.path.join(settings.ANDROID['BUILD']['build'], NAME)
        name = settings.ANDROID['APK']['name']
        version = settings.ANDROID['APK']['version']
        apk_debug = os.path.join(build_dir, '{}-{}-debug.apk'.format(name, version)).replace(' ', '')
        apk_release = os.path.join(build_dir, '{}-{}-release.apk'.format(name, version)).replace(' ', '')
        package = settings.ANDROID['APK']['package']


        #move project
        project_dir = settings.BASE_DIR
        app_dir = os.path.join(settings.ANDROID['BUILD']['build'], NAME, 'app')
        project_build = os.path.join(app_dir, os.path.split(settings.BASE_DIR)[-1])
        if os.path.exists(project_build):
            shutil.rmtree(project_build)
        shutil.copytree(project_dir, project_build)
        os.chdir(os.path.join(app_dir, NAME))
        os.system('python manage.py collectstatic --noinput')

        if os.path.exists(apk_debug):
            os.remove(apk_debug)

        if os.path.exists(apk_release):
            os.remove(apk_release)

        #for apk in filter(lambda f:f.endswith(".apk"), os.listdir(settings.BASE_DIR)):
            #os.remove(os.path.join(settings.BASE_DIR, apk))

        os.chdir(build_dir)

        if options['release']:
            os.environ['P4A_RELEASE_KEYSTORE'] = settings.ANDROID['KEY']['RELEASE_KEYSTORE']
            os.environ['P4A_RELEASE_KEYALIAS'] = settings.ANDROID['KEY']['RELEASE_KEYALIAS']
            os.environ['P4A_RELEASE_KEYSTORE_PASSWD'] = settings.ANDROID['KEY']['RELEASE_KEYSTORE_PASSWD']
            os.environ['P4A_RELEASE_KEYALIAS_PASSWD'] = settings.ANDROID['KEY']['RELEASE_KEYALIAS_PASSWD']
            os.system('p4a apk --release')
            shutil.copy(apk_release, settings.BASE_DIR)


        elif options['debug']:
            os.system('p4a apk')
            shutil.copy(apk_debug, settings.BASE_DIR)


            if options['install']:
                os.system("adb start-server")
                os.system("adb install -r {}".format(apk_debug))

                if options['run']:
                    os.system("adb shell monkey -p {PACKAGE} -c android.intent.category.LAUNCHER 1".format(PACKAGE=package))

                if options['logcat']:
                    os.system("adb logcat")

