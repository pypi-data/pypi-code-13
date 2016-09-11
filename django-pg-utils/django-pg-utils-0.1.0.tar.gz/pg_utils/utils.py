'''
The utils module has custom query expressions for Django, built on
PostgreSQL functions. These can be used as a part of update, create,
filter, order by, annotation, or aggregate.
'''

from django.db.models import Func, Sum
from django.db.models import ExpressionWrapper
from django.db.models import FloatField


class Date(Func):
    '''
    Custom query expression to get date from datetime object.

    Example usage
    queryset.annotate(
        created_at=Date('created_at')
    )
    '''
    function = 'DATE'


def DateTZ(expression, timezone):
    '''
    Custom query expression to get date from datetime object with
    time zone offset.

    Example usage
    queryset.annotate(
        created_date=DateTZ('created_at', '+05:30')
    )
    '''
    class DateWithTZ(Date):
        template = '%(function)s(%(expressions)s AT TIME ZONE '\
                   'INTERVAL \'{timezone}\')'.format(timezone=timezone)

    return DateWithTZ(expression)


class Seconds(Func):
    '''
    Custom query expression to convert time interval to seconds.

    Example usage
    queryset.annotate(
        duration=Seconds(F('end_time') - F('start_time'))
    )
    '''
    function = 'EXTRACT'
    template = '%(function)s(EPOCH FROM %(expressions)s)'


class DistinctSum(Sum):
    '''
    Custom query expression to take a distinct sum.

    Example usage
    queryset.annotate(
        total_tasks=DistinctSum('drivers__tasks')
    )
    '''
    function = 'SUM'
    template = '%(function)s(DISTINCT %(expressions)s)'


class NullIf(Func):
    '''
    Helper query expression for divide, to check if denominator is 0, and
    if so, then return null.
    '''
    function = 'NULLIF'
    template = '%(function)s(%(expressions)s,0)'


class Float(Func):
    '''
    Custom query expression to cast integer field to float. Used as a
    helper method for division of integer fields.
    '''
    function = 'CAST'
    template = '%(function)s(%(expressions)s AS FLOAT)'


def divide(numerator, denominator):
    '''
    Custom query expression to divide numerator by denominator.

    Example usage
    queryset.annotate(
        speed=divide(F('distance'), F('time'))
    )
    '''
    return ExpressionWrapper(Float(numerator) /
                             NullIf(denominator),
                             output_field=FloatField())
