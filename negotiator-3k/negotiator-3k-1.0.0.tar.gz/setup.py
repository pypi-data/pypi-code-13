from setuptools import setup, find_packages

setup(
    name = 'negotiator-3k',
    version = '1.0.0',
    packages = find_packages(),
    install_requires = [],
    url = 'https://github.com/ashkop/negotiator-3k',
    author = 'Alex Shkop',
    author_email = 'a.v.shkop+pypi@gmail.com',
    description = """
    Proper Content Negotiation for Python
    
    The Negotiator is a library for decision making over Content Negotiation requests.
    It takes the standard HTTP Accept headers (Accept, Accept-Language, Accept-Charset,
    Accept-Encoding) and rationalises them against the parameters acceptable by the
    server; it then makes a recommendation as to the appropriate response format.
    
    This version of the Negotiator also supports the SWORDv2 extensions to HTTP Accept
    in the form of Accept-Packaging.

    Forked from https://pypi.python.org/pypi/negotiator/1.0.0
    """,
    license = 'CC0',
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

