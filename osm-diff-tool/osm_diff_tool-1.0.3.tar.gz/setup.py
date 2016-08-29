from setuptools import setup

setup(
    name = 'osm_diff_tool',
    version = '1.0.3',
    description = 'Tool for use with OpenStreetMap planet diffs.',
    url = 'http://github.com/ethan-nelson/osm_diff_tool',
    author = 'Ethan Nelson',
    author_email = 'git@ethan-nelson.com',
    packages = ['osmdt'],
    license = 'MIT',
    install_requires = ['requests']
    )
      
