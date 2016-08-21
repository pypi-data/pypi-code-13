# Author: John Jiang
# Date  : 2016/8/22

from setuptools import setup, find_packages

setup(
        name='pyrandom',
        version='0.0.1',
        url='https://github.com/j178/pyrandom',
        author='john jiang',
        author_email='nigelchiang@outlook.com',
        keywords=['random', 'random.org'],
        description='a convenient Python lib for random.org ',
        license='MIT',
        packages=find_packages(),
        install_requires=[
            'requests',
        ],
)
