from setuptools import setup

setup(
    name='bluejay2',
    version='0.1',
    py_modules=['bluejay'],
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        bluejay=bluejay:cli
    ''',
)
