from setuptools import setup, find_packages

setup(
    name = 'just4alauda',
    version = '0.1',
    keywords = ('alauda', 'api'),
    description = 'An simple python API for alauda.cn and alauda.io',
    license = 'wtfpl',
    install_requires = ['pyyaml'],

    author = 'Just4test',
    author_email = 'myservice@just4test.net',
    
    packages = find_packages(),
    platforms = 'any',
)