# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import MagicMock
from unittest import main

from link.dbrequest.ast import AST, ModelBuilder, NodeWalker


class ModelBuilderTest(UTCase):
    def setUp(self):
        self.builder = ModelBuilder()

    def test_parse(self):
        ast = AST('node1', [
            AST('node2', 'foo'),
            AST('node3', 'bar')
        ])

        model = self.builder.parse(ast)

        self.assertEqual(model.__class__.__name__, 'ASTNode1')
        self.assertIsNone(model.parent)
        self.assertEqual(len(model.children), 2)

        child1, child2 = model.children

        self.assertEqual(child1.__class__.__name__, 'ASTNode2')
        self.assertIs(child1.parent, model)
        self.assertEqual(child1.val, 'foo')
        self.assertEqual(child1.children, [])

        self.assertEqual(child2.__class__.__name__, 'ASTNode3')
        self.assertIs(child2.parent, model)
        self.assertEqual(child2.val, 'bar')
        self.assertEqual(child2.children, [])


class NodeWalkerTest(UTCase):
    def setUp(self):
        builder = ModelBuilder()
        ast = AST('node1', [
            AST('node2', 'foo'),
            AST('node3', AST('node4', 'bar'))
        ])

        self.model = builder.parse(ast)
        self.child1, self.child2 = self.model.children

        self.walker = NodeWalker()

    def test_find_walker(self):
        result = self.walker.find_walker(self.model)
        self.assertIsNone(result)

        self.walker.walk_default = MagicMock(return_value=None)
        result = self.walker.find_walker(self.model)
        self.assertIs(result, self.walker.walk_default)

        self.walker.walk_ASTNode1 = MagicMock(return_value='expected')
        result = self.walker.find_walker(self.model)
        self.assertIs(result, self.walker.walk_ASTNode1)

        self.walker.walk_ASTNode2 = MagicMock(return_value='foo')
        self.walker.walk_ASTNode3 = MagicMock(return_value='bar')

        result = self.walker.walk(self.model)

        self.walker.walk_ASTNode2.assert_called_with(self.child1, [])
        self.walker.walk_ASTNode3.assert_called_with(self.child2, [None])
        self.walker.walk_ASTNode1.assert_called_with(
            self.model, ['foo', 'bar']
        )
        self.assertEqual(result, 'expected')

        del self.walker.walk_default
        result = self.walker.walk([self.model, self.child2])

        self.assertEqual(result, ['expected', 'bar'])


if __name__ == '__main__':
    main()
