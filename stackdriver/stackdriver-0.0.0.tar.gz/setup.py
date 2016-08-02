from setuptools import setup

setup(
    name='stackdriver',
    version='0.0.0',
    author='Mihir Singh (@citruspi)',
    author_email='hello@mihirsingh.com',
    description='A Python client for the Stackdriver service',
    url='https://github.com/citruspi/py-stackdriver',
    classifiers=[
        'License :: Public Domain',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Monitoring',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X'
    ],
    scripts=[
        'scripts/stackdriver'
    ],
    packages=['stackdriver'],
    zip_safe=False,
    include_package_date = True,
    platforms = 'any',
    install_requires = [
        'requests'
    ]
)
