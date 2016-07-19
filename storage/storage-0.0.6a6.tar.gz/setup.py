from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='storage',
    version='0.0.6a6',
    description='Libraries to interact with Enterprise Storage Arrays, FC Switches and Servers.',
    long_description=readme,
    author='Srikanth Chundi',
    author_email='srikanth912@gmail.com',
    url='https://github.com/OpenSRM/storage',
    license=license,
    packages=find_packages(exclude=('docs', 'tests', 'tests.*', 'private_tests', 'private_tests.*')),
    download_url='http://pypi.python.org/pypi/storage/',
    install_requires=[
       'paramiko',
       'lxml'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Hardware",
        #"Operating System :: POSIX",
    ],
)