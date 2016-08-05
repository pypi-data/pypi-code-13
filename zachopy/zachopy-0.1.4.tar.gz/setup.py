from setuptools import setup

# See PEP 0440: https://www.python.org/dev/peps/pep-0440/#version-scheme
VERSION = '0.1.4'

setup(
    name='zachopy',
    version=VERSION,
    package_dir={'zachopy': '.',
                 'zachopy.borrowed': 'borrowed',
                 'zachopy.displays': 'displays',
                 'zachopy.relations': 'relations'},
    packages=['zachopy', 'zachopy.borrowed', 'zachopy.displays', 'zachopy.relations'],
    description="Various tools used in lots of code written by Zach Berta-Thompson (zkbt@mit.edu)",
    author='Zach Berta-Thompson',
    author_email='zkbt@mit.edu',
    url='https://github.com/TESScience/zachopy',
    install_requires=['numpy', 'astropy', 'astroquery', 'matplotlib', 'scipy', 'pyds9==1.8.1', 'colormath', 'parse'],
    download_url = 'https://github.com/TESScience/zachopy/tarball/{}'.format(VERSION),
)
