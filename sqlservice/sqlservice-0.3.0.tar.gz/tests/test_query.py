# -*- coding: utf-8 -*-

import pytest
import sqlalchemy as sa

import pydash as pyd
from pydash.chaining import Chain
from sqlservice.query import Query

from .fixtures import AModel, CModel, DModel, parametrize, random_alpha


def test_query_entities(db):
    """Test Query.entities/join_entities/all_entities."""
    entities = [AModel]
    join_entities = [CModel, DModel]

    query = db.query(*entities).join(*join_entities)

    assert query.entities == entities
    assert query.join_entities == join_entities
    assert query.all_entities == entities + join_entities


@parametrize('model_class,data,callback,expected', [
    (AModel,
     [{'name': 'a'}, {'name': 'b'}],
     lambda model: model.name * 2,
     ['aa', 'bb']),
])
def test_query_map(db, model_class, data, callback, expected):
    """Test Query.map."""
    db.save([model_class(item) for item in data])
    assert db.query(model_class).map(callback) == expected


@parametrize('model_class,data,callback,initial,expected', [
    (AModel,
     [{'name': 'a'}, {'name': 'b'}],
     lambda ret, model: ret + model.name,
     '',
     'ab'),
])
def test_query_reduce(db, model_class, data, callback, initial, expected):
    """Test Query.reduce."""
    db.save([model_class(item) for item in data])
    result = db.query(model_class).reduce(callback, initial=initial)
    assert result == expected


@parametrize('model_class,data,callback,initial,expected', [
    (AModel,
     [{'name': 'a'}, {'name': 'b'}],
     lambda ret, model: ret + model.name,
     '',
     'ba'),
])
def test_query_reduce_right(db,
                            model_class,
                            data,
                            callback,
                            initial,
                            expected):
    """Test Query.reduce_right."""
    db.save([model_class(item) for item in data])
    result = db.query(model_class).reduce_right(callback, initial=initial)
    assert result == expected


@parametrize('model_class,data,column,expected', [
    (AModel, [{'name': 'a'}, {'name': 'b'}], 'name', ['a', 'b']),
])
def test_query_pluck(db, model_class, data, column, expected):
    """Test Query.pluck."""
    db.save([model_class(item) for item in data])
    assert db.query(model_class).pluck(column) == expected


@parametrize('model_class,data', [
    (AModel, [{'name': 'a'}, {'name': 'b'}]),
])
def test_query_chain(db, model_class, data):
    """Test Query.chain."""
    db.save([model_class(item) for item in data])
    chain = db.query(model_class).chain()

    assert isinstance(chain, Chain)

    keys = list(data[0].keys())
    results = (chain
               .map(dict)
               .map(lambda item: pyd.pick(item, keys))
               .value())

    assert results == data


@parametrize('model_class,data,callback,expected', [
    (AModel,
     [{'name': 'a'}, {'name': 'b'}],
     'name',
     {'a': {'name': 'a'}, 'b': {'name': 'b'}}),
])
def test_query_index_by(db, model_class, data, callback, expected):
    """Test Query.index_by."""
    db.save([model_class(item) for item in data])
    results = db.query(model_class).index_by(callback)

    for key, value in results.items():
        assert pyd.pick(dict(value), pyd.keys(expected[key])) == expected[key]


@parametrize('model_class,data,callback,expected', [
    (AModel,
     [{'name': 'a'}, {'name': 'b'}, {'name': 'a'}],
     'name',
     {'a': [{'name': 'a'}, {'name': 'a'}], 'b': [{'name': 'b'}]}),
])
def test_query_stack_by(db, model_class, data, callback, expected):
    """Test Query.stack_by."""
    db.save([model_class(item) for item in data])
    results = db.query(model_class).stack_by(callback)

    for key, items in results.items():
        items = [pyd.pick(dict(item), pyd.keys(expected[key][0]))
                 for item in items]
        assert items == expected[key]


@parametrize('model_class,data,count', [
    (AModel, [{'name': 'a'}, {'name': 'b'}, {'name': 'c'}], 1),
    (AModel, [{'name': 'a'}, {'name': 'b'}, {'name': 'c'}], 2),
    (AModel, [{'name': 'a'}, {'name': 'b'}, {'name': 'c'}], 3),
    (AModel, [{'name': 'a'}, {'name': 'b'}, {'name': 'c'}], 50),
])
def test_query_top(db, model_class, data, count):
    """Test Query.top."""
    models = db.save([model_class(item) for item in data])

    if count == 1:
        assert db.query(model_class).top(count) == models[0]
    else:
        assert db.query(model_class).top(count) == models[:count]


@parametrize('pagination,limit,offset', [
    (15, 15, None),
    ((15,), 15, None),
    ((15, 1), 15, None),
    ((15, 2), 15, 15),
    ((15, 3), 15, 30),
    ((15, -1), 15, None),
    ((15, -2), 15, None),
    ((15, -3), 15, None),
])
def test_query_paginate(db, pagination, limit, offset):
    """Test Query.paginate."""
    query = db.query(AModel).paginate(pagination)

    assert query._limit == limit
    assert query._offset == offset
