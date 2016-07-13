from setuptools import setup
from setuptools import find_packages

setup(name='componere',
      version='0.1.3',
      url='https://github.com/premisedata/componere',
      author='Moustafa Maher and Mostafa Gabriel',
      author_email='mmaher@premise.com, mgabriel@premise.com',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'componere = componere.__main__:_main',
        ]
      },
      install_requires=['graphviz==0.4.10', 'pyyaml==3.10'])
