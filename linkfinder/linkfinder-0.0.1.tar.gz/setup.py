from setuptools import setup, find_packages

install_requires = ['gevent==1.1.2', 'greenlet==0.4.10', 'requests==2.11.1', ]

setup(
    name='linkfinder',
    version='0.0.1',
    description='Link Finder',
    long_description='A proto type for finding and checking http links.',
    author='Dan Nguyen',
    author_email='dan.nguyens.mail@gmail.com',
    license='MIT',
    classifiers=['Development Status :: 3 - Alpha', ],
    keywords='links http gevent',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    extras_require={
        'dev': ['pep8==1.7.0',
                'pylint==1.6.4',
                ],
        'test': ['coverage==4.2', ],
    },
    entry_points={
        'console_scripts': [
            'linkfinder=linkfinder:main.execute',
        ],
    },
)
