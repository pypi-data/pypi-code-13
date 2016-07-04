#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from sql import Query, Expression

from ...config import CONFIG
from .field import Field, FieldTranslate, size_validate, SQLType


def autocomplete_validate(value):
    if value:
        assert isinstance(value, list), 'autocomplete must be a list'


class Char(FieldTranslate):
    '''
    Define a char field (``unicode``).
    '''
    _type = 'char'

    def __init__(self, string='', size=None, help='', required=False,
            readonly=False, domain=None, states=None, translate=False,
            select=False, on_change=None, on_change_with=None, depends=None,
            context=None, loading=None, autocomplete=None):
        '''
        :param translate: A boolean. If ``True`` the field is translatable.
        :param size: A integer. If set defines the maximum size of the values.
        '''
        if loading is None:
            loading = 'lazy' if translate else 'eager'
        super(Char, self).__init__(string=string, help=help, required=required,
            readonly=readonly, domain=domain, states=states, select=select,
            on_change=on_change, on_change_with=on_change_with,
            depends=depends, context=context, loading=loading)
        self.__autocomplete = None
        self.autocomplete = autocomplete if autocomplete else None
        self.translate = translate
        self.__size = None
        self.size = size
    __init__.__doc__ += Field.__init__.__doc__

    def _get_autocomplete(self):
        return self.__autocomplete

    def _set_autocomplete(self, value):
        autocomplete_validate(value)
        self.__autocomplete = value

    autocomplete = property(_get_autocomplete, _set_autocomplete)

    def _get_size(self):
        return self.__size

    def _set_size(self, value):
        size_validate(value)
        self.__size = value

    size = property(_get_size, _set_size)

    @staticmethod
    def sql_format(value):
        if isinstance(value, (Query, Expression)):
            return value
        if value is None:
            return None
        elif isinstance(value, str):
            return unicode(value, 'utf-8')
        assert isinstance(value, unicode)
        return value

    def sql_type(self):
        db_type = CONFIG['db_type']
        if self.size and db_type != 'sqlite':
            return SQLType('VARCHAR', 'VARCHAR(%s)' % self.size)
        elif db_type == 'mysql':
            return SQLType('CHAR', 'VARCHAR(255)')
        return SQLType('VARCHAR', 'VARCHAR')
