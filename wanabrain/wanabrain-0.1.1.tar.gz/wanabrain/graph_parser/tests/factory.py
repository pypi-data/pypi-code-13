# -*- coding: utf-8 -*-
from unittest import TestCase
from wanabrain.graph_parser import ObjectFactory, Interpreter

class TestFactory(TestCase):

    def test_factory(self):

        interpreter1 = ObjectFactory.createObject(Interpreter.__name__)
        interpreter2 = ObjectFactory.createObject(Interpreter.__name__)
        interpreter3 = ObjectFactory.createObject(Interpreter.__name__)

        print(interpreter1)
        print(interpreter2)
        print(interpreter3)
        print(interpreter1 is interpreter2)
        print(interpreter1 is interpreter3)
        print(interpreter2 is interpreter3)

