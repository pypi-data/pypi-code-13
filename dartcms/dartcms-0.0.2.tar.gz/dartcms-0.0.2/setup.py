import setuptools

setuptools.setup(
    name='dartcms',
    version='0.0.2',
    description='DartCMS',
    long_description=open('README.md').read().strip(),
    author='Dmitry Astrikov',
    author_email='astrikov.d@gmail.com',
    url='https://github.com/astrikov-d/dartcms',
    py_modules=['dartcms'],
    install_requires=[
        'Django>=1.9.6',
        'django-extra-views>=0.7.1',
        'django-form-utils>=1.0.3',
        'django-gravatar2>=1.4.0',
        'django-mptt>=0.8.4',
        'django-widget-tweaks>=1.4.1',
        'Pillow>=3.2.0',
    ],
    license='MIT License',
    zip_safe=False,
    keywords='django cms dartcms',
    classifiers=['Development Status :: 3 - Alpha']
)
