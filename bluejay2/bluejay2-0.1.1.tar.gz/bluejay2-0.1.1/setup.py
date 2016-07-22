from setuptools import setup

setup(
    name='bluejay2',
    version='0.1.1',
    py_modules=['bluejay'],
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
    ],
    description='Client for Nibiru',
    author='Dinesh Weerapurage',
    author_email='dinesh.weerapurage@pearson.com',
    entry_points='''
        [console_scripts]
        bluejay=bluejay:cli
    ''',
)
