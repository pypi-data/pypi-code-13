import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


exclude = [
    'tests',
]


packages = (
    'arpegio',
    'arpegio.blog',
    'arpegio.pages',
)

setup(
    name='arpegio',
    version='0.2.1',
    author='Gildardo Adrian Maravilla Jacome',
    author_email='gilmrjc@gmail.com',
    description='Django apps that sound good together',
    long_description=README,
    url='https://gitlab.com/arpegio/arpegio/',
    license='MIT',
    install_requires=[
        'django>=1.8,<1.11',
        'pillow>=3.3.0,<3.4.0',
    ],
    packages=find_packages(exclude=exclude),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms=['all', ],
)
