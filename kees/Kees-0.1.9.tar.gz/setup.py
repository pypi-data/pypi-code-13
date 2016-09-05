from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Kees',
    version='0.1.9',
    author='C. Eigenraam',
    author_email='proprefenetre@gmail.com',
    packages=['kees'],
    url='https://github.com/proprefenetre/kees',
    keywords='thesaurus translate translation dictionary Dutch',
    license='MIT',
    description='Translate words to or from Dutch',
    long_description=readme(),
    install_requires=[
        'beautifulsoup4',
        'lxml'
    ],
    entry_points={
        'console_scripts': [
            'kees = kees.kees:run',
        ]
    }
)
