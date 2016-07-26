from setuptools import setup


setup(
    name='smartenv',
    description='Intelligent environment variable handling',
    keywords='environment variable parsing',
    version='1.0.0',
    url='https://github.com/mikeroll/smartenv',
    license='MIT',
    author='mikeroll',
    author_email='scaryspiderpig@gmail.com',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-pep8'],
    py_modules=['smartenv'],
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
