##############################################################################
#
# Copyright (c) 2016, 2degrees Limited.
# All Rights Reserved.
#
# This file is part of django-postgres-delete-cascade
# <https://github.com/2degrees/django-postgres-delete-cascade>, which is subject
# to the provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

from django.db.backends.postgresql_psycopg2.base import \
    DatabaseWrapper as PostgresDatabaseWrapper

from django_postgres_delete_cascade.schema import DatabaseSchemaEditor


class DatabaseWrapper(PostgresDatabaseWrapper):
    SchemaEditorClass = DatabaseSchemaEditor
