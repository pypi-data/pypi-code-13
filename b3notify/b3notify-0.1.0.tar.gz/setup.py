from setuptools import setup

setup(
    name='b3notify',
    version='0.1.0',
    py_modules=['b3notify'],
    include_package_data=True,
    install_requires=[
        'click',
        'requests==2.3.0'
    ],
    description='Build status notifier for bitbucket server',
    author='Dinesh Weerapurage',
    author_email='dinesh.weerapurage@pearson.com',
    entry_points='''
        [console_scripts]
        b3notify=b3notify:cli
    ''',
)
