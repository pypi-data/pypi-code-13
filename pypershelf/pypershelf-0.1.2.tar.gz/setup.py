from setuptools import setup

setup(name='pypershelf',
      version='0.1.2',
      description='ORM With Focus on RM. Inspired by Bookshelf.js',
      url='https://github.com/insipidish/pypershelf',
      author='insipidish',
      author_email='insipidish@gmail.com',
      license='MIT',
      packages=['pypershelf'],
      install_requires=['sqlent', 'nose'],
      zip_safe=False)
