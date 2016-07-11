import sys
from setuptools import setup

PY2 = sys.version_info[0] <= 2

setup(
        name='worklogmd',
        version=0.24,
        author='Samuel Taylor',
        url='https://github.com/ssaamm/worklog.md',
        description='Text-based work habit tracker',
        license='MIT',
        packages=['worklog', 'worklog.parsing2' if PY2 else 'worklog.parsing'],
        install_requires=['antlr4-python2-runtime' if PY2 else 'antlr4-python3-runtime'],
        entry_points={
            'console_scripts': ['processWorklog = worklog.process:run',
                                'printWorklogFunction = worklog.print_worklog_function:run'],
        },
)
