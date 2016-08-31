from setuptools import setup, find_packages

setup(
    name = 'centiment_alpha',
    version = '0.0.29',
    keywords = ('SO-CAL'),
    description = '[alpha test] SO-CAL sentiment motified for tweets.',
    license = 'MIT License',
    install_requires = ['nltk'],
    include_package_data = True,
    zip_safe = True,

    author = 'cchen224',
    author_email = 'phantomkidding@gmail.com',

    packages = find_packages(),
    platforms = 'any',
)