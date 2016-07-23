# vi:et:ts=4 sw=4 sts=4

import subprocess

_VCSS = {
    'git': 'git rev-parse --abbrev-ref HEAD -C {}',
    'hg': 'hg branch -R {}',
}

def get_branch(path):
    branch = None

    for _, cmd in _VCSS.iteritems():
        try:
            command = cmd.format(path)
            branch = subprocess.check_output(command.split())
            branch = branch.strip()
        except subprocess.CalledProcessError:
            pass

    return branch

def get_vcses():
    return _VCSS.keys()

