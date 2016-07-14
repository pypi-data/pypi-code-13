from setuptools import setup, find_packages


setup(
    name='dropbox-offline-backup',
    version='0.0.2',
    description='Backup your Dropbox offline',
    url='https://github.com/764664/dropbox-offline-backup',
    author='Jie Lu',
    author_email='764664@gmail.com',
    license='MIT',
    install_requires=['dropbox'],
    entry_points={
        'console_scripts': [
            'dropboxbackup=src:start',
        ],
    }
)