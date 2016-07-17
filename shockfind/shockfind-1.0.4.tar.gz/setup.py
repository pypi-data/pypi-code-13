from setuptools import setup, find_packages

setup(name='shockfind',
      version='1.0.4',
      description='Find shocks in MHD simulations.',
      long_description='Check the paper Lehmann, Federrath and Wardle (2016).',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Astronomy',
      ],
      keywords='MHD shocks ISM',
      url='http://web.science.mq.edu.au/~alehmann/shockfind',
      author='Andrew Lehmann',
      author_email='andrew.lehmann@mq.edu.au',
      license='Apache',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
