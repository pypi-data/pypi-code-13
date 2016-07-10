from setuptools import setup

setup(
    name='Flask-SimpleACL',
    version='1.0',
    url='',
    license='BSD',
    author='swerwer',
    description='Simple ACL extension',
    long_description=__doc__,
    py_modules=['simple_acl'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
