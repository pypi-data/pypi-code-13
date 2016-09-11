# -*- coding: utf-8 -*-
from setuptools import setup, Extension

setup(
    name='automodel-server',
    version='0.1.14',
    url='https://bitbucket.org/jlalmeidaf/automodel-server-with-hmmer',
    license='',
    author='João Luiz de Almeida Filho, Jorge Hernandez Fernandez',
    author_email='joaoluiz.af@gmail.com',
    keywords='protein modeling modeller automodel',
    description=u'Server of service for structure protein prediction',
    packages=['AutomodelServerModules', 'modellerstep', 'modellingfile', 'pdb',  'tests'],
    install_requires=['argparse', 'biopython', 'rpyc', 'matplotlib'],
    package_data={'pdb': ['pdb_95.pir, pdb_95.bin']},
    include_package_data=True,
    scripts=['server.py']
)
