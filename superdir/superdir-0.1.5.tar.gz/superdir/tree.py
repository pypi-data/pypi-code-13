# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import utils
import pdb

class Tree:

    def __init__(self, INDENT_SIZE=None, OUTPUT_DIR=None, base_path=None):

        self.INDENT_SIZE = INDENT_SIZE
        self.OUTPUT_DIR = OUTPUT_DIR
        self.base_path = base_path
        self.data = None
        self.root = None

    def build_tree(self):
        ''' Build tree from indentation. '''

        virtual_root = self._make_new_node(
            parent      = None,
            children    = [],
            value       = None,
            path        = self.base_path
        )

        root = self._make_new_node(
            parent      = virtual_root,
            children    = [],
            value       = self.OUTPUT_DIR, 
            # issue here: if no output dir? Then what ?
            path        = ( os.path.join(self.base_path, self.OUTPUT_DIR) 
                            if self.OUTPUT_DIR 
                            else self.base_path )
        )

        virtual_root['children'].append(root)

        parent_node = virtual_root
        prev_indent = -1
        for line in self.data:

            cur_indent = utils.get_indent_count(line, self.INDENT_SIZE)
            distance = cur_indent - prev_indent
            filename = (utils.get_dirname(line)
                       if utils.is_dir(line)
                       else utils.get_filename(line))

            parent_node = self._find_new_parent(parent_node, distance)

            child = self._make_new_node(
                parent   = parent_node, 
                children = [] if utils.is_dir(line) else None,
                value    = filename,
                path     = os.path.join(parent_node['path'], filename)
            ) 

            parent_node['children'].append(child)
            prev_indent = cur_indent

        self.root = virtual_root

    def _find_new_parent(self, parent_node, distance):

        new_parent = parent_node

        if distance > 0:
            new_parent = parent_node['children'][-1]

        elif distance < 0:
            new_parent = self._find_ancestor(parent_node, distance)

        return new_parent

    def walk(self, callbacks):
        ''' Walk tree and call callback on each node. '''

        def _walk(tree):

            children = tree['children']

            for child in children:

                if callbacks:
                    for cb in callbacks:
                        cb(child)

                if child['children'] is not None:
                    _walk(child)

        tree = self.root
        _walk(tree)

    def load_data(self, data):
        ''' Load and clean up input data '''

        self.data = utils.clean(data)

    def _make_new_node(self, parent=None, children=None, value=None, path=''):
        ''' Create a new node. If children is NoneType, node is treated as a 
        leaf. 
        '''
        return  dict(parent=parent, children=children, value=value, path=path)

    def _find_ancestor(self, start_node, parents_to_visit):
        ''' Return parent directory corresponding to node parsed from current line. '''

        current_node = start_node

        while (parents_to_visit > 0):
            current_node = current_node['parent']
            parents_to_visit -= 1

        return current_node
