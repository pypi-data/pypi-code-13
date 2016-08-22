from __future__ import print_function 
import os
import sys
import imp
import fnmatch
import getpass
from Crypto.Cipher import AES

__all__ = [
    "Abstractor"
]

class Abstractor(object):
    def __init__(self):
        self.path = "."
        self.passphrase = "PROJECT@ENC@1234"
        self.ext = ".enc"

    def set_passphrase(self,passphrase):
        self.passphrase = passphrase

    def set_path(self,path):
        self.path = path

    def set_extention(self,ext):
        self.ext = ext

    def setup(self):
        print("Enter path of project root directory(default: .): ", end="")
        inp = raw_input()
        if inp:self.path = inp
        inp = getpass.getpass("Enter passphrase(default: PROJECT@ENC@1234)(16/24/32 characters): ")
        if len(inp)<16:
            inp = ""
        else:
            inp = inp[:-(len(inp)%8)]

        if inp:self.passphrase = inp
        print("Enter file extention(default .enc): ", end="")
        inp = raw_input()
        if inp:self.ext = inp
        

    def encrypt(self):
        obj = AES.new(self.passphrase, AES.MODE_ECB, 'This is an IV456')
        for i in os.walk(self.path):
            for j in fnmatch.filter(i[2],"*.py"):
                fin = open(i[0]+'/'+j,'r')
                data = fin.read()
                data = data + " "*(16-len(data)%16)
                fin.close()
                fout = open(i[0]+'/'+j[:-3]+self.ext,'w')
                enc_data = obj.encrypt(data)
                fout.write(enc_data)
                fout.close()
                os.remove(i[0]+'/'+j)
                

    def decrypt(self):
        obj = AES.new(self.passphrase, AES.MODE_ECB, 'This is an IV456')
        for i in os.walk(self.path):
            for j in fnmatch.filter(i[2],"*.enc"):
                fin = open(i[0]+'/'+j,'r')
                data = fin.read()
                data = data + " "*(16-len(data)%16)
                fin.close()
                fout = open(i[0]+'/'+j[:-4]+'.py','w')
                dec_data = obj.decrypt(data)
                fout.write(dec_data)
                fout.close()
                os.remove(i[0]+'/'+j)

    def decrypt_import(self,mpath,objects = ""):
        obj = AES.new(self.passphrase, AES.MODE_ECB, 'This is an IV456')
        filepath = mpath.replace('.','/')
        fin = open(filepath+".enc")
        data = fin.read()
        fin.close()
        dec_data = obj.decrypt(data)
        module_name = mpath.split('.')[-1]
        thismodule = sys.modules[__name__]
        setattr(thismodule,module_name,imp.new_module(module_name))
        x = getattr(thismodule,module_name)
        exec dec_data in x.__dict__
        sys.modules[module_name] = x
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

