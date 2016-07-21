from setuptools import setup


setup(
    name='django-bootstrap4-datetimepicker',
    packages=['bootstrap4_datetime',],
    package_data={'bootstrap4_datetime': ['static/bootstrap4_datetime/css/*.css', 
                                          'static/bootstrap4_datetime/js/*.js',
                                          'static/bootstrap4_datetime/js/locales/*.js',]},
    include_package_data=True,
    version='4.0',
    description='Bootstrap4 compatible datetimepicker for Django projects.',
    long_description=open('README.rst').read(),
    author='Patrick Gallagher',
    author_email='patrickj@cpgallagher.com',
    url='https://github.com/pattyjogal/django-bootstrap4-datetimepicker.git',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
