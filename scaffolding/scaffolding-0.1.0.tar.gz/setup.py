from setuptools import (
      setup, find_packages
)

setup(name='scaffolding',
      version='0.1.0',
      description='Setup your project layout by templates',
      url='https://github.com/MinweiShen/scaffolding',
      author='Minwei Shen',
      author_email='minweishen1991@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'docopt',
      ],
      entry_points={
          'console_scripts': ['scaffold=scaffold.scaffold:main'],
      },
      zip_safe=False
      )
