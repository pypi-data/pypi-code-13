from setuptools import setup

setup(name='accenter',
      version='0.1',
      description='Put random accents on words. Test package.',
      url='http://github.com/steveandroulakis/accenter',
      author='Steve Androulakis',
      author_email='steve.androulakis@gmail.com',
      license='MIT',
      packages=['accenter'],
      scripts=['bin/accenter'],
      zip_safe=False)