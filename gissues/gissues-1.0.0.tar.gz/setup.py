from setuptools import setup, find_packages

setup(

    name='gissues',
    version='1.0.0',

    description='View and Manage Github issues from the comfort of your console.',

    # The project's main homepage.
    url='https://github.com/DeveloperMal/gissues',

    # Author details
    author='Malcolm Jones',
    author_email='developermalj@gmail.com',

    license='mit',
    keywords='github issues cli',

    install_requires=['click', 'github3.py'],
    packages=find_packages(),

    entry_points={
    'console_scripts': [
        'giss=gissues.cli:giss',
    ],
    },
)
