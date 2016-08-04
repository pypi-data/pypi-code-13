'''
Created on Jul 28, 2016

@author: iitow
'''
import re
from __builtin__ import str

class File(object):
    '''
    Represents a python file
    '''
    def __init__(self,name, doc):
        '''
        Constructor
        '''
        self.name = name
        self.doc = doc
        self.data = []

    def add_data(self,dataObj):
        self.data.append(dataObj)

class Data(object):
    '''
    Represents classes, defs of a python file
    '''
    def __init__(self, type, name, doc, fields):
        '''
        Constructor
        '''
        self.type = type
        self.name = name
        self.doc = doc
        self.fields = fields
        self.tags = self.get_tags(self.doc)
        self.example = self._get_example(doc)
    
    def get_tags(self,doc):
        tags = []
        if doc:
            for line in doc.split("\n"):
                if line:
                    tag = self._get_tags(line)
                    if tag:
                        tags.append(tag)
        if tags:
            return tags
            
    
    def _get_tags(self, line,regex=r'(?<=:)[^:\n]*'):
        ''' Bolds params and attribs
        :param line: String
        :param: regex: raw String
        '''
        if isinstance(line,str):
            if not ':example:' in line:
                matches = re.findall(regex, line)
                try:
                    return matches
                except:
                    return None
            else:
                return None
    
    def _get_example(self, text,regex=r"`(.*?)\s(.*?)`"):
        ''' Bolds params and attribs
        :param line: String
        :param: regex: raw String
        '''
        example = None
        if isinstance(text,str):
            matches = re.findall(r"`(.*?)\s(.*?)\s`", text, re.DOTALL)
            try:
                if matches[0][1]:
                    example = [self.name,matches[0][1]]
            except:
                return None
        return example
                    
                    
        
