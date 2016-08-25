import os
from StringIO import StringIO

import pytest

from superdir.tree import Tree

def test_tree_constructor():

    tree = Tree(
        INDENT_SIZE = 4,
        OUTPUT_DIR = 'TEST_DIR',
        base_path = os.path.abspath(os.curdir)
    )

    assert type(tree.INDENT_SIZE) is int 
    assert tree.INDENT_SIZE is not None

    assert type(tree.OUTPUT_DIR) is str
    assert tree.OUTPUT_DIR is not None

    assert type(tree.base_path) is str
    assert tree.base_path is not None

