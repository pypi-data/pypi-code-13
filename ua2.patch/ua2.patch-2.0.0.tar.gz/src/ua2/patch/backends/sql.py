import os
from copy import deepcopy

from django.db import connections

from ua2.patch.backends.base import BaseShellBackend


class Backend(BaseShellBackend):

    def print_args(self, args):
        print("> %s" % ' '.join(args))
        print("-" * 80)

    def run_psql(self, db_connect, patch):
        settings_dict = db_connect.settings_dict

        args = ['psql', '-1', '-a', '-v',
                '-d', settings_dict['NAME'],
                '-f', patch.fullname,
                '--set', 'ON_ERROR_STOP=ON']

        if settings_dict['USER']:
            args += ["-U", settings_dict['USER']]
        if settings_dict['HOST']:
            args.extend(["-h", settings_dict['HOST']])
        if settings_dict['PORT']:
            args.extend(["-p", str(settings_dict['PORT'])])

        env = deepcopy(os.environ)
        if settings_dict['PASSWORD']:
            env['PGPASSWORD'] = settings_dict['PASSWORD']

        self.print_args(args)
        return self.popen(*args, env=env)

    def run_mysql(self, db_connect, patch):
        settings_dict = db_connect.settings_dict
        sql_fd = patch.open()

        args = ['mysql',
                '--line-numbers',
                '-v']

        if settings_dict['USER']:
            args += ["--user=%s" % settings_dict['USER']]
        if settings_dict['PASSWORD']:
            args += ["--password=%s" % settings_dict['PASSWORD']]
        if settings_dict['HOST']:
            if '/' in settings_dict['HOST']:
                args += ["--socket=%s" % settings_dict['HOST']]
            else:
                args += ["--host=%s" % settings_dict['HOST']]
        if settings_dict['PORT']:
            args += ["--port=%s" % settings_dict['PORT']]

        if settings_dict['NAME']:
            args += [settings_dict['NAME']]

        self.print_args(args)
        return self.popen(*args, stdin=sql_fd)

    def run_sqllite3(self, patch):
        args = ['sqlite3',
                self.connection.settings_dict['NAME']]

        sql_fd = patch.open()
        return self.popen(*args, stdin=sql_fd)

    def run(self, patch):
        database_name = patch.get_database_name()
        db_connect = connections[database_name]
        client = db_connect.client.executable_name

        print("* ...run SQL (%s)" % database_name)

        if not hasattr(self, 'run_%s' % client):
            raise NotImplementedError

        handler = getattr(self, 'run_%s' % client)
        return handler(db_connect, patch)
