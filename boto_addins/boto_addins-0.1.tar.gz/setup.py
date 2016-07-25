from setuptools import setup

setup(
    name="boto_addins",
    version="0.1",
    author="Uploadcare",
    author_email="ak@uploadcare.com",
    description="Async proxy libraries for AWS services.",
    install_requires=[
        'tornado_botocore==1.0.2',
        'boto==2.42.0',
    ],
    keywords="aws amazon S3 SQS messages storage",
    url="http://packages.python.org/an_example_pypi_project",
    packages=['boto_addins'],
)
