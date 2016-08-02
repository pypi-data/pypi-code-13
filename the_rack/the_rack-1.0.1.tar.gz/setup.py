from setuptools import setup, find_packages
import the_rack

setup(
    name='the_rack',
    version=the_rack.__version__,
    packages=find_packages(),
    author="tleb",
    author_email="tleb@openmailbox.org",
    description="A cachable collection with extension abilities",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='http://github.com/tleb/the_rack',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
    ],
)
