from setuptools import setup, find_packages

def get_version(path):
    """ Parse the version number variable __version__ from a script. """
    import re
    string = open(path).read()
    version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_str = re.search(version_re, string, re.M).group(1)
    return version_str
    
setup(
    name = 'admiral',
    description = "Simple python high-performance computing cluster batch submission",
    version = get_version("src/admiral/__init__.py"),

    author = "Noah Spies",
    url = "https://github.com/nspies/admiral",
    
    packages = find_packages('src'),
    package_dir = {"": "src"},

    install_requires = ["humanfriendly"]

)
