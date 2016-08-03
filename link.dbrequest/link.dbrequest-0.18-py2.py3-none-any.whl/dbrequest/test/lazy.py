# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import MagicMock
from unittest import main

from link.dbrequest.lazy import Lazy, Dataset, Procedure
from link.dbrequest.expression import F


class LazyTest(UTCase):
    def test_lazy(self):
        l = Lazy('manager')

        self.assertEqual(l.manager, 'manager')
        self.assertEqual(l.scope, [])
        self.assertIsNone(l.data)

    def test_scope(self):
        l1 = Lazy('manager', scope='scope')
        self.assertEqual(l1.scope, ['scope'])

        l2 = Lazy('manager', scope=l1)
        self.assertEqual(l2.scope, [l1])

        l3 = Lazy('manager', scope=(l1, l2))
        self.assertEqual(l3.scope, [l1, l2])

        l4 = Lazy('manager', scope=[l1, l2, l3])
        self.assertEqual(l4.scope, [l1, l2, l3])

    def test_execute(self):
        l = Lazy('manager')
        expected = 'result'
        l.execute = MagicMock(return_value=expected)

        result = l()

        self.assertEqual(l.data, result)
        self.assertEqual(result, expected)

    def test_execute_nocache(self):
        l = Lazy('manager')
        expected = 'result'
        l.execute = MagicMock(return_value=expected)

        result = l(cache=False)

        self.assertIsNone(l.data)
        self.assertEqual(result, expected)

    def test_dataset(self):
        d = Dataset('manager')
        expected = [1, 2, 3]
        d.execute = MagicMock(return_value=expected)

        result = list(d())

        self.assertEqual(result, expected)

    def test_procedure(self):
        manager = MagicMock()
        manager.execute = MagicMock(return_value='expected')

        with self.assertRaises(TypeError):
            Procedure('wrong', manager)

        p = Procedure(F('sum'), manager)

        ast = p.to_ast()

        self.assertEqual(
            ast,
            {
                'name': 'run',
                'val': {
                    'name': 'func_sum',
                    'val': []
                }
            }
        )

        result = p()

        self.assertEqual(result, 'expected')
        manager.execute.assert_called_with(
            p.to_ast(),
            scope=[]
        )

    def test_copy_procedure(self):
        p1 = Procedure(F('sum'), 'manager')
        p2 = p1.copy()

        self.assertIs(p1.manager, p2.manager)
        self.assertEqual(p1.f, p2.f)
        self.assertEqual(p1.scope, p2.scope)


if __name__ == '__main__':
    main()
