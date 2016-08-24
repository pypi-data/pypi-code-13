class_def = """from __future__ import print_function 
import os
import sys
import imp
import pickle
from Crypto.Cipher import AES

class Importer(object):
    def __init__(self):
        pass
    def __run__(self):
        project_path = "#############change project path#############"
        passphrase_for_encryption__ = "#############encryption passphrase#############"
        extn = "#############.extention#############"
        def decrypt_import(mpath):
            obj = AES.new(passphrase_for_encryption, AES.MODE_ECB, 'This is an IV456')
            filepath = mpath.replace('.','/')
            fin = open(self.__path+'/'+filepath+extn)
            data = fin.read()
            fin.close()
            dec_data = obj.decrypt(data)
            module_name = mpath.split('.')[-1]
            thismodule = sys.modules[__name__]
            setattr(thismodule,module_name,imp.new_module(module_name))
            x = getattr(thismodule,module_name)
            exec dec_data in x.__dict__
            sys.modules[mpath] = x
        
        # Enter import statements here
        # eg. decrypt_model("lib.utils")
        #     this will load project_path/lib/utils.py
        #     it can be accessed as lib.utils
        #     eg. from lib.utils import function
        
        
        self.__dict__ = {}
"""