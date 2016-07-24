from setuptools import setup, find_packages

setup(
    name="cheerlights",
    version="0.1.1",
    author="Gregory Parker",
    description="Simple wrapper for cheerlights API",
    license="MIT",
    url="https://github.com/electronicsgeek/cheerlights",
    long_description=str(open("README.rst")),
    install_requires=["requests"]
)
