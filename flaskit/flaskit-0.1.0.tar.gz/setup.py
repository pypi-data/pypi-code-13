from setuptools import setup

ver = '0.1.0'

setup(
    name='flaskit',
    packages=['flaskit'],
    version=ver,
    description=r'''Utilies for Flask application.''',
    author='Giang Manh',
    author_email='manhgd@yahoo.com',
    url='https://github.com/manhg/flaskit',
    download_url='https://github.com/manhg/flaskit/tarball/' + ver,
    keywords=['web', 'flask'],
    install_requires = [
        "Flask"
    ],
    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)
