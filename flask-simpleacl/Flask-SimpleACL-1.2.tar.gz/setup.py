from setuptools import setup

setup(
    name='Flask-SimpleACL',
    version='1.2',
    url='',
    license='BSD',
    author='swerwer',
    description='Simple ACL extension',
    long_description=__doc__,
    py_modules=['flask_simpleAcl', 'test_simpleAcl'],
    test_suite='test_simpleAcl',
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Login'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
