from setuptools import setup

setup(name='apertium_lint',
      version='0.2',
      description='Lint for apertium. Part of GSoC 2016',
      url='https://gitlab.com/jpsinghgoud/apertium-lint',
      author='Jaipal Singh Goud',
      author_email='jpsinghgoud@gmail.com',
      license='MIT',
      packages=['apertium_lint'],
      scripts=['bin/apertium_lint'],
      zip_safe=False)