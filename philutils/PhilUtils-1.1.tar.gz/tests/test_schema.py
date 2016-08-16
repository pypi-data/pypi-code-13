#!/usr/bin/env python

import unittest
from philutils import schema
from datetime import date


class TestMappingDefinition(unittest.TestCase):
    def test_mapping_definition(self):
        class TestMapping(schema.Mapping):
            key_type = int
            value_type = str

    def test_mapping_definition_with_callable_attribute(self):
        class TestMapping(schema.Mapping):
            key_type = int
            value_type = str

            def return_caps(self):
                return "CAPS"
        self.assertIn('return_caps', dir(TestMapping))

    def test_mapping_definition_with_noncallable_attribute(self):
        class TestMapping(schema.Mapping):
            key_type = int
            value_type = str
            blue = 5
        self.assertIn('blue', dir(TestMapping))

    def test_defining_mapping_type_without_specifying_key_type(self):
        with self.assertRaises(ValueError):
            class TestMapping(schema.Mapping):
                value_type=int

    def test_defining_mapping_type_without_specifying_value_type(self):
        with self.assertRaises(ValueError):
            class TestMapping(schema.Mapping):
                key_type=str

    def test_defining_mapping_type_with_invalid_key_type(self):
        with self.assertRaises(TypeError):
            class TestMapping(schema.Mapping):
                key_type='moose'
                value_type=int

    def test_defining_mapping_type_with_invalid_value_type(self):
        with self.assertRaises(TypeError):
            class TestMapping(schema.Mapping):
                key_type=str
                value_type=4


class TestMappingInit(unittest.TestCase):
    def setUp(self):
        class MyMapping(schema.Mapping):
            key_type = int
            value_type = str
        self.mapping_class = MyMapping

    def test_init_method(self):
        new_mapping = self.mapping_class()
        self.assertIsInstance(new_mapping, self.mapping_class)


class TestMappingSetItem(unittest.TestCase):
    def setUp(self):
        class MyMapping(schema.Mapping):
            key_type = int
            value_type = str
        self.mapping = MyMapping()

    def test_set_item_and_getitem(self):
        self.mapping[5] = 'banana'
        self.assertEqual(self.mapping[5], 'banana')

    def test_repr(self):
        expected_value = 'Mapping int -> str'
        self.assertEqual(repr(self.mapping), expected_value)

    def test_len(self):
        self.mapping[5] = 'banana'
        self.mapping[3] = 'moose'
        self.mapping[4] = 'orange'
        self.assertEqual(len(self.mapping), 3)

    def test_iter(self):
        self.mapping[5] = 'banana'
        self.mapping[3] = 'moose'
        count = 0
        result_dict = dict()
        for x in self.mapping:
            result_dict[x] = self.mapping[x]
            count = count + 1
        self.assertEqual(count, 2)
        self.assertEqual(result_dict, {5: 'banana', 3: 'moose'})

    def test_setting_invalid_key(self):
        with self.assertRaises(TypeError):
            self.mapping['moose'] = 'blue'

    def test_setting_invalid_value(self):
        with self.assertRaises(TypeError):
            self.mapping[5] = 45




class TestDocumentDefinition(unittest.TestCase):
    def test_document_definition(self):
        class TestDoc(schema.Document):
            id = schema.IntegerField(required=True)
            name = schema.StringField(default="moose")
            date = schema.DateField(default=date.today)
            def funkyfunk(self):
                return 'superfunk' + str(self.id)


class TestDocumentCreation(unittest.TestCase):
    def setUp(self):
        class TestDoc(schema.Document):
            id = schema.IntegerField(required=True)
            name = schema.StringField(default="moose")
            date = schema.DateField(default=date.today)
            def funkyfunk(self):
                return 'superfunk' + str(self.id)
        self.document_class = TestDoc

    def test_creation_of_new_document(self):
        new_doc = self.document_class(id=4)
        self.assertIsInstance(new_doc, self.document_class)
        self.assertEqual(new_doc.id, 4)
        self.assertEqual(new_doc.name, "moose")
        self.assertEqual(new_doc.date, date.today())

    def test_creation_of_new_document_sending_unknown_property(self):
        new_doc = self.document_class(id=4, fruit='banana')
        self.assertIsInstance(new_doc, self.document_class)
        self.assertEqual(new_doc.id, 4)
        self.assertEqual(new_doc.name, "moose")
        self.assertEqual(new_doc.date, date.today())

class TestDocumentProperties(unittest.TestCase):
    def setUp(self):
        class TestDoc(schema.Document):
            id = schema.IntegerField(required=True)
            name = schema.StringField(default="moose")
            date = schema.DateField(default=date.today)
            def funkyfunk(self):
                return 'superfunk' + str(self.id)
        self.document_class = TestDoc
        self.instance = TestDoc(id=4)

    def test_setting_property(self):
        self.instance.id = 5
        self.assertEqual(self.instance._fields['id']._value, 5)
        self.assertEqual(self.instance.id, 5)
        self.assertEqual(self.instance.name, "moose")
        self.assertEqual(self.instance.date, date.today())

    def test_setting_property_using_invalid_value(self):
        self.assertRaises(TypeError, setattr, self.instance, 'id', 'redtail')

    def test_calling_method_defined_on_document_class(self):
        self.assertEqual(self.instance.funkyfunk(), 'superfunk4')

    def test_repr_method(self):
        repr(self.instance)

    def test_getting_nonexistant_attribute(self):
        self.assertRaises(AttributeError, getattr, self.instance, 'greenboat')

    def test_getitem_method(self):
        self.assertEqual(self.instance['name'], 'moose')
