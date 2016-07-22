from distutils.core import setup

setup(
    name = 'yandc',
    packages = ['yandc_base', 'yandc_snmp', 'yandc_ssh', 'yandc_ros'],
    requires = ['paramiko', 'pysnmp'],
    version = '0.2a',
    description = 'Yet Another Networked Device Client module',
    author = 'Matt Ryan',
    author_email = 'inetuid@gmail.com',
    url = 'https://github.com/inetuid/yandc',
    download_url = 'https://github.com/inetnet/yandc/tarball/0.2',
    classifiers = [],
)
