"""
Bayesian AB Test
-----------------

Calculates Bayesian Probabilty that A - B > x
"""
from setuptools import setup

setup(
    name='bayesian_ab_test',
    version='0.0.1',
    #packages=[''],
    url='http://github.com/eriktaubeneck/bayesian_ab_test',
    license='MIT',
    author='Erik Taubeneck',
    author_email='erik.taubeneck@gmail.com',
    description='Calculates Bayesian Probability that A - B > x',
    long_description=__doc__,
    py_modules=['ab_test', 'cli'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'numpy >= 1.10.0'
    ],
    entry_points="""
    [console_scripts]
    bayesian_ab_test = cli:main
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English ',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
