from setuptools import setup

setup(
    name='loot',
    version='0.2.0',
    author='Taff Gao',
    author_email='gaotongfei199@gmail.com',
    url='https://github.com/gaotongfei/loot',
    description='loot is a command line tool that helps you work with github without pain',
    py_modules=['loot'],
    install_requires=[
        'Click',
        'colorama',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        loot=loot:cli
    ''',
)
