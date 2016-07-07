#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import packages
from sys import exit
from os import chmod, remove, rename, getcwd, chdir, makedirs, walk, environ, chown, system
from os.path import abspath, dirname, join, isdir, isfile, exists, basename, splitext, relpath
from shutil import copyfile, copytree, rmtree, copy2
from tarfile import open
from pwd import getpwnam
from grp import getgrnam
from subprocess import Popen, PIPE
from re import compile, search
from platform import system as p_system
from zipfile import ZipFile, ZIP_DEFLATED
from debugger import Debugger

class Utils():
    def __init__(self):
        self.d = Debugger(self.get_env("RK_DEBUG"))

        self.path_list = []

    def get_current(self, file_path):
        return abspath(dirname(file_path))

    def exit(self):
        exit()

    def command(self, cmd):
        self.d.log("command: %s" % (cmd))
        system(cmd)

    def pushd(self, path):
        self.path_list.append(getcwd())
        chdir(path)
        self.d.log("pushd < %s" % (path))

    def popd(self):
        last_idx = len(self.path_list) - 1
        chdir(self.path_list[last_idx])
        self.d.log("popd > %s" % (self.path_list[last_idx]))
        del self.path_list[last_idx]

    def isfile(self, path):
        return isfile(path)

    def isdir(self, path):
        return isdir(path)

    def exists(self, path):
        return exists(path)

    def abspath(self, path):
        return abspath(path)

    def dirname(self, path):
        return dirname(path)

    def basename(self, path):
        return basename(path)

    def join_dirs(self, path_list):
        path = ""
        for idx in range(len(path_list)):
            path = join(path, path_list[idx])
        return path

    def get_env(self, key):
        return environ.get(key)

    def is_root(self):
        return (self.get_env("USER") == "root")

    def get_platform(self):
        p = p_system()
        if (p == "Linux"):
            return "linux"
        if (p == "Darwin"):
            return "osx"
        if (p == "Windows"):
            return "windows"
        return ""

    def mkdir(self, path):
        if (not self.exists(path)):
            self.d.log("mkdir: %s" % (path))
            makedirs(path)
        else:
            self.d.log("Exist directory: %s" % (path))

    def remove(self, path):
        if (self.isfile(path)):
            self.d.log("Removed %s" % (path))
            remove(path)
        elif (self.isdir(path)):
            self.d.log("Removed %s" % (path))
            rmtree(path)
        else:
            self.d.warn("Didn't removed %s" % (path))

    def rename(self, src, dst):
        if (self.exists(dst)):
            self.remove(dst)

        if (self.isfile(src)):
            rename(src, dst)
        elif (self.isdir(src)):
            self.remove(dst)
            self.copy(src, dst)
            self.remove(src)

    def splitext(self, path):
        return splitext(path)

    def get_file_path_in_dir(self, dir_path):
        path_list = []
        for (root, dirs, files) in walk(dir_path):
            for file_name in files:
                path_list.append(self.join_dirs([root, file_name]))
        return path_list

    def get_dir_path_in_dir(self, dir_path):
        path_list = []
        for (root, dirs, files) in walk(dir_path):
            for dir_name in dirs:
                path_list.append(self.join_dirs([root, dir_name]))
        return path_list

    def get_path_in_dir(self, dir_path):
        return self.get_file_path_in_dir(dir_path) + self.get_dir_path_in_dir(dir_pat)

    def copy(self, src, dst):
        # file -> file(not exist)
        if (self.isfile(src) and self.isdir(dirname(dst)) and not self.isfile(dst)):
            copy2(src, dst)
            self.d.log("%s -> %s" % (src, dst))
        #file -> file(exist)
        elif (self.isfile(src) and self.isfile(dst)):
            self.remove(dst)
            copy2(src, dst)
            self.d.log("%s -> %s" % (src, dst))
        #dir -> dir(not exist)
        elif (self.isdir(src) and not self.isdir(dst)):
            copytree(src, dst)
            self.d.log("%s -> %s" % (src, dst))
        #dir -> dir(exist)
        elif (self.isdir(src) and self.isdir(dst)):
            src_len = len(src)
            path_list = self.get_file_path_in_dir(src)
            for path in path_list:
                src_relpath = path[src_len + 1:]
                dst_abspath = self.join_dirs([dst, src_relpath])
                src_abspath = self.join_dirs([src, src_relpath])
                if (self.isfile(dst_abspath)):
                    self.remove(dst_abspath)
                self.mkdir(self.dirname(dst_abspath))
                self.copy(src_abspath, dst_abspath)
            self.d.log("%s -> %s" % (src, dst))

    def chmod(self, path, mode):
        if (self.exists(path)):
            chmod(path, mode)
        else:
            self.d.warn("Not found %s" % (path))

    def chown(self, path, user=None, group=None):
        if (user is None or group is None):
            print("Chown need user and group")
            self.exit()

        uid = getpwnam(user).pw_uid
        gid = getgrnam(group).gr_gid
        if (self.isfile(path)):
            chown(path, uid, gid)
        elif (self.isdir(path)):
            chown(path, uid, gid)
            for p in self.get_dir_path_in_dir(path):
                chown(p, uid, gid)
            for p in self.get_file_path_in_dir(path):
                chown(p, uid, gid)
        else:
            self.d.warn("Not found %s" % (path))

    def decode(self, text):
        lookup = (
                 'utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
                 'shift_jis', 'shift_jis_2004','shift_jisx0213',
                 'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
                 'iso2022_jp_ext','latin_1', 'ascii',
                 )
        enc = None

        for encoding in lookup:
            try:
                text = text.decode(encoding)
                enc = encoding
                break
            except:
                pass
        if isinstance(text, unicode):
            return text, enc
        else:
            raise LookupError

    def get_pid(self, keyword):
        pid_pos = 1
        pid_list = []
        stdout, stderr = Popen(["ps", "aux"], stdout=PIPE, stderr=PIPE).communicate()
        lines = [j for i,j in enumerate(stdout.split('\n')) if i > 0]
        r = compile(r'\s+')
        for line in lines:
            l = r.split(line.strip())
            for idx in range(len(l)):
                if (l[idx].find(keyword) < 0):
                    continue
                pid_list.append(int(l[pid_pos]))
        return list(set(pid_list))

    def __unzip_tar(self, src, dst):
        tf = open(src)
        tf.extractall(dst)
        tf.close()

    def __zip_tar(self, src, dst, mode):
        tf = open(dst, mode)
        for root, dirs, files in walk(src):
            for file_path in files:
                tf.add(self.join_dirs([root, file_path]))
        tf.close() 

    def __zip(self, src, dst):
        z = ZipFile(dst, "w", ZIP_DEFLATED)
        if (self.isdir(src)):
            for path in self.get_path_in_dir(src):
                z.write(path, relpath(path, "./"))
        elif (self.isfile(src)):
            z.write(src, relpath(src, "./"))
        z.close()

    def __unzip(self, src, dst):
        z = ZipFile(src, "r")
        for path in z.namelist():
            if (not self.basename(path)):
                self.mkdir(path)
            else:
                fd = file(path, "wb")
                fd.write(z.read(path))
                fd.close()
        z.close()

    def unzip_tar_bz2(self, src, dst):
        if (dst is None):
            name = self.basename(src)
            idx = name.rfind(".tar.bz2")
            dst = self.join_dirs([self.dirname(src), name[0:idx]])

        self.remove(dst)
        self.__unzip_tar(src, dst)

    def unzip_tar_gz(self, src, dst=None):
        if (dst is None):
            name = self.basename(src)
            idx = name.rfind(".tar.gz")
            dst = self.join_dirs([self.dirname(src), name[0:idx]])

        self.remove(dst)
        self.__unzip_tar(src, dst)

    def zip_tar_bz2(self, src, dst):
        if (dst is None):
            root, ext = self.splitext(self.basename(src))
            dst = self.join_dirs([self.dirname(src), "%s.tar.bz2" % (root)])

        self.remove(dst)
        self.__zip_tar(src, dst, 'w:bz2')

    def zip_tar_gz(self, src, dst=None):
        if (dst is None):
            root, ext = self.splitext(self.basename(src))
            dst = self.join_dirs([self.dirname(src), "%s.tar.gz" % (root)])

        self.remove(dst)
        self.__zip_tar(src, dst, 'w:gz')

    def zip(self, src, dst=None):
        if (dst is None):
            root, ext = self.splitext(self.basename(src))
            dst = self.join_dirs([self.dirname(src), "%s.zip" % (root)])

        self.remove(dst)
        self.__zip(src, dst)

    def unzip(self, src, dst=None):
        if (dst is None):
            name = self.basename(src)
            idx = name.rfind(".zip")
            dst = self.join_dirs([self.dirname(src), name[0:idx]])

        self.remove(dst)
        self.__unzip(src, dst)
