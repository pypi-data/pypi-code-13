from os.path import join, dirname
from setuptools import setup, find_packages

setup(
    name='search_engine_app',
    version = "0.0.10",
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=[
        'Flask',
        'validators',
        'urllib3',
        'urlparse3',
        'cookiejar',
        'bs4'
    ],
    entry_points={
       'console_scripts': [
           'serve=search_engine_app.flask_app:serve'
           ]
   },
   include_package_data=True
)
