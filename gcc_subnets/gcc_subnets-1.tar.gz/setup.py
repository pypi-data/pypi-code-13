from setuptools import setup

setup(
    name='gcc_subnets',
    version='1',
    description='A simple client for fetching Google Compute Cloud subnets.',
    url='https://github.com/sbarbett/gcc_subnets',
    author='Shane Barbetta',
    author_email='shane@barbetta.me',
    license='The MIT License (MIT)',
    keywords='gcc_subnets',
    packages=['gcc_subnets'],
    install_requires=['dnspython'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    zip_safe=False
)