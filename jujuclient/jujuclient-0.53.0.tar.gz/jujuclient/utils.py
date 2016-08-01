import subprocess


_juju_major_version = None


def get_juju_major_version():
    global _juju_major_version
    if _juju_major_version is None:
        _juju_major_version = int(subprocess.check_output(
            ["juju", "--version"]).split(b'.')[0])
    return _juju_major_version
