from setuptools import setup
setup(name='flupan',
      version='0.0.5',
      description='Python library to parse influenza passaging annotations',
      url='http://github.com/clauswilke/flupan',
      author='Claire D. McWhite',
      author_email='claire.mcwhite@utexas.edu',
      license='MIT',
      scripts=['src/translate_passage'],
      test_suite='nose.collector',
      tests_require=['nose']
     )
