from setuptools import setup


setup(
    name='lektor-google-tag-manager',
    version='0.1',
    url='http://github.com/JavierLopezMunoz/lektor-google-tag-manager/',
    author=u'Javier Lopez',
    author_email='javier@lopezmunoz.name',
    license='BSD',
    description='Adds support for Google Tag Manager to Lektor CMS',
    py_modules=['lektor_google_tag_manager'],
    entry_points={
        'lektor.plugins': [
            'google-tag-manager = lektor_google_tag_manager:GoogleTagManagerPlugin',
        ]
    },
    install_requires=['markupsafe', 'lektor'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
