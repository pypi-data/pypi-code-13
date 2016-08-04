'''
Created on May 2, 2016

:author: iitow
'''
import ast
import os
import re
import sys
from data import File,Data

        
class Scanner(object):
    ''' scans all python files for attributes
    '''
    def __init__(self,base_path,file,output):
        ''' Scanner Constructor
        :param base_path: String, base of git repo
        :param file: String, to be parsed
        :param output: String, place to put README.md
        '''
        self.base_path = base_path
        self.file = file
        self.output = output
        self.handle = self.get_ast()
        self.examples = []

    def get_ast(self):
        ''' Get ast obj tree
        '''
        with open(self.file, 'r') as f:
            data  = f.read()
        return ast.parse(data)
    
    def _scan(self):
        ''' Performs the scan & adds markdown
        '''
        filename = self.file.rsplit(self.base_path,1)[1]
        text = ast.get_docstring(self.handle)
        fileObj = File(filename,text)
        for node in ast.walk(self.handle):
            if isinstance(node,ast.ClassDef):
                type = 'class'
                name = node.name
                doc = ast.get_docstring(node)
                fields = ast.iter_fields(node)
                classObj = Data(type,name,doc,fields)
                fileObj.add_data(classObj)
            if isinstance(node,ast.FunctionDef):
                type = 'def'
                name = node.name
                doc = ast.get_docstring(node)
                fields = ast.iter_fields(node)
                defObj = Data(type,name,doc,fields)
                fileObj.add_data(defObj)
        return fileObj
    
    def bold(self, line,regex=r'(?<=:)[^:\n]*'):
        ''' Bolds params and attribs
        :param line: String
        :param: regex: raw String
        '''
        if isinstance(line,str):
            matches = re.findall(regex, line)
            for match in matches:
                old = ':%s:' % match
                new = '\n**:%s:**' % (match)
                if new:
                    line = line.replace(old, new)
        return line