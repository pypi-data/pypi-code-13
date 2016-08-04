from setuptools import setup, find_packages

setup(

    name="fsq_wrapper",
    version="0.0.1",
    description="This is a CLI tool to make calls to the foursquare API",
    url="https://github.com/Zabanaa/foursquare-cli",
    author="Karim Cheurfi (Zabanaa)",
    author_email="karim.cheurfi@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Web Development',
        'Licence :: OSI Approved :: MIT Licence',
        'Programming Language :: Python :: 3.5'
    ],
    keywords="Foursquare API web development",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fsq-wrapper=fsq_wrapper:main'
        ]
    }
)

