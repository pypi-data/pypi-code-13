from setuptools import setup

setup(
    name='yodoit',
    description='Python CLI for using an ' \
                'Eisenhower Decision Matrix with Trello',
    version='1.1.2',
    url='https://github.com/niketanpatel/yodoit-cli',
    author='Niketan Patel',
    scripts=['bin/yodoit'],
    packages=['yodoit'],
    license='MIT',
    keywords='todo list todolist trello developer ' \
             'cli eisenhower decision matrix box productivity method'
)