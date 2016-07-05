"""This is the "ghostsplitfile.py" module and it provide one function called split_file() which splits document by separator and prints."""

import os
def split_file( file_name, split_char=':' ):
    """
    This function takes one positional argument called "file_name", which is the local document to print.
    It takes another positional argument called "split_char", which is the separator to splits the document with default value ':'
    Each data item in the provided local document is (recursively) printed to the screen on it's own line.
    """
    #file_name = 'xxx\python\chapter3\sketch.txt'
    #split_char = ':'
    try:
        #os.chdir( 'xxx\python\chapter3' )
        data = open( file_name )
        data.seek( 0 ) 
        for each_line in data:
            print( each_line )
        try:
            ( role, line_spoken ) = each_line.split( split_char )
            print( role, end='' )
            print( ' said: ', end='' )
            print( line_spoken )
        except ValueError:
            pass
        data.close()    
    except IOError:
        print( 'The data file is missing!' )