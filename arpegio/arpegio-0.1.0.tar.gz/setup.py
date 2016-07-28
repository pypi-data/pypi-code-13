from os import path
from setuptools import find_packages, setup


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


exclude= [
    'tests',
]


packages=(
    'arpegio',
    'arpegio.blog',
    'arpegio.pages',
)

setup(
    name='arpegio',
    version='0.1.0',
    author='Gildardo Adrian Maravilla Jacome',
    author_email='gilmrjc@gmail.com',
    description='Django apps that sound good together',
    long_description=read('README.rst'),
    url='https://gitlab.com/arpegio/arpegio/',
    license='MIT',
    install_requires=[
        'django>=1.8,<1.10',
        'pillow>=3.3.0,<3.4.0',
    ],
    packages=find_packages(exclude=exclude),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms=['all', ],
)
