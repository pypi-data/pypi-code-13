class_def = """import os
import sys
import imp
import fnmatch
from Crypto.Cipher import AES

class Importer(object):
    def __init__(self):
        pass
    def __run__(self):
        import os
        import sys
        import imp
        import fnmatch
        from Crypto.Cipher import AES
        project_path = "#############change project path#############"
        passphrase_for_encryption__ = "#############encryption passphrase#############"
        extn = "#############.extention#############"
        def decrypt_import(mpath):
            obj = AES.new(passphrase_for_encryption, AES.MODE_ECB, 'This is an IV456')
            filepath = mpath.replace('.','/')
            fin = open(project_path+'/'+filepath+extn)
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
        # eg. decrypt_import("lib.utils")
        #     this will load project_path/lib/utils.py
        #     it can be accessed as lib.utils
        #     eg. from lib.utils import function
        
        #For loading all files open below code
        #for i in os.walk(project_path):
        #    for j in fnmatch.filter(i[2],"*"+extn):
        #        file_name = (i[0]+'/'+j.replace(extn,'')).replace('/','.')
        #        try:
        #            decrypt_import(file_name)
        #        except Exception, e:
        #            pass
        
        self.__dict__ = {}
"""