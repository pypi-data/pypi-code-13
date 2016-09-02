# -*- coding: utf-8 -*-

from link.middleware.core import Middleware, register_middleware
from link.feature import getfeature

from link.dbrequest.ast import AST
from link.dbrequest.ast import ASTSingleStatementError
from link.dbrequest.ast import ASTLastStatementError
from link.dbrequest.ast import ASTInvalidStatementError
from link.dbrequest.ast import ASTInvalidFormatError

from link.dbrequest.comparison import C, CombinedCondition
from link.dbrequest.assignment import A

from link.dbrequest.lazy import Query, Procedure
from link.dbrequest.driver import Driver

from copy import deepcopy


@register_middleware
class QueryManager(Middleware):
    """
    Manage storage backend and provide query system for it.

    :param backend: Storage backend
    :type backend: Driver
    """

    __protocols__ = ['query']

    def from_ast(self, ast):
        """
        Create a query from the provided AST.

        :param ast: AST
        :type ast: list

        :rtype: Query

        :raises ASTError: if provided AST is not valid.
        """

        self.validate_ast(ast)

        q = Query(self)
        q.ast = deepcopy(ast)

        return q

    def all(self):
        """
        Get a query selecting all elements in store.

        :rtype: Query
        """

        return Query(self)

    def subset(self, scope):
        """
        Get a query selecting all scoped elements in store.

        :param scope: Query's scope
        :type scope: str, Query or list

        :rtype: Query
        """

        return Query(self, scope=scope)

    def prepare(self, f, *queries):
        """
        Get a lazy procedure.

        :param f: Function to call
        :type f: F

        :param queries: Function's scope
        :type queries: list of Query or str

        :returns: New lazy procedure
        :rtype: Procedure
        """

        return Procedure(f, self, scope=queries)

    def run(self, f, *queries):
        """
        Execute a procedure.

        :param f: Function to call
        :type f: F

        :param queries: Function's scope
        :type queries: list of Query or str

        :returns: Procedure's result
        :rtype: any
        """

        return self.prepare(f, *queries)()

    def get(self, condition):
        """
        Get a single element matching the filter.

        :param condition: Filter
        :type condition: C or CombinedCondition

        :returns: Matching element or None
        :rtype: Model or None
        """

        if not isinstance(condition, (C, CombinedCondition)):
            raise TypeError('Supplied condition is not supported: {0}'.format(
                type(condition)
            ))

        return self.execute(AST('get', condition.get_ast()))

    def create(self, *fields):
        """
        Put a new element into the store.

        :param fields: List of assignments
        :type fields: list of A

        :returns: Created element
        :rtype: Model
        """

        fields_ast = []

        for field in fields:
            if not isinstance(field, A):
                raise TypeError('Supplied field is not supported: {0}'.format(
                    type(field)
                ))

            fields_ast.append(field.get_ast())

        return self.execute(AST('create', fields_ast))

    @staticmethod
    def validate_ast(ast):
        """
        Validate AST semantics.

        :raises ASTError: if the AST semantics are not valid
        """

        if isinstance(ast, AST):
            if ast.name not in ['get', 'create', 'run']:
                raise ASTSingleStatementError(ast.name)

        elif isinstance(ast, list):
            statements = [
                'get',
                'filter',
                'exclude',
                'update',
                'delete',
                'count',
                'slice',
                'group'
            ]
            last_statements = ['update', 'delete', 'get', 'count', 'group']
            l = len(ast)

            for i in range(l):
                node = ast[i]

                if node.name in last_statements and (i + 1) != l:
                    raise ASTLastStatementError(node.name, i)

                elif node.name not in statements:
                    raise ASTInvalidStatementError(node.name)

        else:
            raise ASTInvalidFormatError()

    def execute(self, ast, scope=None):
        """
        Send query to the storage driver.

        :param ast: AST describing the query
        :type ast: dict or list

        :param scope: Query's scope
        :type scope: list of str or Query

        :returns: storage driver's response
        """

        self.validate_ast(ast)
        feature = getfeature(
            self.get_child_middleware(),
            Driver.name,
            scope=scope
        )

        if isinstance(ast, AST):
            if ast.name == 'get':
                elements = feature.find_elements(
                    ast.val
                )

                if len(elements) == 0:
                    return None

                else:
                    return elements[0]

            elif ast.name == 'create':
                return feature.put_element(ast.val)

            elif ast.name == 'run':
                return feature.run_procedure(ast.val)

        elif len(ast) == 0:
            return feature.find_elements(ast)

        elif ast[-1].name == 'update':
            return feature.update_elements(
                ast[:-1],
                ast[-1].val
            )

        elif ast[-1].name == 'delete':
            return feature.remove_elements(ast[:-1])

        elif ast[-1].name == 'count':
            return feature.count_elements(ast[:-1])

        else:
            result = feature.find_elements(ast)

            if ast[-1].name == 'get':
                if len(result) == 0:
                    result = None

                else:
                    result = result[0]

            return result
