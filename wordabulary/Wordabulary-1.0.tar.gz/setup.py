from setuptools import setup
setup(
  name = 'Wordabulary',
  packages = ['Wordabulary'], # this must be the same as the name above
  version = '1.0',
  description = 'A console-based software which may be used as a library for analysing word patterns, various properties of words, analysing documents.',
  author = 'Kaustubh Hiware',
  author_email = 'hiwarekaustubh@gmail.com',
  url = 'https://github.com/kaustubhhiware/Wordabulary', 
  # download_url = '',
  keywords = ['Words', 'Vocabulary', 'wordplay', 'Literature', 'Books', 'Kaustubh Hiware', 'Python', ], 
  
  license = 'GNU General Public License v3 (GPLv3)',
  #reference:
  #https://pypi.python.org/pypi?%3Aaction=list_classifiers
  #https://github.com/pypa/sampleproject/blob/master/setup.py

  classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Build Tools',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    install_requires=['prettytable', 'matplotlib'],#graphs and tables
)