from collections import namedtuple

import flask

__all__ = [
    'LazyNavItem',
    'Nav',
    'NavItem'
    ]


# A named tuple structure used to store the results of `Nav` queries.
QueryResult = namedtuple(
    'QueryResult',
    ['exists', 'allowed', 'active', 'url']
    )


class Nav:
    """
    The `Nav` class is a static class that allows;

    - access rules to be defined and assigned to endpoints,
    - querying of endpoints to see;
        - if an endpoint exists,
        - if access to it is allowed by the caller,
        - if it is the currently active link.
    """

    # A dictionary of nav menus
    _menus = {}

    # A dictionary that holds the defined rules for navigation
    _rules = {}

    # A dictionary that holds the rules for endpoints
    _endpoint_rules = {}

    @classmethod
    def allowed(cls, endpoint, **view_args):
        """Return True if the specified endpoint (plus view_args) is allowed"""
        if endpoint in cls._endpoint_rules:
            for rule_name in cls._endpoint_rules[endpoint]:
                if not cls._rules[rule_name](**view_args):
                    return False
        return True

    @classmethod
    def apply(cls, endpoint, rules):
        """Apply one or more rules to the given endpoint"""
        cls._endpoint_rules[endpoint] = list(rules)

    @classmethod
    def exists(cls, endpoint):
        """Return True if the specified endpoint exists"""
        app = flask.current_app

        # On the first query we need to build a map of endpoints to make
        # querying quicker?
        if not hasattr(cls, '_endpoints'):
            cls._endpoints = set([r.endpoint for r in app.url_map.iter_rules()])

        return endpoint in cls._endpoints

    @classmethod
    def menu(self, name):
        """
        The `menu` method provides a simple way to define and share nav menus
        (reality a `NavItem`) between modules/files. If the named menu exists
        it's returned, if not it's generated, stored and returned.
        """

        if name not in self._menus:
            self._menus[name] = NavItem()

        return self._menus[name]

    @classmethod
    def query(cls, endpoint, **view_args):
        """Query a given endpoint and set of arguments"""
        exists = cls.exists(endpoint)

        # Build the URLs for the endpoint
        url = None
        if exists:
            url = flask.url_for(endpoint, **view_args)

        return QueryResult(
            exists=exists,
            allowed=exists and cls.allowed(endpoint, **view_args),
            active=url == flask.request.path,
            url=url
            )

    @classmethod
    def rule(cls, *args, **kw_args):
        """Decorate a function with this method to define it as a rule"""
        def wrap(func):
            cls.set_rule(func, **kw_args)
            return func

        if len(args) == 1 and callable(args[0]):
            return wrap(args[0])
        else:
            return wrap

    @classmethod
    def set_rule(cls, func, name=None):
        """
        Set a rule, optionally a name can be specified to set the rule for but
        by default the `func`s name will be used.
        """

        assert callable(func), '`func` must be callable'

        cls._rules[name or func.__name__] = func


