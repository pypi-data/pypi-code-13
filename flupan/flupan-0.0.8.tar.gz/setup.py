from setuptools import setup

import unittest
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*_test.py')
    return test_suite

setup(name='flupan',
      version='0.0.8',
      description='Python library to parse influenza passaging annotations',
      url='http://github.com/clauswilke/flupan',
      author='Claire D. McWhite',
      author_email='claire.mcwhite@utexas.edu',
      license='MIT',
      #install_requires = ['setuptools-git'],
      scripts=['bin/translate_passage'],
      package_dir={'flupan':'src'},
      #packages=['flupan', 'flupan.tables'],
      packages=['flupan'],
      #package_data= {'flupan' : ['tables/*.txt']},
      #package_data={'flupan.tables':['*']},
      include_package_data=True,
      #test_suite='nose.collector',
     #tests_require=['nose']
      test_suite='setup.my_test_suite'#,
      #tests_require=['unittest']

     )
