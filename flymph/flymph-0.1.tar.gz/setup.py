from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'readme.rst')).read()
NEWS = open(os.path.join(here, 'news.txt')).read()


version = '0.01'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'flask',
    'lymph',
]


setup(name='flymph',
    version=version,
    description="Flask as Lymph Web API",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='flask lymph web-api',
    author='Srinivas Devaki',
    author_email='mr.eightnoteight@gmail.com',
    url='https://github.com/eightnoteight/flymph',
    license='MIT License',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['flymph=flymph:main']
    }
)

