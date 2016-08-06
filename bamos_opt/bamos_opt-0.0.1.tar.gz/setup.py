from setuptools import find_packages, setup

setup(
    name='bamos_opt',
    version='0.0.1',
    description="Python library for optimization",
    author='Brandon Amos',
    author_email='bamos@cs.cmu.edu',
    platforms=['any'],
    license="Apache 2.0",
    url='https://github.com/bamos/opt.py',
    packages=find_packages(),
    install_requires=[
        'numpy>=1<2',
    ]
)
