from setuptools import setup

import unittest
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*_test.py')
    return test_suite

setup(name='flupan',
      version='0.0.6',
      description='Python library to parse influenza passaging annotations',
      url='http://github.com/clauswilke/flupan',
      author='Claire D. McWhite',
      author_email='claire.mcwhite@utexas.edu',
      license='MIT',
      scripts=['bin/translate_passage'],
      package_dir={'':'src'},
      #test_suite='nose.collector',
      #tests_require=['nose']
      test_suite='setup.my_test_suite'#,
      #tests_require=['unittest']

     )
