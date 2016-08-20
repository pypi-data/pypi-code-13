from setuptools import setup, find_packages

setup(
    name='flask-admin-barin',
    version='0.0.1',
    description='A Barin backend for Flask-Admin',
    long_description='Some restructured text maybe',
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Rick Copeland',
    author_email='rick@arborian.com',
    url='',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    tests_require=[],
    entry_points="""
    [console_scripts]
    """)
