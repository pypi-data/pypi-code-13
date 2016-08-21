from setuptools import setup

DESCRIPTION = "A command-line interface for fetching summaries of wikipedia pages."

with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()

with open('requirements.txt', 'r') as f:
    requirements = [line.rstrip() for line in f]

setup(
        author="Kalle Saari",
        author_email="kasaar2@gmail.com",
        url="https://github.com/kalleroska/wikipedia-cli",
        name="wikipedia-cli",
        version="1.0.1",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license="MIT License",
        keywords='wikipedia cli summary',
        classifiers=['Programming Language :: Python',
                     'Programming Language :: Python :: 3.5',
                     'License :: OSI Approved :: MIT License',
                     'Development Status :: 4 - Beta',
                     'Topic :: Utilities',
                     'Intended Audience :: Developers',
                     'Environment :: Console'],
        py_modules = ['wikipedia_cli'],
        install_requires=requirements,
        entry_points={
            'console_scripts': [
                'wikipedia=wikipedia_cli:main'
                ]
            }
        )
