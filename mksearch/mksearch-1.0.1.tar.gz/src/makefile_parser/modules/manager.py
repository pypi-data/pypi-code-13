'''
Created on Jul 28, 2016

@author: iitow
'''
import os
import sys
import re
import json
from goephor.version import string

class Manager(object):
    ''' Represents a management singleton
    '''
    def __init__(self,options):
        ''' 
        Manager Constructor
        
        :param options: argarse obj
        '''
        self.options = options
        self.options.path
        self.mk_objs = []
        self.main()
        if self.options.debug:
            self.pprint()
    
    def pprint(self,title='loaded'):
        '''
        Pretty print out makefiles
        
        :param title: String
        '''
        for mk_obj in self.mk_objs:
            self._pprint(mk_obj,title=title)
    
    def _pprint(self,mk_obj,title='loaded'):
        '''
        Private, Pretty print out makefiles
        
        :param mk_obj: Object, Makfile
        :param title: String
        '''
        print "***************************************"
        print "\n\n[%s] @ %s" % (title,mk_obj.file_ext)
        print "\n[comments]"
        comments =  mk_obj.info.get('comments')
        print comments
        print "\n[includes]"
        includes =  mk_obj.info.get('includes')
        for value in includes:
            print "     - %s" % (value)
        print "\n[variables]"
        variables =  mk_obj.info.get('variables')
        for key,value in variables.iteritems():
            print "%s" % (key)
            for val in value:
                print "     - %s" % (val)

    def _walk(self,path,includes=[]):
        ''' performs scan on all files
        :param path: String
        :param excludes: List, list of excludes
        '''
        paths = []
        for root, directories, filenames in os.walk(path):
            for filename in filenames:
                root = root.replace(path,'')
                filepath =  "%s/%s" % (root, filename)
                if includes:
                    if self._is_include(filepath):
                        paths.append(filepath)
                    else:
                        pass
                else:
                    paths.append(filepath)
        return paths

    def _is_include(self,filepath):
        '''
        Check for includes in given file name
        :param filepath: String
        '''
        for include in self.options.include:
            if include in filepath:
                return True
        return False
    
    def _write(self,data):
        '''
        writes json file
        :param data: Dict
        '''
        path = "%s/%s" % (os.getcwd(),self.options.json)
        print "[results] @ %s" % path
        with open(path, 'w') as file:
            file.write(json.dumps(data,
                      indent=4,
                      sort_keys=True))

    def main(self):
        '''
        main entry point of class
        '''
        makefiles = self._walk(self.options.path, self.options.include)
        for makefile in makefiles:
            mk_obj = Makefile(self.options.path,makefile,self.options)
            self.mk_objs.append(mk_obj)
        if self.options.search:
            mkfiles = self.find_matches()
            if self.options.json and mkfiles:
                self._write(mkfiles)

    def find_matches(self):
        '''
        Find matches in a given makefile
        '''
        matches = []
        for s in self.options.search:
            for mk_obj in self.mk_objs:
                found = str(self.traverse(mk_obj.info, s))
                if s in found:
                    if self.options.debug:
                        self._pprint(mk_obj,title='found')
                    else:
                        print "[found] @ %s" % (mk_obj.file_ext)
                        matches.append(mk_obj.info)
        if matches:
            return matches
        return None
    def traverse(self,data, key):
        '''
        Private recursively traverse nested json data
        :param data: Nested dict/list
        :param key: String
        :return: value
        '''
        values=[]
        if isinstance(data, list):
            for items in data:
                value = self.traverse(items, key)
                values.append(value)
            return values
        elif isinstance(data, dict):
            for k, v in data.iteritems():
                if key in k:
                    return str(v)                
                elif  isinstance(v, dict):
                    value = self.traverse(v, key)
                    values.append(value)
                elif isinstance(v, list):
                    for q in v:
                        if key in q:
                            return str(q)
                    value = self.traverse(v, key)
                    values.append(value) 
            return values
        else:
            if values:
                return values

class Makefile(object):
    '''
    Represents a Makefile
    '''
    def __init__(self,base_path,file_ext,options):
        '''
        Makefile Constructor
        
        :param base_path: String
        :param file_ext: String
        :param options: Object, argparse
        '''
        self.options = options
        self.base_path = base_path
        self.file_ext = file_ext
        self.filepath = "%s/%s" % (self.base_path,self.file_ext)
        self.raw = self._reader(self.filepath)
        self.includes = None
        self.comments = None
        self.variables = None
        self.info = self._parse()

    def _reader(self,filepath):
        '''
        Private, file reader
        
        :param filepath: String
        '''
        with open(self.filepath) as fp:
            return fp.read()

    def _parse(self):
        '''
        Private, add all parsing here
        '''
        info = {'filepath':self.file_ext}
        syntax = Syntax(self.raw,self.filepath,self.options)
        self.includes = syntax.includes_are(self.raw)
        info['includes'] = self.includes
        self.comments = syntax.comments_are(self.raw)
        info['comments'] = self.comments
        self.variables = syntax.variables_are(self.raw)
        info['variables'] = self.variables
        return info

class Syntax(object):
    '''
    This class is used to find elements in a makefile
    '''
    def __init__(self,raw,filepath,options):
        '''
        Syntax constructor
        
        :param raw: String
        :param filepath: String
        :param options: Object, argparse
        '''
        self.options = options
        self.filepath = filepath
        self.raw =raw

    def includes_are(self,raw):
        '''
        Grab includes from makefile regex
        
        :param raw: String
        '''
        matches = re.findall(r'(?<=\.include).*', raw)
        return matches

    def comments_are(self,raw):
        '''
        Grab comments from makefile regex
        
        :param raw: String
        '''
        matches = re.findall(r'\s*#(.*)\s*#(.*)|#(.*)[^#]*',raw,re.MULTILINE)
        comment = " "
        for match in matches: 
            comment = "%s\n%s" % (comment,"\n".join(match))
            comment = comment.replace("#",'')
        return comment

    def _variables_are(self,raw):
        '''
        Private, Grab all variables from makefile regex
        
        :param raw: String
        '''
        regex = r'([^\s=]+=)(.*)|([^\s=]+=)?(.*\\\n)|((?<=\\\n).*)'
        matches = re.findall(regex,raw,re.MULTILINE)
        for match in matches:
            yield match

    def variables_are(self,raw):
        '''
        Grab all variables from makefile, transforms tuples to dict
        
        :param raw: String
        '''
        variables = {}
        matches = self._variables_are(raw)
        previous = None
        while True:
            try:
                new = matches.next()
            except:
                break
            if not new[0]=='' and '#' not in new[0]:
                previous = str(new[0]).strip()
                if variables.has_key(previous):
                    val1 = new[1].replace('\\','').strip()
                    variables[previous].append(val1)
                else:
                    val1 = new[1].replace('\\','').strip()
                    variables[previous]=[val1]
            else:
                if not new[3] == '' and ':' not in new[3] and not previous == None:
                    val3 = new[3].replace('\\','').strip()
                    variables[previous].append(val3)
                if not new[4] == '' and not previous == None:
                    val4 = new[4].replace('\\','').strip()
                    variables[previous].append(val4)
        return variables
