from setuptools import setup

setup(
    name='gbdxcli',
    version='0.0.4',
    description='GBDX command line interface.',
    classifiers=[],
    keywords='',
    author='Donny Marino',
    author_email='dmarino@digitalglobe.com',
    url='https://github.com/DigitalGlobe/gbdxcli',
    license='MIT',
    install_requires=[
        'Click',
        'gbdxtools',
        'gbdx-auth'
    ],
    packages=['gbdxcli'],
    entry_points='''
        [console_scripts]
        gbdx=gbdxcli.commands:cli
    '''

)


