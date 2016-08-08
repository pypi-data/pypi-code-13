from setuptools import setup, find_packages

setup(
    name = 'PlotDraw',
    version = '0.0.1',
    keywords = ('Matplotlib', 'Draw'),
    description = 'interface of Matplotlib',
    license = 'MIT License',
    install_requires = ['matplotlib', 'numpy', 'xlrd', 'brewer2mpl'],

    author = 'lwj0012',
    author_email = 'lwj0012@gmail.com',

    packages = find_packages(),
    platforms = 'any',
)
