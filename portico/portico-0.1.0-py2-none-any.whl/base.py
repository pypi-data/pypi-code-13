class Item(object):
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.process(self.event)

    def process(self, event):
        raise NotImplementedError('Base Class does not implement')
