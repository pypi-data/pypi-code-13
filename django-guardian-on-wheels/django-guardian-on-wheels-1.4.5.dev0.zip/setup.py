import os
import sys
from setuptools import setup
from extras import RunFlakesCommand


from guardian import __version__ as version

readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(readme_file, 'r') as f:
    long_description = f.readline().strip()

setup(
    name='django-guardian-on-wheels',
    version=version,
    setup_requires=['pytest-runner'],
    url='http://github.com/pombredanne/django-guardian',
    author='Lukasz Balcerzak, Philippe Ombredanne',
    author_email='pombredanne@gmail.com',
    download_url='https://github.com/pombredanne/django-guardian/tags',
    description=("Implementation of per object permissions for Django.  "
                 "Minor fork to get wheels in Pypi"),
    long_description=long_description,
    zip_safe=False,
    packages=[
        'guardian', 'guardian.conf', 'guardian.management',
        'guardian.migrations', 'guardian.templatetags', 'guardian.testapp',
        'guardian.management.commands', 'guardian.testapp.migrations',
        'guardian.testapp.tests'
    ],
    include_package_data=True,
    license='BSD',
    install_requires=[
        'Django >= 1.7',
        'six',
    ],
    tests_require=['mock', 'django-environ', 'pytest', 'pytest-django'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Security',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 ],
    test_suite='tests.main',
    cmdclass={'flakes': RunFlakesCommand},
)
