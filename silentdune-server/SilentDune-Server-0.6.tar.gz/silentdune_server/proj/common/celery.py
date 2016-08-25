#
# Authors: Robert Abram <robert.abram@entpack.com>,
#          Brett Donohoo <brett.donohoo@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

# To Start Celery during development make sure Redis is installed
# locally and running.  Open a terminal, then source the virtual environment and change directory
# to the project root directory.  Finally run "celery -A proj worker -l info" to
# to start the celery workers for testing.

# For PyMySQL
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj',
             broker='redis://127.0.0.1:6379/0',
             backend='redis://127.0.0.1:6379/0',
             include=['proj.tasks']
             )

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# JSON serializer limits you to the following data types:
# strings, Unicode, floats, boolean, dictionaries, and lists.
# Decimals and dates are notably missing.

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_IGNORE_RESULT=False,
    CELERY_DISABLE_RATE_LIMITS=True,
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))