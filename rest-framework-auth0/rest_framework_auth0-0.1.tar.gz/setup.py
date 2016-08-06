from distutils.core import setup
setup(
  name = 'rest_framework_auth0',
  packages = ['rest_framework_auth0'],
  version = '0.1',
  description = 'Django Rest Framework Library to use Auth0 authentication',
  author = 'Marcelo Cueto',
  author_email = 'yo@marcelocueto.cl',
  url = 'https://github.com/mcueto/djangorestframework-auth0', # use the URL to the github repo
  download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', # I'll explain this in a second
  keywords = ['auth0', 'rest framework', 'django'], # arbitrary keywords
  classifiers=[
      'Environment :: Web Environment',
      'Framework :: Django',
    #   'Framework :: Django :: X.Y',  # replace "X.Y" as appropriate
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Topic :: Internet :: WWW/HTTP',
  ],
  install_requires = [
      'djangorestframework>=1.9.0',
      'djangorestframework-jwt>=1.7.2',
      'django-filter',
  ],
)
