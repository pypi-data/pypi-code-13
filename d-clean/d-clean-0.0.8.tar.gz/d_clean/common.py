import subprocess


def shell_call(cmd):
    out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                shell=True).communicate()
    if out:
        out = out.decode('utf-8')
    if err:
        err = err.decode('utf-8')

    if err:
        return ""
    else:
        return out
