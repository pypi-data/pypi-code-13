import subprocess


def shell_call(cmd):
    result = subprocess.getoutput(cmd)
    if 'command not found' in result:
        return ""
    else:
        return result
