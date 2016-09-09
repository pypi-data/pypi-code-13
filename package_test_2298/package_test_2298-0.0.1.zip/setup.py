from setuptools import setup, find_packages

setup(
    name = "package_test_2298",
    version = "0.0.1",
    keywords = ("pip", "datacanvas", "eds", "xiaoh"),
    description = "package testing",
    long_description = "first package testing",
    license = "MIT Licence",

    url = "http://nonono",
    author = "sheldon",
    author_email = "xing.gao@nokia.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)