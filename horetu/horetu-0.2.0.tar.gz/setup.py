from distutils.core import setup

setup(name='horetu',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Make a command-line interface from a function.',
      url='http://src.thomaslevine.com/horetu/',
      packages=['horetu'],
      install_requires=[
      #   'inflection>=0.3.1', # for singularize
      ],
      extras_require={
          'docs': [
              'sphinxcontrib-autorun>=0.1',
          ],
          'tests': ['pytest>=2.6.4'],
          'dev': ['horetu[docs]', 'horetu[tests]']
      },
      tests_require=[
          'horetu[tests]',
      ],
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ],
      version='0.2.0',
      license='AGPL',
      )
