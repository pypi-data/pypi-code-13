from setuptools import setup, find_packages

setup(

    name="fsq_wrapper",
    version="0.0.5",
    description="Test This is a CLI tool to make calls to the foursquare API",
    url="https://github.com/Zabanaa/foursquare-cli",
    author="Karim Cheurfi (Zabanaa)",
    author_email="karim.cheurfi@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: Freely Distributable',
        'Programming Language :: Python'
    ],
    keywords="Foursquare API web development",
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'fsq-wrapper=fsq_wrapper:main'
        ]
    }
)

