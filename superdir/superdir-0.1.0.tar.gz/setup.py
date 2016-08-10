import os
from setuptools import setup

def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "superdir",
    author = 'Alex Ramsdell',
    author_email = 'alexramsdell@gmail.com',
    version = "0.1.0",
    url = 'http://github.com/foundling/superdir',
    license = 'MIT',
    description = 'Turn that text file into a file tree!',
    keywords = 'cli productivity',
    packages = ['superdir'],
    long_description = read('README.md'),
    install_requires = [
        'superdir'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    entry_points = '''
        [console_scripts]
        superdir=superdir:main
    '''
)
