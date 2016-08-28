from __future__ import with_statement
from __future__ import absolute_import
from __future__ import generators
from __future__ import nested_scopes
from __future__ import print_function
from __future__ import division

#The MIT License (MIT)
#Copyright (c) 2016 Sam Caldwell.
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to 
#deal in the Software without restriction, including without limitation the
#rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#sell copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#IN THE SOFTWARE.

import os
import sys
import time
import json
import inspect

class Config:
   
    def __init__(self,oName,is_file=False,i=0,debug_mode=False):
        self.debug_mode=debug_mode
        self.i=i
        self.type=None
        if is_file:
            self.oName="root"
            self.type="root"
        else:
            self.oName=oName
            self.type="child"

        self.debug("init {}[{}] starting".format(self.oName,self.type))

        if is_file:
            j=None
            try:
                with open(oName,'r') as f:
                    j=json.loads(f.read())

                self.debug(
                    "----Raw Input----\n\n{}\n".format(
                        json.dumps(j,indent=4)
                    )
                )
                self.deserialize(j,i+1)

            except Exception as e:
                self.debug("Could not load config file.  Error:{}".format(e))
                sys.exit(1)
            
        self.debug("init {}[{}] complete".format(self.oName,self.type))

    def deserialize(self,j,i=0):
        self.i=i
        try:
            self.debug(" ")
            self.debug("---deserializer loop started")
            self.debug("+>json:{}".format(j))
            for k,v in j.viewitems():
                self.debug("calling walk() with '{}'".format(k))
                self.walk(k,v,i+1)
                self.debug("returned from walk() '{}'".format(k))
            self.debug("---deserializer loop complete.")

        except Exception as e:
            self.debug("Could not deserialize config. Error:".format(e))
            sys.exit(1)
        self.i-=1

    def walk(self,key_name,key_value,i=1):
        self.i=i
        self.debug("walking the config:{}".format(i))
        try:
            o=None
            if type(key_value) is dict:
                o=Config(oName=key_name,i=i)
                o.deserialize(key_value,i+1)
                self.debug("walk(): recovered from recursive call.")
                assert key_name != "oName", "oName is reserved for parser"
                setattr(self,key_name,o)
            else:
                self.debug("Set value:{},{}".format(key_name,key_value))
                assert key_name != "oName", "oName is reserved for parser"
                setattr(self,key_name,key_value)

        except Exception as e:
            self.debug("config.walk() Error:{}".format(e))
            sys.exit(1)
        self.i-=1

    def dump_config(self,i=0,data_only=False):
        old_debug_mode=self.debug_mode
        self.debug_mode=True
        self.i=i
        if i == 0:
            c="*"
        else:
            c="-"
        self.debug("{0}DUMP CONFIG START ({1}:{2}){0}".format(c*3,self.type,self.oName))
        for k in dir(self):
            if data_only and \
               not k.startswith("_") and \
               not callable(getattr(self,k)):
                self.debug("{0:15}:{1}".format(k,getattr(self,k)))
            if isinstance(getattr(self,k),Config):
                self.i+=1
                o=getattr(self,k)
                o.dump_config(self.i+1,data_only)
                self.i-=1
        self.debug("{0}DUMP CONFIG ENDS ({1}:{2}){0}".format(c*3,self.type,self.oName))
        self.debug_mode=old_debug_mode

    def debug(self,m):
        try:
            if self.debug_mode:
                print(
                    "{0:15}|{1:<2}| {2} [{3}]:{4}".format(
                        int(time.time()*10000000000),
                        hex(self.i),
                        " . "*self.i,
                        self.oName,
                        m
                    )
                )
        except Exception as e:
            print("Could not print message: Error:{}".format(e))
            sys.exit(1)

    def getChildAttribute(self,index,object,path):
        self.i+=1
        assert isinstance(self,Config),"self must be <instance>"
        assert type(index) is int, "index must be <int>"
        assert isinstance(object,Config),"object must be <instance>"
        assert type(path) is list, "path must be <list>"
        for i in path: 
            assert type(i) in [str,unicode], "path elements must be <str>"
        assert index >= 0, "index must be > 0"
        assert len(path) > 0, "len(path <list>) must be > 0"

        self.debug("position[{}]:{}".format(index,path[index]))

        o=getattr(object,path[index])
        if (index < len(path)) and isinstance(o,Config):
            return self.getChildAttribute(index+1,o,path)
        else:
            return o
        self.i-=1



    def read_value(self,k):
        if self.debug_mode:self.dump_config(data_only=True)
        self.i=0
        try:
            path=k.split('.')
            self.debug("path: {}".format(path))
            o=getattr(self,path[0])
            self.debug("o:{}:{}".format(o,o.oName))
            return 0, self.getChildAttribute(
                                    index=1,
                                    object=o,
                                    path=path
            )
        except Exception as e:
            return 1,e



    def write_value(self,k,v):
        """
        What we need here...
            (1) assume k is a path in . notation to a value
            (2) we need to walk that path and--
                (a) If a branch of the path does not exist, create a node.
                (b) If a branch of the path does exist, walk further.
                (c) When the end of the path is reached, set value
        """
        try:
            assert k is not None, "Expected a key string (--key)"
            assert v is not None, "Expected a value string (--value)"
            assert type(k) is str, "--key must specify a string."
            assert type(v) is str, "--value must specify a string."
        except Exception as e:
            print("Error: {}".format(e))
            sys.exit(1)

        try:
            print("write_value() not implemented yet.")
        except Exception as e:
            print("write_value() Error: {}".format(e))
            sys.exit(1)
