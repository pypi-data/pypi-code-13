from builtins import object


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
        if not result and hasattr(data, '__getitem__'):
            result = data.get(self.value, None)
        return result


class DisjunctionTag(object):

    def __init__(self, elements):
        self.elements = elements

    def execute(self, data):
        if not data:
            return None
        for element in self.elements:
            result = data
            for tag in element:
                result = tag.execute(result)
            if result:
                return result
        return None
