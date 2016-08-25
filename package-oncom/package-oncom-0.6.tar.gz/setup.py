from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='package-oncom',
      version='0.6',
      description='Cuma latihan upload package 1',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
      ],
      url='http://github.com/blahblah/package-oncom',
      author='Yanzen',
      author_email='yanzen@example.com',
      license='MIT',
      packages=['package_oncom'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)