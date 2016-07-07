"""
create the package:

python setup.py sdist

register the package:

python setup.py register -r https://testpypi.python.org/pypi

Upload the package:

python setup.py upload -r https://testpypi.python.org/pypi

Test install the package:

pip install -i https://testpypi.python.org/pypi <package name>

classifier list:

https://pypi.python.org/pypi?:action=list_classifiers
"""

from distutils.core import setup

setup(
    name = 'pystl',
    packages = ['pystl'],
    version = '0.0.1',
    description = 'Simple Python package to write STL files for 3D printing.',
    author='Len Wanger',
    author_email='len_wanger@hotmail.com',
    license= 'PSF',
    keywords = 'STL stereolithography, 3D printing',
    classifiers = [ 'License :: Freely Distributable', 'Development Status :: 5 - Production/Stable',
                    'Operating System :: OS Independent', 'Programming Language :: Python',
                    'Programming Language :: Python :: 3',
                    'Intended Audience :: Developers',
                    'Topic :: Multimedia :: Graphics :: 3D Modeling'],
)
