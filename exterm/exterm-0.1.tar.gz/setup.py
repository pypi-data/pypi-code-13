from distutils.util import convert_path
from setuptools import setup, find_packages

main_ns = {}
ver_path = convert_path('exterm/version.py')
with open(ver_path) as ver_file:
        exec(ver_file.read(), main_ns)

version = main_ns['__version__']

# long_description = open('README.rst').read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='exterm',
    version=version,
    author='Alex Tan',
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'miniterm = exterm.tools.miniterm:main',
            ]
    },
    # package_data={'exterm.tools': ['avrdude/*']},
    include_package_data=True,
    author_email='alex.jz.tan@gmail.com',
    # url="https://github.com/uarm-developer/pyuarm",
    keywords="curses miniterm exterm",
    install_requires=requirements,
    # long_description=long_description,
    description='A simple terminal library',
)
