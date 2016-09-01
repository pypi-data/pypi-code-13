# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import subprocess

def run_work(projectdir):
    p = subprocess.Popen('cd {}&&git reset --hard&&git pull'.format(projectdir),
                         shell=True,
                         stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    from os.path import join
    import time
    f = open(join(projectdir, 'date'), 'w')
    f.write(str(time.time()))

