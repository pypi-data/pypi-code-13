'''
Created on Jun 3, 2016

:author: iitow
'''
import sys
import time
from signal import signal, SIGPIPE, SIG_DFL 
def colors(color_type,output):
    '''
    Types of colors to display
    '''
    types = {'header': '\033[1m\033[34m',
              'info': '\033[34m',
              'success': '\033[32m',
              'warning': '\033[33m',
              'fail': '\033[31m',
              'error': '\033[31m',
              'end': '\033[0m'}
    trans = types.get(color_type,None)
    if not output:
        output = ""
    output = trans+str(output)+types.get('end')
    return output
    
def message(message_type,output,debug=False):
    '''
    Display a colorized message
    :param message_type: String, header, info, success, warning, fail, error
    :param output: String
    :return: colorized string
    '''
    try:
        if debug:
            with open("DEBUG.log", "a") as debug:
                output_str = "# %s\n" % (output)
                debug.write(output_str)
        output_final = colors(message_type,output)
        #sys.stdout.flush()
    except Exception as e:
        pass
    return output_final
