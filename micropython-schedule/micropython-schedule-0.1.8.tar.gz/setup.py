import sys
sys.path.pop(0)
from setuptools import setup

#from distutils.core import setup


SCHEDULE_VERSION = '0.1.8'
SCHEDULE_DOWNLOAD_URL = (
    'https://github.com/rguillon/schedule/tarball/' + SCHEDULE_VERSION
)


setup(
    name='micropython-schedule',
    packages=['schedule'],
    version=SCHEDULE_VERSION,
    description='Job scheduling for humans.',
    long_description="Lighter implementation of the schedule module: https://github.com/dbader/schedule",
    license="MIT", 
    author='Renaud Guillon',
    author_email='renaud.guillon@gmail.com',
    url='https://github.com/rguillon/schedule',
    download_url=SCHEDULE_DOWNLOAD_URL,
    keywords=[
        'schedule', 'periodic', 'jobs', 'scheduling','cron','micropython'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Natural Language :: English',
    ],
    py_modules=['schedule'], 
    install_requires=['micropython-ucontextlib', 'micropython-logging', 'micropython-time']
)
