'''
Created on Jul 28, 2016

@author: iitow
'''
import re
   
def divider():
    '''
    Represents a markdown divider
    '''
    output = "**********************************************"
    return output

def header(size,input):
    '''
    Represents a header
    '''
    h = ""
    for c in range(0,size):
        h = "%s%s" % (h,'#')
    output = "%s%s%s" % (h,input,h)
    return output

def bold(input):
    ''' Bolds 
    '''
    output = "***%s***" % (input)
    return output

def inline(input):
    ''' Bolds 
    '''
    output = "\n```\n%s\n```\n" % (input)
    return output

def bold_regex(text,regex=r'(?<=:)[^:\n]*'):
    ''' Bolds params and attribs
    :param line: String
    :param: regex: raw String
    '''
    if isinstance(text,str):
        matches = re.findall(regex, text, re.DOTALL)
        for match in matches:
            old = ':%s:' % match
            new = '\n**:%s:**' % (match)
            if new:
                text = text.replace(old, new)
    return text



        