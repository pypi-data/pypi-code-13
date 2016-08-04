from .interpreter import Interpreter
from .reporter import Reporter

class ObjectFactory:

    factories = {}

    def addFactory(id, factory):

        ObjectFactory.factories[id] = factory
    addFactory = staticmethod(addFactory)

    def createObject(id):

        if not ObjectFactory.factories.has_key(id):
            ObjectFactory.factories[id] = \
              eval(id + '.Factory()')
        return ObjectFactory.factories[id].create()
    createObject = staticmethod(createObject)
