import subprocess


def shell_call(cmd):
    result = subprocess.getoutput(cmd)
    if 'command not found' or 'Cannot connect to the Docker daemon' in result:
        return ""
    else:
        return result
