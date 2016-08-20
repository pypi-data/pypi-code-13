import setuptools
import yaml

# Parse our compile config
with open('_compile-config.yml') as f:
    compile_config_yaml = yaml.safe_load(f)

VERSION = compile_config_yaml['config']['package']['version']

setuptools.setup(
    name='tractdb',
    version=VERSION,
    description='TractDB',
    url='https://tractdb.org',
    packages=['tractdb'],
    install_requires=[
        'couchdb',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [],
    },
    zip_safe=False,
)
