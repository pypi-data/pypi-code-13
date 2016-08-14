from builtins import object
from tag_processor.services import execute_tag_chain

__all__ = [
    'DataContainer',
    'FunctionTag',
    'ObjectTag',
    'DisjunctionTag',
    'TernaryTag'
]

class DataContainer(object):

    @staticmethod
    def dateformat(value, date_format):
        if not value:
            return None
        return value.strftime(date_format)

    @staticmethod
    def first(value, params):
        return value[0]

    @staticmethod
    def str(value, *args, **kwargs):
        return str(value)


class FunctionTag(object):

    def __init__(self, value, params):
        self.value = value
        self.params = params

    def execute(self, data):
        if not self.value or not hasattr(self.value, '__call__'):
            return data

        return self.value(data, self.params)


class ObjectTag(object):

    def __init__(self, value):
        self.value = value

    def execute(self, data):
        if not data:
            return None
        result = getattr(data, self.value, None)
        if not result and callable(getattr(data, 'get', None)):
            result = data.get(self.value, None)
        return result


class DisjunctionTag(object):

    def __init__(self, elements):
        self.elements = elements

    def execute(self, data):
        if not data:
            return None
        for element in self.elements:
            result = execute_tag_chain(element, data)
            if result:
                return result
        return None


class TernaryTag(object):

    def __init__(self, condition, if_true, if_false):
        self.if_true = if_true
        self.if_false = if_false
        self.condition = condition

    def execute(self, data):
        if not data:
            return None
        if execute_tag_chain(self.condition, data):
            return execute_tag_chain(self.if_true, data)
        else:
            return execute_tag_chain(self.if_false, data)
