#!/usr/bin/env python
# encoding: utf-8

# Front Matter {{{
'''
Copyright (c) 2016 The Broad Institute, Inc.  All rights are reserved.

mdbindex: this file is part of mdbtools.  See the <root>/COPYRIGHT
file for the SOFTWARE COPYRIGHT and WARRANTY NOTICE.

@author: Michael S. Noble
@date:  2016_07_25
'''

# }}}

from MDBtool  import *
from MDButils import *

class mdbindex(MDBtool):

    def __init__(self):
        super(mdbindex, self).__init__(version="0.2.0")

        cli = self.cli
        cli.description = 'Add one or more indexes to one or more collections '\
						  'in a MongoDB database,\nusing simple syntax from '\
                          'the *NIX CLI.\n\n'

        # Optional arguments
        cli.add_argument('-r', '--remove', action='store_true',
                    help='instead of adding the given index(es) to the '\
                    'collection, attempt to delete them if they exist')

        # Positional (required) arguments
        cli.add_argument('indexes',
                    help='One or more index expressions, each of the form:\n'\
                    '       collection_name:key[=direction][,key[=direction]...]'\
                    '\nDirection can be 1 or -1 (ASCENDING/DESCENDING), '\
                    'and defaults to 1 if not specified.  Use the | character '\
                    'to delimit multiple index expressions; if | or any white '\
                    'space appears in the indexes argument, enclose the entire '\
                    'entire argument in quotes.')

    def create_indexes(self, collection, index_terms):

        indexes = list()
        for iterm in index_terms:
            indexes.append( IndexModel( [iterm] ) )
            print "Adding index %s_%d to collection %s " \
                                    % (iterm[0], iterm[1], collection)

        self.db[collection].create_indexes(indexes)

    def remove_indexes(self, collection, index_terms):
        # Attempts to delete non-existent index/etc will be silently ignored
        for iterm in index_terms:
            print "Attempting to drop index %s_%d from collection %s" \
                                        % (iterm[0], iterm[1], collection)
            try:
                self.db[collection].drop_index([iterm])
            except Exception as e:
                pass

    def parse_index(self, keyvals):
        if not keyvals:
            return []
        index_terms = []
        for keyval in keyvals.split(','):
            key, _ , value = keyval.partition('=')
            if not value:
                value = "1"
            index_terms.append( ( key.strip(), int(value.strip()) ) )
        return index_terms

    def execute(self):
        super(mdbindex, self).execute()
        indexes = self.options.indexes

        if self.options.remove:
            index_operation = self.remove_indexes
        else:
            index_operation = self.create_indexes

        # Multiple indexes can be specified at CLI or in file, separated by |
        if os.path.isfile(indexes):
            indexes = open(indexes, 'rb').read().split('\n')
        else:
            indexes = indexes.split('|')

        for i in indexes:
            # Partition each index spec into Collection:key[=direction] [,key=[direction]...]
            i = i.split(':')
            if len(i) < 2:
                i.append('')

            collection = i[0]
            if collection not in self.collection_names:
                eprint('Skipping non-existing collection: '+collection)
                continue

            index_operation(collection, self.parse_index( i[1] ))

if __name__ == "__main__":
    mdbindex().execute()
