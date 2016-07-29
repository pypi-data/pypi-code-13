# -*- coding:utf-8 -*-

import os

from fabric import api
from .utils import createUwsgiConfig, createSuperVisorConfig


class INSTALL():
    def __init__(self, env):
        self.env = env

    def add_postgres_sources(self):
        """ Add postgres respository in sources.list """
        api.run('aptitude install -y curl')
        api.run('aptitude install -y sudo')
        api.run('echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" > /etc/apt/sources.list.d/pgdg.list')
        api.run('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -')

    def install_packages(self):
        """ Install debian packages, PACKAGES is a list of packages. """
        api.run('aptitude update')
        api.run('aptitude upgrade -y')
        api.run('aptitude install -y ' + ' '.join(self.env.PACKAGES))

    def add_user(self):
        """ Create user, create directories """
        api.run('id -u %s &>/dev/null || useradd --home-dir %s -m --shell /bin/bash %s' % (self.env.USER, self.env.HOME, self.env.USER))
        api.run('echo "%s:%s" | chpasswd' % (self.env.USER, self.env.PASSWD))
        with api.cd(self.env.HOME):
            api.sudo('ls www &> /dev/null || mkdir www', user=self.env.USER)
            api.sudo('ls logs &> /dev/null || mkdir logs', user=self.env.USER)
            api.sudo('ls pids &> /dev/null || mkdir pids', user=self.env.USER)
            api.sudo('touch www/restart.txt', user=self.env.USER)

    def database_config(self):
        """ Database configuration """
        with api.settings(warn_only=True):
            api.sudo('psql -c "CREATE USER %s WITH PASSWORD \'%s\'"' % (self.env.DB_USER, self.env.DB_PASS), user='postgres')
            api.sudo('createdb -O %s %s' % (self.env.DB_USER, self.env.DB_NAME), user='postgres')

    def nginx_config(self, PATH):
        """ Nginx load site_configuration """
        HOST_PATH = '/etc/nginx/sites-available/%s.conf' % (self.env.USER)
        ALIAS_PATH = '/etc/nginx/sites-enabled/%s.conf' % (self.env.USER)
        api.put(PATH, HOST_PATH)
        api.run('ls %s > /dev/null || ln -s %s %s' % (ALIAS_PATH, HOST_PATH, ALIAS_PATH))

    def clone_project(self, COMMAND):
        """
        Clone project, example:
            _clone_project(self, 'hg clone http://login@bitbucket.org/testproj testproj')
        WARNING: testproj need to be equal env.USER
        """
        with api.cd(self.env.HOME):
            api.run('ls %s &> /dev/null || %s' % (self.env.USER, COMMAND))

    def install_django(self):
        """
        Install requirements in virtualenv (name=env in root of user).
        Migrate database.
        Collect static files
        """
        with api.cd(self.env.HOME):
            api.sudo('ls env &> /dev/null || virtualenv env', self.env.USER)

        with api.cd(self.env.PROJECT):
            with api.prefix(self.env.VENV):
                api.sudo('pip install -r requirements.txt', user=self.env.USER)
                api.sudo('python manage.py migrate', user=self.env.USER)
                api.sudo('python manage.py collectstatic', user=self.env.USER)

    def uwsgi_django(self, PATH):
        """ Setup uwsgi settings """
        api.put(PATH, os.path.join(self.env.HOME, 'www/uwsgi_params'))
        uwsgi = createUwsgiConfig(self.env)
        uwsgi.django_uwsgi()
        uwsgi.save()

        api.put(uwsgi.path, os.path.join(self.env.HOME, 'www/%s.ini' % self.env.USER))

        with api.cd(self.env.HOME):
            api.sudo('ls env &> /dev/null || virtualenv env', self.env.USER)

        with api.prefix(self.env.VENV):
            api.sudo('pip install uwsgi', self.env.USER)

    def supervisor_django(self, PATH):
        """ Setup supervisor settings for uwsgi. Run after uwsgi """
        api.put(PATH, '/etc/supervisor/supervisord.conf')
        supervisor = createSuperVisorConfig(self.env)
        supervisor.django_uwsgi()
        supervisor.save()
        api.put(supervisor.path, os.path.join(self.env.HOME, 'supervisor.conf'), self.env.USER)
        api.run('supervisorctl update', shell=False)
        api.run('supervisorctl restart %s:' % self.env.USER, shell=False)

    def chown(self):
        """ Set permissions """
        api.run('chown -R %s:%s %s' % (self.env.USER, self.env.USER, self.env.HOME))
