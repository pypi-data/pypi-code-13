from setuptools import setup

version = '0.0.5'

setup(
    name='crypt_keeper',
    version=version,
    url='https://github.com/wybiral/crypt_keeper/',
    author='Davy Wybiral',
    author_email='davy.wybiral@gmail.com',
    description='Secure password keeper and generator.',
    packages=['crypt_keeper'],
    platforms='any',
    install_requires=[
        'cryptography>=1.5',
        'xerox>=0.4.1',
    ],
    classifiers=[
    ],
)