from setuptools import setup

setup(name='pygments-colorizer',
      version='1.0.0',
      classifer=[
      	'Development Status :: 3 - Alpha',
      	'Intended Audience :: Developers',
      	'License :: OSI Approved :: MIT License',
      	'Topic :: Text Processing :: Markup',
      	'Topic :: Utilities'
      ],
      description='Syntax highlighter for higlighting code blocks in html using Pygments.',
      url='https://github.com/BrutalSimplicity/colorizer',
      author='BrutalSimplicity',
      author_email='kory.taborn@gmail.com',
      license='MIT',
      packages=['pygments_colorizer'],
      scripts=['bin/colorize-html'],
      zip_safe=False)