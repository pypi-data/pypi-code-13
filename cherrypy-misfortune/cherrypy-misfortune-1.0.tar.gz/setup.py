from setuptools import setup
setup(
    name='cherrypy-misfortune',
    version='1.0',

    description=(
        "CherryPy tool that causes requests to stall or fail with the aim of "
        "assisting the development of robust consumers"),
    url="https://bitbucket.org/gclinch/cherrypy-misfortune",
    license='Apache License, Version 2.0',

    author='Graham Clinch',
    author_email='g.clinch@lancaster.ac.uk',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: CherryPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License'],

    packages=['cherrypy_misfortune'],
    install_requires=['CherryPy'],
)
