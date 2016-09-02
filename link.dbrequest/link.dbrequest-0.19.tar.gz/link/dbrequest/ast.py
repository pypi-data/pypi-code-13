# -*- coding: utf-8 -*-


class AST(dict):
    """
    Helper for create AST nodes.

    :param name: AST node name
    :type name: str

    :param val: AST node value
    """

    def __init__(self, name, val, *args, **kwargs):
        super(AST, self).__init__(*args, **kwargs)

        self.name = name
        self.val = val
        self.parent = None
        self.children = []

    @property
    def name(self):
        return self['name']

    @name.setter
    def name(self, value):
        self['name'] = value

    @property
    def val(self):
        return self['val']

    @val.setter
    def val(self, value):
        self['val'] = value


class ASTError(Exception):
    """
    Basic AST semantic error.
    """

    pass


class ASTSingleStatementError(ASTError):
    """
    Error raised when trying to execute statements that must be in a sequence.
    """

    def __init__(self, stmt):
        super(ASTSingleStatementError, self).__init__(
            'Single statement must be "get" or "create", got: {0}'.format(
                stmt
            )
        )


class ASTLastStatementError(ASTError):
    """
    Error raised when trying to execute a statement that must be in the end of
    the sequence.
    """

    def __init__(self, stmt, pos):
        super(ASTLastStatementError, self).__init__(
            'Statement "{0}" must be last, got position: {1}'.format(stmt, pos)
        )


class ASTInvalidStatementError(ASTError):
    """
    Error raised when trying to execute an unknown statement.
    """

    def __init__(self, stmt):
        super(ASTInvalidStatementError, self).__init__(
            'Statement not allowed in this context: {0}'.format(stmt)
        )


class ASTInvalidFormatError(ASTError):
    """
    Error raised when supplied AST is not a valid expected type.
    """

    def __init__(self):
        super(ASTInvalidFormatError, self).__init__(
            'AST must be a list or a dict'
        )


class ModelBuilder(object):
    """
    Class used to link nodes in AST together.
    """

    def __init__(self, *args, **kwargs):
        super(ModelBuilder, self).__init__(*args, **kwargs)

        self.cache_cls = {}

    def parse(self, node, parent=None):
        """
        Parse AST to resolve link between nodes.

        :param node: node to parse
        :type node: AST or list or value

        :param parent: parent node (default: None)
        :type parent: AST or None

        :returns: Node
        :rtype: same as param node
        """

        if isinstance(node, AST):
            if node.name not in self.cache_cls:
                self.cache_cls[node.name] = type(
                    'AST{0}'.format(
                        ''.join([
                            name.capitalize()
                            for name in node.name.split('_')
                        ])
                    ),
                    (AST,),
                    {}
                )

            cls = self.cache_cls[node.name]

            result = cls(node.name, node.val)
            result.parent = parent

            if parent is not None:
                parent.children.append(result)

            result.val = self.parse(node.val, parent=result)

        elif isinstance(node, list):
            result = [
                self.parse(subnode, parent=parent)
                for subnode in node
            ]

        else:
            result = node

        return result


class NodeWalker(object):
    """
    Walk through AST.
    """

    def find_walker(self, node):
        """
        Find method used to walk through specific node.

        :param node: node to walk through
        :type node: AST

        :returns: Method used to walk through the node
        :rtype: callable or None
        """

        return getattr(
            self,
            'walk_{0}'.format(node.__class__.__name__),
            getattr(self, 'walk_default', None)
        )

    def walk(self, node, *args, **kwargs):
        """
        Walk through AST (depth first).

        :param node: Root node to start walking through
        :type node: any

        :param args: Positional arguments for walker method
        :type args: iterable

        :param kwargs: Keyword arguments for walker method
        :type kwargs: dict

        :returns: Walker method's result
        """

        result = node

        if isinstance(node, AST):
            children = [
                self.walk(child, *args, **kwargs)
                for child in node.children
            ]

            walker = self.find_walker(node)

            if callable(walker):
                result = walker(node, children, *args, **kwargs)

            else:
                result = None

        elif isinstance(node, list):
            result = [
                self.walk(item, *args, **kwargs)
                for item in node
            ]

        return result
