from utils import parse_indent, is_empty, is_comment, is_dir, is_multiple_of_indent, clean

''' 
    Validates schema and returns indent size if valid, otherwise raises ValueError.

    Once an indent size N is determined, each indentation level must be:

        1) less than N by a multiple of N,  e.g. 8 -> 4 or 8 -> 0
        2) 0, or 
        3) preceded by a directory and greater than N by exactly N.
'''

class Validator():

    def __init__(self):

        self.indent = None
        self.schema = None
        self.indent_size = None

    def validate(self):

        indent, start_index = self._find_first_indent()

        prev_indent = indent
        prev_line = self.schema[start_index]
        for index, line in enumerate( self.schema[start_index + 1:] ):

            this_indent = parse_indent(line) 
            difference = this_indent - prev_indent

            if (difference == 0) or\
               (difference == indent and is_dir(prev_line)) or\
               (difference < 0 and is_multiple_of_indent(this_indent, indent)):
                prev_indent = this_indent
                continue
            else:
                self.raise_parse_error(line_number=(index + start_index + 1), line=line)

            prev_line = line

        self.indent_size = indent

    def load_schema(self, schema):

        self.schema = clean(schema)

    def get_indent_size(self):

        return self.indent_size

    def _find_first_indent(self):
        ''' returns indent_value, start_index '''

        indent, start_index = 0, 0 

        for index, line in enumerate(self.schema):
            if parse_indent(line) > 0:
                indent = parse_indent(line)
                break

        return indent, start_index
