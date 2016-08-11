import os
from StringIO import StringIO

from scaffolder.tree import Tree
from scaffolder.utils import clean

def test_tree_obj():

    schema_file = 'good_schema.txt'
    schema = clean(open(schema_file).readlines())

    new_tree = Tree(
        indent_size = 4,
        output_dir = 'new_app',
    )

    new_tree.load_data(schema)

    assert new_tree.data is not None
    assert new_tree.indent_size == 4 
    assert new_tree.output_dir == 'new_app'

def test_build_tree():
    schema_file = 'good_schema.txt'
    schema = clean(open(schema_file).readlines())

    new_tree = Tree(
        indent_size = 4,
        output_dir = 'new_app'
    )
    new_tree.load_data(schema)
    new_tree.build_tree()

    assert new_tree.root is not None


def test_walk():
    pass

def test_load_data():
    pass

def test_make_new_node():
    pass

def test_find_ancestor():
    pass

