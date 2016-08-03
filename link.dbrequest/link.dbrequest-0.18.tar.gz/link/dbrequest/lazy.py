# -*- coding: utf-8 -*-

from link.dbrequest.comparison import C, CombinedCondition
from link.dbrequest.expression import F
from link.dbrequest.assignment import A
from link.dbrequest.ast import AST

from six import string_types
from copy import deepcopy


class Lazy(object):
    """
    Object holding data that will be fetched by the manager when needed.

    :param manager: Manager that will execute this query
    :type manager: QueryManager

    :param scope: Object's scope (default: None)
    :type scope: str, Query or list
    """

    def __init__(self, manager, scope=None, *args, **kwargs):
        super(Lazy, self).__init__(*args, **kwargs)

        self.manager = manager
        self.data = None

        if scope is None:
            scope = []

        elif isinstance(scope, string_types + (Lazy,)):
            scope = [scope]

        else:
            scope = list(scope)

        self.scope = scope

    def execute(self):
        """
        Execute object

        :returns: Data held by object
        :rtype: any
        """

        raise NotImplementedError()

    def __call__(self, cache=True):
        data = None

        if cache:
            data = self.data

        if data is None:
            data = self.execute()

        if cache:
            self.data = data

        return data


class Dataset(Lazy):
    """
    Lazy dataset, hold scoped set of data.
    """

    def __iter__(self):
        """
        Execute lazy object and iterate through result
        """

        return iter(self())


class Query(Dataset):
    """
    Database agnostic query.

    :param manager: Manager that will execute this query
    :type manager: QueryManager
    """

    def __init__(self, *args, **kwargs):
        super(Query, self).__init__(*args, **kwargs)

        self.ast = []

    def execute(self):
        return self.manager.execute(self.ast, scope=self.scope)

    def copy(self):
        """
        Create a copy of this query.

        :returns: Copy
        :rtype: Query
        """

        c = Query(self.manager, scope=self.scope)
        c.ast = self.to_ast()
        return c

    def to_ast(self):
        """
        Returns a copy of query's AST

        :returns: AST
        :rtype: list
        """

        return deepcopy(self.ast)

    def count(self):
        """
        Count elements matched by this query.

        :returns: Number of matching elements
        :rtype: int
        """

        c = self.copy()
        c.ast.append(AST('count', None))

        return c()

    def get(self, condition):
        """
        Add filter to the query, and get a single element matching the query.

        :param condition: Filter
        :type condition: C or CombinedCondition

        :returns: Matching element or None
        :rtype: Model or None
        """

        c = self.copy()

        if not isinstance(condition, (C, CombinedCondition)):
            raise TypeError('Supplied condition is not supported: {0}'.format(
                type(condition)
            ))

        c.ast.append(AST('get', condition.get_ast()))

        return c()

    def filter(self, condition):
        """
        Returns a new query with a new filter added.

        :param condition: Filter
        :type condition: C or CombinedCondition

        :returns: Query
        :rtype: Query
        """

        c = self.copy()

        if not isinstance(condition, (C, CombinedCondition)):
            raise TypeError('Supplied condition is not supported: {0}'.format(
                type(condition)
            ))

        c.ast.append(AST('filter', condition.get_ast()))

        return c

    def exclude(self, condition):
        """
        Returns a new query with a new (negated) filter added.

        :param condition: Filter
        :type condition: C or CombinedCondition

        :returns: Query
        :rtype: Query
        """

        c = self.copy()

        if not isinstance(condition, (C, CombinedCondition)):
            raise TypeError('Supplied condition is not supported: {0}'.format(
                type(condition)
            ))

        c.ast.append(AST('exclude', condition.get_ast()))

        return c

    def __getitem__(self, s):
        """
        Returns a new query with a slice of filtered elements.

        :param s: query's slice
        :type s: slice

        :returns: Query
        :rtype: Query
        """

        c = self.copy()

        if not isinstance(s, slice):
            s = slice(s)

        c.ast.append(AST('slice', s))

        return c

    def update(self, *fields):
        """
        Update elements matching the query.

        :param fields: Assignments
        :type fields: list of A

        :returns: Number of modified elements.
        :rtype: int
        """

        c = self.copy()

        fields_ast = []

        for field in fields:
            if not isinstance(field, A):
                raise TypeError('Supplied field is not supported: {0}'.format(
                    type(field)
                ))

            fields_ast.append(field.get_ast())

        c.ast.append(AST('update', fields_ast))

        return c()

    def delete(self):
        """
        Delete elements matching the query.

        :returns: Number of deleted elements.
        :rtype: int
        """

        c = self.copy()
        c.ast.append(AST('delete', None))

        return c()

    def group(self, key, *expressions):
        """
        Group elements by key matching the query using the expressions.

        :param key: Key used to group elements
        :type key: str

        :param expressions: Expressions
        :type expressions: list of CombinableExpression

        :returns: Grouped elements.
        """

        c = self.copy()
        c.ast.append(
            AST(
                'group',
                [
                    AST('prop', key)
                ] + [
                    expression.get_ast()
                    for expression in expressions
                ]
            )
        )

        return c()


class Procedure(Dataset):
    def __init__(self, f, *args, **kwargs):
        super(Procedure, self).__init__(*args, **kwargs)

        if not isinstance(f, F):
            raise TypeError('Expecting F, got: {0}'.format(type(f)))

        self.f = f

    def copy(self):
        return Procedure(self.f, self.manager, scope=self.scope)

    def to_ast(self):
        return AST('run', self.f.get_ast())

    def execute(self):
        return self.manager.execute(self.to_ast(), scope=self.scope)
