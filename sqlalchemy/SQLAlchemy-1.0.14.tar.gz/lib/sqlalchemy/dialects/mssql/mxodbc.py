# mssql/mxodbc.py
# Copyright (C) 2005-2016 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""
.. dialect:: mssql+mxodbc
    :name: mxODBC
    :dbapi: mxodbc
    :connectstring: mssql+mxodbc://<username>:<password>@<dsnname>
    :url: http://www.egenix.com/

Execution Modes
---------------

mxODBC features two styles of statement execution, using the
``cursor.execute()`` and ``cursor.executedirect()`` methods (the second being
an extension to the DBAPI specification). The former makes use of a particular
API call specific to the SQL Server Native Client ODBC driver known
SQLDescribeParam, while the latter does not.

mxODBC apparently only makes repeated use of a single prepared statement
when SQLDescribeParam is used. The advantage to prepared statement reuse is
one of performance. The disadvantage is that SQLDescribeParam has a limited
set of scenarios in which bind parameters are understood, including that they
cannot be placed within the argument lists of function calls, anywhere outside
the FROM, or even within subqueries within the FROM clause - making the usage
of bind parameters within SELECT statements impossible for all but the most
simplistic statements.

For this reason, the mxODBC dialect uses the "native" mode by default only for
INSERT, UPDATE, and DELETE statements, and uses the escaped string mode for
all other statements.

This behavior can be controlled via
:meth:`~sqlalchemy.sql.expression.Executable.execution_options` using the
``native_odbc_execute`` flag with a value of ``True`` or ``False``, where a
value of ``True`` will unconditionally use native bind parameters and a value
of ``False`` will unconditionally use string-escaped parameters.

"""


from ... import types as sqltypes
from ...connectors.mxodbc import MxODBCConnector
from .pyodbc import MSExecutionContext_pyodbc, _MSNumeric_pyodbc
from .base import (MSDialect,
                   MSSQLStrictCompiler,
                   _MSDateTime, _MSDate, _MSTime)


class _MSNumeric_mxodbc(_MSNumeric_pyodbc):
    """Include pyodbc's numeric processor.
    """


class _MSDate_mxodbc(_MSDate):
    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return "%s-%s-%s" % (value.year, value.month, value.day)
            else:
                return None
        return process


class _MSTime_mxodbc(_MSTime):
    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return "%s:%s:%s" % (value.hour, value.minute, value.second)
            else:
                return None
        return process


class MSExecutionContext_mxodbc(MSExecutionContext_pyodbc):
    """
    The pyodbc execution context is useful for enabling
    SELECT SCOPE_IDENTITY in cases where OUTPUT clause
    does not work (tables with insert triggers).
    """
    # todo - investigate whether the pyodbc execution context
    #       is really only being used in cases where OUTPUT
    #       won't work.


class MSDialect_mxodbc(MxODBCConnector, MSDialect):

    # this is only needed if "native ODBC" mode is used,
    # which is now disabled by default.
    # statement_compiler = MSSQLStrictCompiler

    execution_ctx_cls = MSExecutionContext_mxodbc

    # flag used by _MSNumeric_mxodbc
    _need_decimal_fix = True

    colspecs = {
        sqltypes.Numeric: _MSNumeric_mxodbc,
        sqltypes.DateTime: _MSDateTime,
        sqltypes.Date: _MSDate_mxodbc,
        sqltypes.Time: _MSTime_mxodbc,
    }

    def __init__(self, description_encoding=None, **params):
        super(MSDialect_mxodbc, self).__init__(**params)
        self.description_encoding = description_encoding

dialect = MSDialect_mxodbc
