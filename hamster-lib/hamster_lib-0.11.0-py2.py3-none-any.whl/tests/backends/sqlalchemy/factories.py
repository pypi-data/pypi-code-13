# -*- encoding: utf-8 -*-

"""Factories for sqlalchemy models."""

from __future__ import unicode_literals

import datetime

import factory
from hamster_lib.backends.sqlalchemy.objects import (AlchemyActivity,
                                                     AlchemyCategory,
                                                     AlchemyFact)

from . import common


class AlchemyCategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory class for generic ``AlchemyCategory`` instances."""

    pk = factory.Sequence(lambda n: n)

    @factory.sequence
    def name(n):  # NOQA
        """Return a name that is guaranteed to be unique."""
        return '{name} - {key}'.format(name=factory.Faker('word'), key=n)

    class Meta:
        model = AlchemyCategory
        sqlalchemy_session = common.Session
        force_flush = True


class AlchemyActivityFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory class for generic ``AlchemyActivity`` instances."""

    pk = factory.Sequence(lambda n: n)
    name = factory.Faker('sentence')
    category = factory.SubFactory(AlchemyCategoryFactory)
    deleted = False

    class Meta:
        model = AlchemyActivity
        sqlalchemy_session = common.Session
        force_flush = True


class AlchemyFactFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory class for generic ``AlchemyFact`` instances."""

    pk = factory.Sequence(lambda n: n)
    activity = factory.SubFactory(AlchemyActivityFactory)
    start = factory.Faker('date_time')
    end = factory.LazyAttribute(lambda o: o.start + datetime.timedelta(hours=3))
    description = factory.Faker('paragraph')
    tags = []

    class Meta:
        model = AlchemyFact
        sqlalchemy_session = common.Session
        force_flush = True
