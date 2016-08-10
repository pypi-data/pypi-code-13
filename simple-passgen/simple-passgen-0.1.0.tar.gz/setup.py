from setuptools import setup, find_packages


setup(
    name='simple-passgen',
    version='0.1.0',
    author='Joseph Murphy',
    author_email='air.jmurph+simple-passgen@gmail.com',
    url='https://github.com/JMurph2015/simple-passgen',
    description='Generate secure random character sequences, not inspired by XKCD',
    long_description=open('README.md').read(),
    packages=find_packages(),
    zip_safe=False,
    license='MIT',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'passgen = passgen.simple_passgen:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
)
