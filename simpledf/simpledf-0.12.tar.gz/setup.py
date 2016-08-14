from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='simpledf',
      version='0.12',
      description='A simple, easier-to-use implementation of dataframes.',
      long_description=readme(),
      url='http://github.com/ankur-gupta/simpledf',
      author='Ankur Gupta, Bryson Hagerman',
      author_email='ankur@perfectlyrandom.org, brysonova@gmail.com',
      keywords='dataframes pandas groupby apply custom function',
      license='MIT',
      packages=['simpledf'],
      zip_safe=False,
      install_requires=[
          'pandas',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2.7'
      ],
      test_suite='nose.collector',
      tests_require=['nose'])
