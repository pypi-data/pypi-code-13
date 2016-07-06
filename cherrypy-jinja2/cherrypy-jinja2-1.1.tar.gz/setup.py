from setuptools import setup
setup(
    name='cherrypy-jinja2',
    version='1.1',

    description="CherryPy tool to render jinja2 templates",
    url="https://bitbucket.org/gclinch/cherrypy-jinja2",
    license='Apache License, Version 2.0',

    author='Graham Clinch',
    author_email='g.clinch@lancaster.ac.uk',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: CherryPy',
        'License :: OSI Approved :: Apache Software License'],

    packages=['cherrypy_jinja2'],
    install_requires=['CherryPy', 'Jinja2'],
)
