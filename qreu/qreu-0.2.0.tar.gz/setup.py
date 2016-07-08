from setuptools import setup, find_packages


setup(
    name='qreu',
    version='0.2.0',
    packages=find_packages(),
    url='https://github.com/gisce/qreu',
    install_requires=[
        'flanker'
    ],
    license='MIT',
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    description='EMail Wrapper'
)
