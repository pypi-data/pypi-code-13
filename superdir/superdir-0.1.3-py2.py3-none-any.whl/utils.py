import datetime

import os
import sys


'''  
    Utility functions for superdir.py.  
'''

def usage(out=sys.stdout):
    out.write('Usage: superdir SCHEMA_FILE [TARGET]\n')

def clean(lines):
    return [ line.rstrip() for line in lines if not is_empty(line) and not is_comment(line) ] 

def is_empty(line):
    return line.strip() is ''

def is_comment(line):
    return line.strip().startswith('#')

def is_dir(line):
    return line.rstrip().endswith('/')

def is_multiple_of_indent(this_indent, global_indent):
    ''' Returns True if the current indent reaches 0 when the global indent size is repeatedly subtracted from it. Otherwise returns False. '''

    while this_indent > 0:
        this_indent -= global_indent

    return this_indent == 0

def parse_indent(line):
    ''' Return the leading number of spaces in a line of text. '''
    return len(line) - len(line.lstrip())

def get_indent(line, indent_size):
    ''' Return the number of indentation units after dividing a line of text's leading space count by some indent_size. '''
    raw_indent = len(line) - len(line.lstrip())

    rv = None 

    try:
        rv = raw_indent / indent_size

    except ZeroDivisionError:
        rv = 0

    return rv
            
def get_dirname(line):
    ''' Remove all trailing forward slashes from a line after it's been stripped. '''

    return line.strip().rstrip('/')

def get_filename(line):
    ''' return line with whitespace stripped. '''

    return line.strip()

def handle_args(args):

    #
    #  Provisional argument handling to be replaced by click.
    #
    #  Usage: superdir SCHEMA [OUTPUT_DIR]
    #

    # Check for stdin pipe here
    
    schema_file = None
    output_dir = None
    abs_base_path = None

    if len(args) < 2:
        usage()
        sys.exit(1)

    if len(args) == 2:
        schema_file = args[1] 

        dt_now = datetime.datetime.now()
        date_string = str(dt_now) 
        date_label = date_string.split(' ')[0]
        output_dir = 'SUPERDIR_OUTPUT_{}'.format(date_label)
        output_dir, abs_base_path = get_paths(output_dir)

    if len(args) > 2:

        if os.path.isdir(args[2]):
            print ("An error has occurred: the output directory '{}' exists. In order to run superdir successfully, \n"
            "either rename your output directory or rename the currently directory with the name you've supplied.").format(output_dir)
            usage()
            sys.exit(1) 

        else:
            schema_file = args[1]
            output_dir = args[2]
            output_dir, abs_base_path = get_paths(output_dir)

    return schema_file, output_dir, abs_base_path

def get_paths(output_dir):
    ''' Takes the output directory and breaks it into the relative directory name and the base path/starting point for the traversal 

    ABSOLUTE:

        original output_dir = /data/apps/new_app 

        output_dir = new_app 
        full_base_path = /data/apps

    RELATIVE WITH MULTIPLE LEVELS:

        original output_dir = apps/new_app 

        output_dir = new_app 
        full_base_path = cwd() + '/' + apps/

    RELATIVE WITH A SINGLE LEVEL:

        original_output_dir = new_app

        output_dir = new_app 
        full_base_path = cwd() 

    '''

    abs_cur_dir = os.path.abspath(os.curdir)
    full_base_path = None

    # absolute path example: /data/apps/new_app
    if output_dir.startswith('/'):
        abs_base_path = os.path.join('/', *output_dir.split('/')[:-1])
        output_dir = output_dir.split('/')[-1]

    # relative path with multiple dirs example: apps/new_app 
    else:
        if '/' in output_dir:
            abs_base_path = os.path.join( abs_cur_dir, '/'.join(output_dir.split('/')[:-1]) )
            output_dir = output_dir.split('/')[-1]
        else:
            abs_base_path = abs_cur_dir 

    return output_dir, abs_base_path
