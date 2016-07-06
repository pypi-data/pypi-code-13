# -*- coding: utf-8 -*-
"""
Event
-----

The event module with declarative ORM event decorators and event registration.

SQLAlchemy features an ORM event API but one thing that is lacking is a way to
register event handlers in a declarative way inside the Model's class
definition. To bridge this gap, this module contains a collection of decorators
that enable this kind of functionality.

Instead of having to write event registration like this::

    from sqlalchemy import event

    from myproject import Model

    class User(Model):
        _id = Column(types.Integer(), primary_key=True)
        email = Column(types.String())

    def set_email_listener(target, value, oldvalue, initiator):
        print 'received "set" event for target: {0}'.format(target)
        return value

    def before_insert_listener(mapper, connection, target):
        print 'received "before_insert" event for target: {0}'.format(target)

    event.listen(User.email, 'set', set_email_listener, retval=True)
    event.listen(User, 'before_insert', before_insert_listener)

Model Events allows one to write event registration more succinctly as::

    from sqlservice import events

    from myproject import Model

    class User(Model):
        _id = Column(types.Integer(), primary_key=True)
        email = Column(types.String())

        @events.on_set('email', retval=True)
        def on_set_email(target, value, oldvalue, initiator):
            print 'received set event for target: {0}'.format(target)
            return value

        @events.before_insert()
        def before_insert(mapper, connection, target):
            print ('received "before_insert" event for target: {0}'
                   .format(target))

For details on each event type's expected function signature, see
`SQLAlchemy's ORM Events
<http://docs.sqlalchemy.org/en/latest/orm/events.html>`_.
"""

from sqlalchemy.event import listen


class Event(object):
    """Universal event class used when registering events."""
    def __init__(self, name, attribute, listener, kargs):
        self.name = name
        self.attribute = attribute
        self.listener = listener
        self.kargs = kargs


class EventDecorator(object):
    """Base class for event decorators that attaches metadata to function
    object so that :func:`register` can find the event definition.
    """
    event_names = ()

    def __init__(self, **event_kargs):
        self.attribute = None
        self.event_kargs = event_kargs

    def __call__(self, func):
        """Function decorator that attaches an `__events__` attribute hook which
        is expected when registering a method as an event handler. See
        :func:`register` for details on how this is implemented.
        """
        if not hasattr(func, '__events__'):
            # Set initial value to list so function can handle multiple events.
            func.__events__ = []

        # Attach event objects to function for register() for find.
        func.__events__ += [Event(name, self.attribute, func, self.event_kargs)
                            for name in self.event_names]

        # Return function so that it's passed on to sa.event.listen().
        return func


class AttributeEventDecorator(EventDecorator):
    """Base class for an attribute event decorators."""
    def __init__(self, attribute, **event_kargs):
        self.attribute = attribute
        self.event_kargs = event_kargs


def register(cls, dct):
    """Register events defined on a class during metaclass creation."""
    events = []

    # Add events that were added via @<event> decorator
    for value in dct.values():
        events.extend(getattr(value, '__events__', []))

    if not events:
        return

    for event in events:
        obj = getattr(cls, event.attribute) if event.attribute else cls
        listen(obj, event.name, event.listener, **event.kargs)


##
# Attribute Events
# http://docs.sqlalchemy.org/en/latest/orm/events.html#attribute-events
##


class on_set(AttributeEventDecorator):
    """Event decorator for the ``set`` event."""
    event_names = ('set',)


class on_append(AttributeEventDecorator):
    """Event decorator for the ``append`` event."""
    event_names = ('append',)


class on_remove(AttributeEventDecorator):
    """Event decorator for the ``remove`` event."""
    event_names = ('remove',)


##
# Mapper Events
# http://docs.sqlalchemy.org/en/latest/orm/events.html#mapper-events
##


class before_delete(EventDecorator):
    """Event decorator for the ``before_delete`` event."""
    event_names = ('before_delete',)


class before_insert(EventDecorator):
    """Event decorator for the ``before_insert`` event."""
    event_names = ('before_insert',)


class before_update(EventDecorator):
    """Event decorator for the ``before_update`` event."""
    event_names = ('before_update',)


class before_save(EventDecorator):
    """Event decorator for the ``before_insert`` and ``before_update`` events.
    """
    event_names = ('before_insert', 'before_update')


class after_delete(EventDecorator):
    """Event decorator for the ``after_delete`` event."""
    event_names = ('after_delete',)


class after_insert(EventDecorator):
    """Event decorator for the ``after_insert`` event."""
    event_names = ('after_insert',)


class after_update(EventDecorator):
    """Event decorator for the ``after_update`` event."""
    event_names = ('after_update',)


class after_save(EventDecorator):
    """Event decorator for the ``after_insert`` and ``after_update`` events."""
    event_names = ('after_insert', 'after_update')


##
# Instance Events
# http://docs.sqlalchemy.org/en/latest/orm/events.html#instance-events
##


class on_expire(EventDecorator):
    """Event decorator for the ``expire`` event."""
    event_names = ('expire',)


class on_load(EventDecorator):
    """Event decorator for the ``load`` event."""
    event_names = ('load',)


class on_refresh(EventDecorator):
    """Event decorator for the ``refresh`` event."""
    event_names = ('refresh',)
