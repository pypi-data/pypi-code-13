try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='betatim-fragala',
      version='0.1',
      description='Fragala fragala! Testing dependencies',
      long_description=('This is a non sensical package to test dependencies.'),
      license='BSD',
      author='Tim Head',
      packages=['fragala'],
      install_requires=["numpy", "scipy", "scikit-learn>=0.18dev", "cython",
                        "matplotlib"],
      dependency_links=['https://github.com/scikit-learn/scikit-learn/tarball/master#egg=scikit-learn-0.18dev'],
      )
