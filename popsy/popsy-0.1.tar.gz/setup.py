from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='popsy',
      version='0.1',
      description='Tools for manipulating Handix Scientific POPS data.',
      long_description=readme(),
      classifiers=[
          'Programming Language :: Python :: 2.7',
      ],
      url='http://github.com/gavinmcmeeking/popsy',
      author='Gavin McMeeking',
      author_email='gavin@handixscientific.com',
      packages=['popsy'],
      install_requires=[
          'numpy',
          'pyserial',
      ],
      zip_safe=False)
