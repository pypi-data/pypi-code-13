from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='funniestcsjoke',
      version='0.2',
      description='The funniest CS joke I found',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest cs joke comedy flying circus',
      url='http://github.com/fierobert/funniestcsjoke',
      author='RF',
      author_email='rf@itsoftwareengineering.com',
      license='MIT',
      packages=['funniestcsjoke'],
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/funniest-cs-joke'],
      entry_points = {
        'console_scripts': ['funniest-cs-joke=funniestcsjoke.command_line:main'],
      },
      zip_safe=False)