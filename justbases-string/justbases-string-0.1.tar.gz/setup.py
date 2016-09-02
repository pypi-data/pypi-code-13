import os
import sys
import setuptools
if sys.version_info[0] < 3:
    from codecs import open

def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))

README = local_file("README.rst")

with open(local_file("src/justbases_string/_version.py")) as o:
        exec(o.read())

setuptools.setup(
    name='justbases-string',
    version=__version__,
    author='Anne Mulhern',
    author_email='amulhern@redhat.com',
    description='string representation of a rational number in any base',
    long_description=open(README, encoding='utf-8').read(),
    platforms=['Linux'],
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Mathematics',
        ],
    install_requires = [
        'six'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    )
