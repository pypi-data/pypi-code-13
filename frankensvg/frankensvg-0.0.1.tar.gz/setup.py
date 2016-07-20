from setuptools import setup, find_packages

setup(
    name="frankensvg",
    version="0.0.1",
    url='http://github.com/hodgestar/frankensvg',
    license='MIT',
    description="Generate an SVG from a YAML description",
    long_description=open('README.md', 'r').read(),
    author='Simon Cross',
    author_email='hodgestar@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'svgwrite',
        'PyYAML',
        'click',
    ],
    entry_points='''
    [console_scripts]
    frankensvg = frankensvg.cli:cli
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
