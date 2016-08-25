from setuptools import setup, find_packages

setup(
	name			='SiteLinksCheck',
    version			='0.0.1',
    url				='https://github.com/Manideepto/SiteLinksCheck',
    description		='Given an url it returns all the links, broken links, internal links etc.',
    long_description='Given an url it returns all the 1.links 2.Internal Links 3.Internal broken links 4.Broken Links as a list.',
    author			='Manideepto',
    author_email	='dasmanideepto@gmail.com',
    license			='MIT',
    keywords		='Broken Links, URL, Site Links Check',
    platforms		='any',
    classifiers		=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    packages		=find_packages(),
)
