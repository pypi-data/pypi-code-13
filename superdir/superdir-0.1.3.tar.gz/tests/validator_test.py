import os
from StringIO import StringIO

import pytest

from scaffolder.validator import Validator

good_schema = open('good_schema.txt').readlines()
bad_schema = open('bad_schema.txt').readlines()

def test_load_schema():

    validator = Validator()
    validator.load_schema(good_schema)
    assert validator.schema


def test_validate_success():

    validator = Validator()
    validator.load_schema(good_schema)
    indent_size = validator.validate()

    assert indent_size >= 0

def test_validate_failure():

    validator = Validator()
    validator.load_schema(bad_schema)

    with pytest.raises(ValueError):
        assert Validator().validate() >= 0
