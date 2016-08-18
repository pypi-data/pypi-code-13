from setuptools import setup


def readme():
      with open('README.rst') as f:
            return f.read()


setup(name='hearthstonecarddetector',
      version='0.1.3',
      description='match a specific cropped image to a hearthstone card id',
      long_description=readme(),
      url='https://www.github.com/russon77/hearthstonecarddetector',
      author='Tristan Kernan',
      author_email='russon77@gmail.com',
      keywords='hearthstone',
      license='MIT',
      packages=['hearthstonecarddetector'],
      zip_safe=False,
      include_package_data=True,
      install_requires=[
            'imagehash',
            'numpy',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'PIL'])