class NavItem:
    """
    The `NavItem` class provides a way to define structure navigation menus,
    e.g:

        menu = Nav.menu('some_menu')
        menu.add_item('Some link', 'some.endpoint')
        ...
    """

    def __init__(self, label=None, endpoint=None, view_args=None,
            fixed_url=None, id=None, badge=None, data=None, after=None):

        # The label that will be displayed in the interface for the item
        self.label = label

        # The endpoint and view_arguments that will be used to generate the
        # item's URL. Optionally the `view_args` can be a callable that returns
        # a dictionary of arguments.
        self.endpoint = endpoint
        self._view_args = view_args or {}

        # A fixed URL can be specified over an endpoint and view args.
        self.fixed_url = fixed_url

        # An Id for the item, this is not the HTML Id for the nav item, instead
        # the Id is used to make is simple to determine where a nav item is sits
        # within it's parent using the `after` argument. By default the Id is
        # set to the endpoint.
        self.id = id or endpoint

        # Optionally a callable object (e.g a function) can be set as the badge
        # which should return either a boolean to flag if a badge should appear,
        # or an integer to flag if a count badge should appear and the count to
        # display.
        self._badge = badge

        # A dictionary or callable that returns a dictionary that will be
        # available within the HTML template.
        self._data = data or {}

        # If specified, the `after` argument indicates the Id of the nav item
        # sibling to place the item after.
        self.after = after

        # The child items for this item
        self._children = []

        # This item's parent
        self._parent = None

    # Properties

    @property
    def badge(self):
        """
        Return the badge value for item, if the `badge` value is callable then
        the result of calling `badge` will be returned.
        """
        if callable(self._badge):
            return self._badge()
        return self._badge

    @badge.setter
    def badge(self, value):
        """
        Set the badge value for the item, badge values should be either a
        boolean (True, False) or an integer (indicating a count).
        """
        self._badge = value

    @property
    def children(self):
        """
        This property is responsible for pulling together a view of the nav
        item's children at the instant it is called/accessed.
        """

        # Initially we build a first come ordered list of all the items
        indexes = {}
        children = []

        i = 0
        child_stack = list(self._children)
        while len(child_stack):
            child = child_stack.pop(0)
            if isinstance(child, LazyNavItem):
                # Expand lazy items
                child_stack = child.items + child_stack

            else:
                i += 1
                children.append(child)
                if child.id:
                    indexes[child.id] = i

        # Re-order the list based on each items after anchor
        for child in list(children):

            # For children not anchored by `after` do nothing
            if not child.after or child.after not in indexes:
                continue

            # Determine the insertion point
            child_index = children.index(child)
            index = indexes[child.after]

            if index < child_index:
                indexes[child.after] += 1

            # Remove the child from the liust
            children.remove(child)

            # Re-insert the child
            children.insert(index, child)

        return children

    @property
    def data(self):
        """
        Set the data for the nav. Data is typically used in the HTML template.
        """
        if callable(self._data):
            return self._data()
        return self._data

    @data.setter
    def data(self, value):
        """
        Return the data for item, if the `data` value is callable then the
        result of calling `data` will be returned.
        """
        self._data = value

    @property
    def is_parent(self):
        """
        Return True if the item has children.

        Note: Technically if the only child/children for the item are
        `LazyNavItem`s then the item could return True for `is_parent` but not
        actually have any children (due to the dynamic nature of
        `LazyNavItems`), if this possibility needs to be catered for test by
        calling `len(self.children)` and store the result as this is a
        potentially expensive operation.
        """
        return len(self._children) > 0

    @property
    def query(self):
        """Return the `Nav.query` result for the item"""
        return Nav.query(self.endpoint, **self.view_args)

    @property
    def parent(self):
        """Return the parent for the item"""
        return self._parent

    @property
    def view_args(self):
        """
        Return the view arguments for item, if the `view_args` value is callable
        then the result of calling `view_args` will be returned.
        """
        if callable(self._view_args):
            return self._view_args()
        return self._view_args

    @view_args.setter
    def view_args(self, value):
        """
        Set the view arguments that will accompany the endpoint for the item.
        """
        self._view_args = value

    # Methods

    def add(self, item):
        """Add a child to the item"""

        # Add the item as a child
        self._children.append(item)

        # Set the items parent as this item
        item._parent = self

        return item


class LazyNavItem:
    """
    `LazyNavItem`s allow one or more `NavItem`s to be generated dynamically at
    the point the parent `NavItem.children` property is called.
    """

    def __init__(self, func, after=None):

        # The callable/function that will generate nav items in place of the
        # lazy nav item.
        self.func = func

        # If specified, the `after` argument indicates the Id of the nav item
        # sibling to place the item after.
        self.after = after

        # This item's parent
        self._parent = None

    @property
    def items(self):
        """Generate the nav items for this lazy nav item"""
        items = self.func(self)

        # Ensure each item is assigned a default `after`
        if self.after:
            for item in items:
                item.after = item.after or self.after

        return items

    @property
    def parent(self):
        return self._parent