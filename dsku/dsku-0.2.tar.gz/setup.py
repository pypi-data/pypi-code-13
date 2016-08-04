from setuptools import setup

setup(name='dsku',
      version='0.2',
      description='Show disk usage with colored bars',
      url='http://github.com/MartijnBraam/dsku',
      author='Martijn Braam',
      author_email='martijn@brixit.nl',
      license='MIT',
      packages=['dsku'],
      install_requires=[
          'psutil',
          'colorama',
          'humanize'
      ],
      entry_points={
          'console_scripts': ['dsku=dsku.dsku:main'],
      },
      zip_safe=False)
