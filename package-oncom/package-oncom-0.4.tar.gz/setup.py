from setuptools import setup

setup(name='package-oncom',
      version='0.4',
      description='Cuma latihan upload package 1',
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