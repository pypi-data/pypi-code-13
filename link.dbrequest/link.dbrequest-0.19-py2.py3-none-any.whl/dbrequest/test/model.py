# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import Mock
from unittest import main

from link.dbrequest.model import Model
from link.dbrequest.ast import AST
import json


class ModelTest(UTCase):
    def setUp(self):
        self.driver = Mock()

        self.doc = {
            'foo': 'bar',
            'bar': 'baz'
        }
        self.model = Model(self.driver, self.doc)

    def test_model_access(self):
        self.assertEqual(self.model.data, self.doc)
        self.assertEqual(self.model.foo, self.doc['foo'])
        self.assertEqual(self.model['foo'], self.doc['foo'])

        self.model.baz = 'biz'

        self.assertEqual(self.model.baz, 'biz')
        self.assertEqual(self.model['baz'], 'biz')

        del self.model.baz

        with self.assertRaises(AttributeError):
            self.model.baz

        with self.assertRaises(KeyError):
            self.model['baz']

    def test_model_str_repr(self):
        result = json.loads(str(self.model))

        self.assertEqual(result, self.doc)
        self.assertTrue(repr(self.model).startswith('Model('))
        self.assertTrue(repr(self.model).endswith(')'))

        o = len('Model(')
        l = len(')')

        result = json.loads(repr(self.model)[o:-l])
        self.assertTrue(result, self.doc)

    def test_model_get_filter(self):
        c = self.model._get_filter()
        ast = c.get_ast()

        expected_val = [
            {
                'name': 'cond_eq',
                'val': [
                    {
                        'name': 'prop',
                        'val': 'foo'
                    },
                    {
                        'name': 'val',
                        'val': 'bar'
                    }
                ]
            },
            {
                'name': 'cond_eq',
                'val': [
                    {
                        'name': 'prop',
                        'val': 'bar'
                    },
                    {
                        'name': 'val',
                        'val': 'baz'
                    }
                ]
            }
        ]

        self.assertEqual(ast.name, 'join_and')
        self.assertTrue(
            ast.val[0] == expected_val[0]
            or ast.val[0] == expected_val[1]
        )
        self.assertTrue(
            ast.val[1] == expected_val[0]
            or ast.val[1] == expected_val[1]
        )

    def test_model_get_update(self):
        a = self.model._get_update()
        ast = [_a.get_ast() for _a in a]

        a1 = {
            'name': 'assign',
            'val': [
                {
                    'name': 'prop',
                    'val': 'foo'
                },
                {
                    'name': 'val',
                    'val': 'bar'
                }
            ]
        }
        a2 = {
            'name': 'assign',
            'val': [
                {
                    'name': 'prop',
                    'val': 'bar'
                },
                {
                    'name': 'val',
                    'val': 'baz'
                }
            ]
        }

        self.assertEqual(len(ast), 2)
        self.assertIn(a1, ast)
        self.assertIn(a2, ast)

    def test_model_save(self):
        attrs = {
            'put_element.return_value': Model(self.driver, {
                '_id': 'some id',
                'foo': 'bar',
                'bar': 'baz'
            })
        }
        a1 = {
            'name': 'assign',
            'val': [
                {
                    'name': 'prop',
                    'val': 'foo'
                },
                {
                    'name': 'val',
                    'val': 'bar'
                }
            ]
        }
        a2 = {
            'name': 'assign',
            'val': [
                {
                    'name': 'prop',
                    'val': 'bar'
                },
                {
                    'name': 'val',
                    'val': 'baz'
                }
            ]
        }

        self.driver.configure_mock(**attrs)

        new_model = self.model.save()

        self.assertEqual(new_model._id, 'some id')

        args = self.driver.put_element.call_args[0]

        self.assertEqual(len(args), 1)
        self.assertIsInstance(args[0], list)
        self.assertIn(a1, args[0])
        self.assertIn(a2, args[0])

    def test_model_remove(self):
        attrs = {
            'remove_elements.return_value': None
        }
        self.driver.configure_mock(**attrs)

        expected_val = [
            {
                'name': 'cond_eq',
                'val': [
                    {
                        'name': 'prop',
                        'val': 'foo'
                    },
                    {
                        'name': 'val',
                        'val': 'bar'
                    }
                ]
            },
            {
                'name': 'cond_eq',
                'val': [
                    {
                        'name': 'prop',
                        'val': 'bar'
                    },
                    {
                        'name': 'val',
                        'val': 'baz'
                    }
                ]
            }
        ]

        self.model.delete()

        args = self.driver.remove_elements.call_args[0]

        self.assertEqual(len(args), 1)
        self.assertIsInstance(args[0], list)
        self.assertEqual(len(args[0]), 1)
        self.assertIsInstance(args[0][0], AST)
        self.assertTrue(args[0][0].name, 'filter')
        self.assertIsInstance(args[0][0].val, AST)
        self.assertEqual(args[0][0].val.name, 'join_and')

        self.assertTrue(
            args[0][0].val.val[0] == expected_val[0]
            or args[0][0].val.val[0] == expected_val[1]
        )
        self.assertTrue(
            args[0][0].val.val[1] == expected_val[0]
            or args[0][0].val.val[1] == expected_val[1]
        )


if __name__ == '__main__':
    main()
