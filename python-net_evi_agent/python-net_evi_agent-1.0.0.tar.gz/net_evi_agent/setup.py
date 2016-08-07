import os
import sys

from distutils.core import setup

name = "net_evi_agent"

rootdir = os.path.abspath(os.path.dirname(__file__))

# Restructured text project description read from file
long_description = open(os.path.join(rootdir, 'README.md')).read()
print long_description
# Python 2.4 or later needed
if sys.version_info < (2, 4, 0, 'final', 0):
    raise SystemExit, 'Python 2.4 or later is required!'

# Build a list of all project modules
packages = []
for dirname, dirnames, filenames in os.walk(name):
        print dirname,'\n',dirnames,'\n',filenames
        if '__init__.py' in filenames:
            #pass
            packages.append(dirname.replace('/', '.'))
print "packages:",packages,"\n"
package_dir = {name: name}
print package_dir
# Data files used e.g. in tests
package_data = {name: [os.path.join(name, 'tests', 'prt.txt')]}

# The current version number - MSI accepts only version X.X.X
exec(open(os.path.join(name, 'version.py')).read())
print version

# Scripts
scripts = []
for dirname, dirnames, filenames in os.walk('scripts'):
    for filename in filenames:
        if not filename.endswith('.bat'):
            scripts.append(os.path.join(dirname, filename))

# Provide bat executables in the tarball (always for Win)
if 'sdist' in sys.argv or os.name in ['ce', 'nt']:
    for s in scripts[:]:
        scripts.append(s + '.bat')

# Data_files (e.g. doc) needs (directory, files-in-this-directory) tuples
data_files = []
for dirname, dirnames, filenames in os.walk('doc'):
        fileslist = []
        for filename in filenames:
            fullname = os.path.join(dirname, filename)
            fileslist.append(fullname)
        data_files.append(('share/' + name + '/' + dirname, fileslist))

setup(
    name='python-' + name,
    version=version,
    author  ="wesia",
    author_email = "wexll@sina.com",
    url = "http://www.headfirst.com",
    description = "An openstack multi_tenant network isolation evidence gathering module",
    classifiers=[
          'Development Status :: 1 - Planning',
          'Environment :: Console',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.4',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='openstack multi_tenant network evidence',
      packages=packages,
      package_dir=package_dir,
      package_data=package_data,
      scripts=scripts,
      data_files=data_files,
)

