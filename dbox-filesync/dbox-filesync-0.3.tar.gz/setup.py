from setuptools import setup

setup(
        name='dbox-filesync',
        version='0.3',
        author='Erik Stenlund',
        author_email='erikstenlund0810@gmail.com',
        description='Encapsulation of dropbox module for simple file synchronization',
        py_modules=['dbox_filesync'],
        install_requires=['dropbox'],
)
