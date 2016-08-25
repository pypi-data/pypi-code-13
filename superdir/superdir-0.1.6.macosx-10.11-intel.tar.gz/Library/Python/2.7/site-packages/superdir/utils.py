# -*- coding: utf-8 -*-

'''  
    Utility functions for superdir.py.  
'''

import datetime

import os
import sys

def is_empty(line):
    ''' Return True if line is equal to empty string after being stripped of 
    whitespace. Otherwise, return False.
    '''
    return line.strip() is ''

def is_comment(line):
    return line.strip().startswith('#')

def is_dir(line):
    return line.rstrip().endswith('/')

def is_multiple_of_indent(this_indent, global_indent):
    ''' Returns True if the current indent reaches 0 when the global 
    indent size is repeatedly subtracted from it. Otherwise returns False. 
    '''

    while this_indent > 0:
        this_indent -= global_indent

    return this_indent == 0

def clean(lines):
    ''' Discard all comments and lines with nothing or whitespace. ''' 

    return [ 
            line.rstrip() 
            for line in lines 
            if not ( is_empty(line) or is_comment(line) ) ]

def parse_indent(line):
    ''' Return the leading number of spaces in a line of text. '''

    return len(line) - len(line.lstrip())

def get_indent_count(line, indent_size):
    ''' Return the number of indentation units after dividing a line of 
    text's leading space count by some indent_size. 
    '''
    raw_indent = len(line) - len(line.lstrip())

    rv = None 

    try:
        rv = raw_indent / indent_size

    except ZeroDivisionError:
        rv = 0

    return rv
            
def get_dirname(line):
    ''' Remove all trailing forward slashes from a line after it's been 
    stripped. 
    '''

    return line.strip().rstrip('/')

def get_filename(line):
    ''' Return line with whitespace stripped. '''

    return line.strip()

def get_paths(output_dir):
    ''' Turn /path/to/output_dir into /path/to, output_dir. '''

    abs_cur_dir = os.path.abspath(os.curdir)
    full_base_path = None

    # absolute path example: /data/apps/new_app
    if output_dir.startswith('/'):
        abs_base_path = os.path.join('/', *output_dir.split('/')[:-1])
        output_dir = output_dir.split('/')[-1]

    # relative path with multiple dirs example: apps/new_app 
    else:
        if '/' in output_dir:
            abs_base_path = os.path.join( 
                abs_cur_dir, 
                '/'.join(output_dir.split('/')[:-1]) 
            )
            output_dir = output_dir.split('/')[-1]
        else:
            abs_base_path = abs_cur_dir 

    return abs_base_path, output_dir

def build_output_dirname(dir_suffix='SUPERDIR_OUTPUT', datestring=None):
    ''' Appends a current date in YYYY-MM-DD-HH-MM format to a directory 
    suffix. 
    '''

    if datestring is None:
        import datetime

        dt_now = datetime.datetime.now()
        year, month, day, hour, minute = dt_now.year,\
                                         dt_now.month,\
                                         dt_now.day,\
                                         dt_now.hour,\
                                         dt_now.minute

        datestring = '{}-{}-{}-{}-{}'.format(year, month, day, hour, minute)

    output_dirname = '{}-{}'.format(dir_suffix, datestring)

    return output_dirname

def usage(out=sys.stdout):
    ''' Print usage info. '''

    out.write('Usage: superdir SCHEMA_FILE [TARGET]\n')

def show_err_msg(out=sys.stdout, line_number=None, schema_lines=None):
    ''' Print an error message including the line number and the line. ''' 

    schema_lines[line_number] = schema_lines[line_number].rstrip() +\
                                '    <<< error'
    highlighted_schema = '\n'.join(schema_lines)
    out.write('Parse Error: inconsistent indentation in your schema file '\
              'on line {}\n{}\n'.format(line_number, highlighted_schema))
