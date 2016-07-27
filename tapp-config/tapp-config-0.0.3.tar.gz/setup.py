from setuptools import setup

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries",
]

# Cut the readme before the second section start.
readme = open('./README.rst').read()
url = 'https://github.com/gitguild/tapp-config'
top = readme.find('Usage\n-----')
bottom = readme.find('.. |Build Status|')
more = ("Visit {} to see the full README, the\n"
        "issue tracker, and others.\n\n\n")
readme = readme[:top] + more.format(url) + readme[bottom:]

setup(
    name='tapp-config',
    version='0.0.3',
    py_modules=['tapp_config'],
    url=url,
    long_description=readme,
    license='MIT',
    classifiers=classifiers,
    author='Ira Miller',
    author_email='ira@gitguild.com',
    description='Configuration for tapps (redis, logger, etc.)',
    setup_requires=['pytest-runner'],
    install_requires=[
        'redis'
    ],
    tests_require=['pytest', 'pytest-cov']
)
