from setuptools import setup

setup(name='axl',
      version='0.5.1',
      description='Python package that generates web extensions for Firefox',
      url='http://github.com/justinpotts/axl',
      author='Justin Potts',
      author_email='jpotts@mozilla.com',
      license='MPL',
      packages=['axl'],
      install_requires=['scipy'],
      zip_safe=False,
      entry_points="""
        [console_scripts]
        axl = axl.axl:cli
    """)
