from setuptools import setup, Extension
import numpy

setup(
    name="ulo",
    version="0.1.1",
    packages=["ulo"],
    test_suite="tests",
    author="Pete Shadbolt",
    author_email="hello@peteshadbolt.co.uk",
    url="https://github.com/peteshadbolt/ulo",
    description="Linear optics simulator",
    keywords="quantum",
    scripts=[],
    package_data={},
    ext_modules=[],
    include_package_data=False
)
