import requests
from packaging.version import Version

from .serializer import serialize

def get_last_version(pkg_name):
    response = requests.get('https://pypi.python.org/pypi/{0}/json'.format(pkg_name))
    pkginfo = response.json()

    releases = pkginfo['releases']
    for release in sorted(releases.keys(), reverse=True):
        version = Version(release)
        if not version.is_prerelease:
            return version

def check_file_for_updates(filename):
    requirements = {'base': {}}
    f = open(filename, 'r')
    line = True
    while line:
        line = f.readline().strip()
        parts = line.split('==')
        if len(parts) is 2:
            pkg_name, version_name = parts
            current_version = Version(version_name)
            latest_version = get_last_version(pkg_name)

            if latest_version > current_version:
                print(pkg_name, current_version, '->', latest_version)
                requirements['base'][pkg_name] = str(latest_version)
            else:
                print(pkg_name, 'ok')
                requirements['base'][pkg_name] = str(current_version)
        elif len(line.strip()) is not 0:
            print('Invalid line', line)
        # else: empty line
    serialize(requirements)
