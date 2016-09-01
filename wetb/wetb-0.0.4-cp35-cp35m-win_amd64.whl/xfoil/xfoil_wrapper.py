from subprocess import PIPE, Popen, call
import re
import os
import subprocess
import numpy as np
re_float = "\D*( -?[\d\.]*)\D*"

def run(cmd_lst, regex=None):
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    ps = Popen([os.path.dirname(__file__) + '/xfoil.exe'], stdin=PIPE, stdout=PIPE, stderr=PIPE, startupinfo=si)
    stdout, stderr = ps.communicate(("\n".join(cmd_lst) + "\n").encode())

    if stderr != b"At line 109 of file ../src/userio.f (unit = 5, file = 'stdin')\nFortran runtime error: End of file\n" and\
       stderr != b"At line 135 of file ../src/userio.f (unit = 5, file = 'stdin')\nFortran runtime error: End of file\n":
        print (stderr)
        raise Exception(stderr.decode().replace("\r\n", "\n"))
    output = stdout.decode().replace("\r\n", "\n")
    if regex is None:
        return output
    else:
        return re.compile(".*(%s).*" % regex, re.DOTALL).match(output)

def run_default(filename, re=None, alpha=0, cmd_lst=[], regex="*"):
    load_cmd = ['load', filename, 'airfoil']
    with open(filename) as fid:
        if 1 or len(fid.readlines()) < 160:
            load_cmd.append('pane')
    oper_cmd = ['oper']
    if re is not None:
        oper_cmd.extend(['re %f' % re, 'visc', 'iter 200'])
    oper_cmd.extend(['alfa %f' % alpha, cmd_lst])

    return run(load_cmd + oper_cmd + cmd_lst + ["\n"], regex)


def run_default_alfaseq(filename, Re=None, Ma=0, alfaseq=range(-4, 21), output_cmd=[], regex='*'):
    load_cmd = ['load', filename, 'airfoil']
    with open(filename) as fid:
        if 1 or len(fid.readlines()) < 160:
            load_cmd.append('pane')
    oper_cmd = ['oper']

    if Re is not None:
        oper_cmd.extend(['Re %f' % Re, 'M %f' % Ma, 'visc', 'iter 200'])
    for a in alfaseq:
        oper_cmd.extend(['alfa %f' % a] + output_cmd)

    output = run(load_cmd + oper_cmd + ["\n"])


    print (len(output.split('Calculating wake trajectory')))

    output_lst = output.split('Calculating wake trajectory')[1:]
    return (np.array([re.compile(".*a =%s.*%s.*" % (re_float, regex), re.DOTALL).match(o).groups() for o in output_lst], dtype=np.float))


if __name__ == "__main__":
    #u, v = map(float, run_default('naca633-619.8', re=1e6, alpha=0, cmd_lst=['vels -0.351688344995 -0.131875790438'], regex='u/Uinf =%s v/Uinf = %s' % (re_float, re_float)).groups()[1:])
    #print (u, v)
    run_default_alfaseq('naca633-618_spline', 3e6, range(4), ['vels -0.473619 -0.116992'], 'u/Uinf =%s v/Uinf = %s' % (re_float, re_float))



#from threading import Thread
#from subprocess import Popen, PIPE
#from queue import Queue
#import time
#import sys
#
#
#
#
#
#myprocess = Popen('xfoil.exe', shell=False, stdin=PIPE, stdout=None, stderr=PIPE)
#
#
#def sendcmd(cmd):
#    myprocess.stdin.write(("%s\n" % cmd).encode())
#    myprocess.stdin.flush()
#sendcmd('load naca633-618')
#sendcmd('naca63')
#sendcmd('pane')
#sendcmd('oper')
#sendcmd('vels -10,0')
#sendcmd('')
#sendcmd('quit')
