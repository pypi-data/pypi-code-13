from setuptools import setup, find_packages

setup(
    name='POC-T',
    version='1.7.2',
    keywords=('pentest', 'concurrent', 'toolkit'),
    description='POC-T: Pentest Over Concurrent Toolkit',
    license='GPL v2',
    install_requires=['gevent', 'requests', 'shodan'],

    author='cdxy',
    author_email='i@cdxy.me',

    packages=find_packages(),
    platforms='any',
)
