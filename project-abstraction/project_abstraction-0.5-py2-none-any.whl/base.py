from __future__ import print_function 
import os
import sys
import imp
import fnmatch
import getpass
import string
from Crypto.Cipher import AES
import dill as pickle
import sample

__all__ = [
    "Abstractor"
]

class Abstractor(object):
    def __init__(self,project_path = '.',passphrase = "PROJECT@ENC@1234",passphrase2 = "PROJECT@ENC@1234",extn = '.enc'):
        self.__path = project_path
        self.__passphrase_for_encryption__ = passphrase
        self.__passphrase_for_storing__ = passphrase2
        self.__extn = ".enc"

    def set_param(self,project_path = '',passphrase = "",passphrase2 = "",extn = ''):
        if project_path:
            self.__path = project_path
        if passphrase:
            self.__passphrase_for_encryption__ = passphrase
        if passphrase2:
            self.__passphrase_for_storing__ = passphrase2
        if extn:
            self.__extn = ".enc"

    def setup(self):
        print("Enter path of project root directory(default: .): ", end="")
        inp = raw_input()
        if inp:self.__path = inp
        inp = getpass.getpass("Enter passphrase(default: PROJECT@ENC@1234)(16/24/32 characters): ")
        if len(inp)<16:
            inp = ""
        else:
            inp = inp[:-(len(inp)%8)]

        inp = getpass.getpass("Enter passphrase for storing(default: PROJECT@ENC@1234)(16/24/32 characters): ")
        if len(inp)<16:
            inp = ""
        else:
            inp = inp[:-(len(inp)%8)]

        if inp:self.__passphrase_for_encryption__ = inp
        print("Enter file extention(default .enc): ", end="")
        inp = raw_input()
        if inp:self.__extn = inp
        

    def encrypt(self):
        obj = AES.new(self.__passphrase_for_encryption__, AES.MODE_ECB, 'This is an IV456')
        for i in os.walk(self.__path):
            for j in fnmatch.filter(i[2],"*.py"):
                fin = open(i[0]+'/'+j,'r')
                data = fin.read()
                data = data + " "*(16-len(data)%16)
                fin.close()
                fout = open(i[0]+'/'+j[:-3]+self.__extn,'w')
                enc_data = obj.encrypt(data)
                fout.write(enc_data)
                fout.close()
                os.remove(i[0]+'/'+j)

    def encrypt_one(self,mpath='',delete_file=False):
        obj = AES.new(self.__passphrase_for_encryption__, AES.MODE_ECB, 'This is an IV456')
        if mpath:
            fin = open(mpath,'r')
            data = fin.read()
            data = data + " "*(16-len(data)%16)
            fin.close()
            fout = open(mpath[:-3]+self.__extn,'w')
            enc_data = obj.encrypt(data)
            fout.write(enc_data)
            fout.close()
            if delete_file:
                os.remove(mpath)
                

    def decrypt(self):
        obj = AES.new(self.__passphrase_for_encryption__, AES.MODE_ECB, 'This is an IV456')
        for i in os.walk(self.__path):
            for j in fnmatch.filter(i[2],"*"+self.__extn):
                fin = open(i[0]+'/'+j,'r')
                data = fin.read()
                # data = data + " "*(16-len(data)%16)
                fin.close()
                fout = open(i[0]+'/'+j[:-4]+'.py','w')
                dec_data = obj.decrypt(data)
                fout.write(dec_data)
                fout.close()
                os.remove(i[0]+'/'+j)

    def decrypt_one(self,mpath='',delete_file=False):
        obj = AES.new(self.__passphrase_for_encryption__, AES.MODE_ECB, 'This is an IV456')
        if mpath:
            fin = open(mpath,'r')
            data = fin.read()
            fin.close()
            fout = open(mpath.replace(self.__extn,'.py'),'w')
            dec_data = obj.decrypt(data)
            fout.write(dec_data)
            fout.close()
            if delete_file:
                os.remove(mpath)

    def decrypt_import(self,mpath,objects = ""):
        obj = AES.new(self.__passphrase_for_encryption__, AES.MODE_ECB, 'This is an IV456')
        filepath = mpath.replace('.','/')
        fin = open(self.__path+'/'+filepath+self.__extn)
        data = fin.read()
        fin.close()
        dec_data = obj.decrypt(data)
        module_name = mpath.split('.')[-1]
        thismodule = sys.modules[__name__]
        setattr(thismodule,module_name,imp.new_module(module_name))
        x = getattr(thismodule,module_name)
        exec dec_data in x.__dict__
        sys.modules[mpath] = x
        if objects:
            if isinstance(objects,list):
                out = []
                for i in objects:
                    attr = getattr(x,i)
                    out.append(attr)
            elif isinstance(objects,str):
                out = getattr(x,objects)
        else:
            out = x
        return out

    def create_class(self):
        x = sample.class_def
        x = string.replace(x,"#############encryption passphrase#############",self.__passphrase_for_encryption__)
        x = string.replace(x,"#############change project path#############",self.__path)
        x = string.replace(x,"#############.extention#############",self.__extn)
        f = open(self.__path+"/prjkt_bstrctn_class.py","w")
        f.write(x)
        f.close()

    def create_enc_pickle(self,filename="",newfilename=''):
        if not filename:
            obj = AES.new(self.__passphrase_for_storing__, AES.MODE_ECB, 'This is an IV456')
            foo = imp.load_source("__main__", self.__path+"/prjkt_bstrctn_class.py")
            # f = open(self.__path+"/prjkt_bstrctn_class.py",'r')
            # data  = f.read()
            # f.close()
            # x = imp.new_module("x")
            # exec data in x.__dict__
            x = foo.Importer()
            data = pickle.dumps(x)
            data = data + " "*(16-len(data)%16)
            enc_data = obj.encrypt(data)
            if not newfilename:
                f = open(self.__path+"/ncrytd_dcrptr_class.pkl",'wb')
                f.write(enc_data)
                f.close()
            else:
                f = open(self.__path+"/"+newfilename,'wb')
                f.write(enc_data)
                f.close()
            del foo
        else:
            obj = AES.new(self.__passphrase_for_storing__, AES.MODE_ECB, 'This is an IV456')
            f = open(self.__path+"/"+filename,'r')
            data  = f.read()
            enc_data = obj.encrypt(data)
            f.close()
            if not newfilename:
                f = open(self.__path+"/ncrytd_dcrptr_class.pkl",'wb')
                f.write(enc_data)
                f.close()
            else:
                f = open(self.__path+"/"+newfilename,'wb')
                f.write(enc_data)
                f.close()

    def load_enc_pickle(self,loading_module='sample',filename="",run = False):
        obj = AES.new(self.__passphrase_for_storing__, AES.MODE_ECB, 'This is an IV456')
        if not filename:
            fin = open(self.__path+"/ncrytd_dcrptr_class.pkl",'rb')
            data = fin.read()
            fin.close()
            dec_data = obj.decrypt(data)
            # l_module =  imp.new_module(loading_module)
            # sys.modules[loading_module] = l_module

            # setattr(l_module,"Importer",type('Importer', (object,), {})())
            x = pickle.loads(dec_data.rstrip())
            if run:
                x.__run__()
            else:
                return x
        else:
            fin = open(self.__path+"/"+filename,'rb')
            data = fin.read()
            fin.close()
            dec_data = obj.decrypt(data)
            x = pickle.loads(dec_data.rstrip())
            if run:
                x.__run__()
            else:
                return x
