# -*- coding: utf-8 -*-

import sys
import utils

class Validator():

    def __init__(self, schema, OUTPUT_DIR=None):
        ''' Bind array of cleaned schema file lines to validator object. ''' 

        self.schema = utils.clean(schema)
        self.OUTPUT_DIR = OUTPUT_DIR
        self.INDENT_SIZE = self._find_first_indent()['indent_size']
        self.error = {'msg': None}

    def validate(self):
        ''' Return True if schema is valid, otherwise return False. '''

        if not len(self.schema): 
            self.error['msg'] = 'Error: empty schema file.'
            return False

        start_index = self._find_first_indent()['index']
        prev_line = self.schema[start_index]
        prev_indent = self.INDENT_SIZE

        schema_is_valid = True

        lines_to_validate = self.schema[start_index + 1:]
        for index, this_line in enumerate( lines_to_validate ):

            this_indent = utils.parse_indent(this_line)
            if not self._line_is_valid(this_line, prev_line, this_indent, prev_indent):

                self.error['msg'] = 'Error in schema file on line {}'.format((index + start_index + 1))
                schema_is_valid = False
                break

            prev_indent = this_indent
            prev_line = this_line


        if not self._top_dir_is_valid(self.OUTPUT_DIR):
            self.error['msg'] = 'Error regarding top-level directory rules. See superdir --help for usage.'
            schema_is_valid = False

        return schema_is_valid


    def _line_is_valid(self, this_line, prev_line, this_indent, prev_indent):
        '''
        Once the first indent size is determined, each subsequent
        indent must be:

            1) less than N by a multiple of N,  e.g. 8 -> 4 or 8 -> 0
            2) 0, or 
            3) preceded by a directory and greater than N by exactly N.
        '''

        difference = this_indent - prev_indent

        return  (difference == 0) or\
                (difference == self.INDENT_SIZE and utils.is_dir(prev_line)) or\
                (difference < 0 and utils.is_multiple_of_indent(this_indent, self.INDENT_SIZE)) 


    def _top_dir_is_valid(self, OUTPUT_DIR):
        ''' Return True only if output dir is supplied or schema file has exactly 1 top-level directory and no siblings '''

        indents = [ utils.parse_indent(line) for line in self.schema ]
        min_indent_count = indents.count( min(indents) ) 

        return OUTPUT_DIR is not None or min_indent_count == 1 

    def _find_first_indent(self):
        ''' Returns indent_value, start_index of first indent. '''

        indent_size, start_index = 0, 0 

        for index, line in enumerate(self.schema):
            if utils.parse_indent(line) > 0:
                indent_size = utils.parse_indent(line)
                start_index = index
                break

        return dict(indent_size=indent_size, index=start_index)
