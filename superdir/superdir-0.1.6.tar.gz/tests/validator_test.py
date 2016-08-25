import os
from StringIO import StringIO

import pytest

from superdir.validator import Validator

def full_path(fname):
    return os.path.abspath(os.path.join(os.curdir, 'tests/schemas', fname)) 

good_schema = list(open(full_path('good_schema.txt')))
bad_schema_1 = list(open(full_path('bad_schema1.txt')))
bad_schema_2 = list(open(full_path('bad_schema2.txt')))
schema_single_top_level = list(open(full_path('schema_single_top_level.txt')))
schema_mult_top_levels = list(open(full_path('schema_mult_top_levels.txt')))

def test_find_first_indent():

    validator = Validator(good_schema)
    indent_data = validator._find_first_indent()
    assert indent_data['indent_size'] == 4  
    assert indent_data['index'] == 1

def test_schema_single_top_level():

    top_dir_name = None
    validator = Validator(schema_single_top_level)
    assert validator._top_dir_is_valid(top_dir_name)

def test_schema_multiple_top_levels():

    top_dir_name = 'Test_Dir'
    validator = Validator(schema_mult_top_levels)
    assert validator._top_dir_is_valid(top_dir_name)


    top_dir_name = None 
    validator = Validator(schema_mult_top_levels)
    assert not validator._top_dir_is_valid(top_dir_name)
    

def test_validate_good_schema():
    ''' This test needs to be more granular, there's a conflict of interest regarding the output dir here '''

    validator = Validator(good_schema)
    assert validator.validate()

def test_validate_bad_schema():
    ''' This test needs to be more granular, there's a conflict of interest regarding the output dir here '''

    validator = Validator(bad_schema_1)
    assert not validator.validate()

    validator = Validator(bad_schema_2)
    assert not validator.validate()

