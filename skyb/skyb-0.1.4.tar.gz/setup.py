from setuptools import setup, find_packages

setup(
    name='skyb',
    packages=find_packages(exclude=['test', 'ez_setup']),
    license='MIT',
    version='0.1.4',
    description='skypiea base',
    author='woshifyz',
    author_email='monkey.d.pandora@gmail.com',
    url='https://github.com/woshifyz/skyb',
    download_url='https://github.com/woshifyz/skyb/tarball/0.1.4',
    keywords=['skypiea', 'base'],
    classifiers=[],
    entry_points=dict(
        console_scripts=[
            'skyf = skyb.quick.flyway:main',
        ],
    ),
    include_package_data=True,
)
