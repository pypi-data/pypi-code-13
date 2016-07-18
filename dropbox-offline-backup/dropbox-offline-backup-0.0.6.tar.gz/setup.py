from setuptools import setup, find_packages


setup(
    name='dropbox-offline-backup',
    version='0.0.6',
    description='Backup your Dropbox offline',
    url='https://github.com/764664/dropbox-offline-backup',
    author='Jie Lu',
    author_email='764664@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['dropbox'],
    entry_points={
        'console_scripts': [
            'dropboxbackup=dropboxbackup:start',
        ],
    }
)