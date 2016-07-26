from setuptools import setup
setup(
    name='headspin-cli',
    packages=['headspin_cli'],
    version='0.0.0',
    description='HeadSpin Python API and command-line interface',
    author='HeadSpin',
    author_email='marius@headspin.io',
    url='https://github.com/projectxyzio/headspin-cli',
    download_url='https://github.com/projectxyzio/headspin-cli',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Software Development :: Testing"
    ],
    install_requires=["docopt", "requests"],
    entry_points={
        'console_scripts': [
            "hs = headspin_cli.cli:console_main",
        ]
    },
    keywords=['testing', 'mobile', 'API', 'console', 'docker']
)
