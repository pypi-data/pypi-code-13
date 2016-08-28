from distutils.core import setup, Extension

setup(name='pyarmstrong',
      version = '0.1',
      description = 'Simple C extension for checking armstrong numbers.',
      author = 'Jorick Caberio',
      author_email = 'jorick.caberio@voyagerinnovation.com',
      url = 'https://github.com/jcaberio/pyarmstrong',
      download_url = 'https://github.com/jcaberio/pyarmstrong/tarball/0.1',
      ext_modules=[
        Extension('pyarmstrong',
                  sources =  ['armstrong.c'],
                  include_dirs = ['/usr/include'],
                  library_dirs = ['/usr/lib'],
                  )
      ],
      classifiers=[
        'Programming Language :: Python',
	'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ]
)
