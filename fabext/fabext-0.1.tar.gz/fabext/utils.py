# -*- coding:utf-8 -*-

import os
import ConfigParser


##############
# SUPERVISOR #
##############


class createSuperVisorConfig():
    path = '/tmp/supervisor.conf'

    def __init__(self, env):
        self.env = env
        self.programs = []
        self.config = ConfigParser.RawConfigParser()

    def django_uwsgi(self):
        """ Create uwsgi section """
        name = "%s-uwsgi" % self.env.USER
        self.programs.append(name)
        section = 'program:' + name
        self.config.add_section(section)
        self.config.set(section, 'directory', os.path.join(self.env.HOME, 'www'))
        self.config.set(section, 'command', os.path.join(self.env.HOME, 'env/bin/uwsgi --ini=%s.ini' % self.env.USER))
        self.config.set(section, 'stdout_logfile', os.path.join(self.env.HOME, 'logs/uwsgi.log'))
        self.config.set(section, 'stderr_logfile', os.path.join(self.env.HOME, 'logs/uwsgi_err.log'))
        self.config.set(section, 'autostart', 'true')
        self.config.set(section, 'autorestart', 'true')
        self.config.set(section, 'user', self.env.USER)
        self.config.set(section, 'redirect_stderr', 'true')
        self.config.set(section, 'stopwaitsecs', '60')
        self.config.set(section, 'stopsignal', 'INT')

    def save(self):
        """ Create group section and save config. """
        section = 'group:%s' % self.env.USER
        self.config.add_section(section)
        self.config.set(section, 'programs', ','.join(self.programs))

        with open(self.path, 'w') as fn:
            self.config.write(fn)


#########
# UWSGI #
#########


class createUwsgiConfig():
    path = '/tmp/uwsgi.conf'

    def __init__(self, env):
        self.env = env
        self.programs = []
        self.config = ConfigParser.RawConfigParser()

    def django_uwsgi(self):
        name = "%s-uwsgi" % self.env.USER
        self.programs.append(name)
        section = 'uwsgi'
        self.config.add_section(section)
        self.config.set(section, 'chdir', self.env.PROJECT)
        self.config.set(section, 'home', os.path.join(self.env.HOME, 'env'))
        self.config.set(section, 'module', '%s.wsgi:application' % self.env.USER)
        self.config.set(section, 'master', 'True')
        self.config.set(section, 'vacuum', 'True')
        self.config.set(section, 'max-requests', '5000')
        self.config.set(section, 'socket', os.path.join(self.env.HOME, 'www/%s.sock' % self.env.USER))
        self.config.set(section, 'processes', self.env.uwsgi_processes)
        self.config.set(section, 'workers', self.env.uwsgi_workers)
        self.config.set(section, 'touch-reload', os.path.join(self.env.HOME, 'www/restart.txt'))
        self.config.set(section, 'pidfile', os.path.join(self.env.HOME, 'pids/uwsgi.pid'))
        self.config.set(section, 'chmod-socket', '666')
        self.config.set(section, 'pp', self.env.HOME)

    def save(self):
        """ Create file """
        with open(self.path, 'w') as fn:
            self.config.write(fn)
