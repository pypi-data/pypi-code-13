'''
Condition group where conditions are set
more than one conditions can be added at a time
'''


class ConditionGroup():
    def __init__(self):
        self.conditions = []
        self.success = 'success'
        self.failed = 'failed'

    def add_condition(self, l1, optn, arg, then, else_value):
        input_json = {'l1': l1, 'optn': optn, 'arg': arg, 'then': then, 'else_value': else_value}
        self.conditions.append(input_json)

    @property
    def conditions(self):
        return self.conditions

    def response(self, success, failed):
        self.success = success
        self.failed = failed


class NameError:
    
    def __init__():
        self.data.fetch = None
