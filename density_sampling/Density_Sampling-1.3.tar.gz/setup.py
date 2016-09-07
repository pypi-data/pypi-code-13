#!/usr/bin/env python


# Density_Sampling/setup.py;

# Author: Gregory Giecold for the GC Yuan Lab
# Affiliation: Harvard University
# Contact: g.giecold@gmail.com, ggiecold@jimmy.harvard.edu


"""Setup script for Density_Sampling. For a dataset comprising a mixture 
of rare and common populations, density sampling gives equal weights 
to selected representatives of those distinct populations.

Density sampling is a balancing act between signal and noise, for while 
it increases the prevalence of rare populations, it also increases the prevalence 
of noisy sample points which happen to have their local densities larger than
an outlier density computed by Density_Sampling.

Reference
---------
Giecold, G., Marco, E., Trippa, L. and Yuan, G.-C.,
"Robust Lineage Reconstruction from High-Dimensional Single-Cell Data". 
ArXiv preprint [q-bio.QM, stat.AP, stat.CO, stat.ML]: http://arxiv.org/abs/1601.02748
"""


from codecs import open
from os import path
from sys import version
from setuptools import setup
    
    
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README'), encoding = 'utf-8') as f:
    long_description = f.read()
    

setup(name = 'Density_Sampling',
      version = '1.3',
      
      description = 'For a dataset comprising a mixture of rare and common populations, density sampling gives equal weights to the representatives of those distinct populations.',
      long_description = long_description,
                    
      url = 'https://github.com/GGiecold/Density_Sampling',
      download_url = 'https://github.com/GGiecold/Density_Sampling',
      
      author = 'Gregory Giecold',
      author_email = 'g.giecold@gmail.com',
      maintainer = 'Gregory Giecold',
      maintainer_email = 'ggiecold@jimmy.harvard.edu',
      
      license = 'MIT License',
      
      platforms = ('Any',),
      install_requires = ['numpy>=1.9.0', 'setuptools', 'sklearn'],
                          
      classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',          
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Visualization',
                   'Topic :: Scientific/Engineering :: Mathematics', ],
                   
      packages = ['Density_Sampling'],
      package_dir = {'Density_Sampling': 'src/Density_Sampling'}, 
      
      include_package_data = True,
      #package_data = {
      #    'Density_Sampling':
      #        ['FLANN/bin/*.py',
      #         'FLANN/bin/*.sh',
      #         'FLANN/bin/*.cfg',
      #         'FLANN/cmake/*.txt',
      #         'FLANN/cmake/*.in',
      #         'FLANN/cmake/*.cmake',
      #         'FLANN/COPYING',
      #         'FLANN/ChangeLog',
      #         'FLANN/CMakeLists.txt',
      #         'FLANN/README.md',
      #         'FLANN/examples/*.txt',
      #         'FLANN/examples/*.cpp',
      #         'FLANN/examples/*.c',
      #         'FLANN/examples/README',
      #         'FLANN/doc/*.txt',
      #         'FLANN/doc/*.pdf',
      #         'FLANN/doc/*.tex',
      #         'FLANN/doc/*.bib',
      #         'FLANN/doc/images/*.png',
      #         'FLANN/src/*.txt',
      #         'FLANN/src/cpp/*.txt',
      #         'FLANN/src/cpp/flann/*.h'
      #         'FLANN/src/cpp/flann/*.hpp',
      #         'FLANN/src/cpp/flann/*.cpp',
      #         'FLANN/src/cpp/flann/*.in',
      #         'FLANN/src/cpp/flann/algorithms/*.h',
      #         'FLANN/src/cpp/flann/mpi/*.h',
      #         'FLANN/src/cpp/flann/mpi/*.cpp',
      #         'FLANN/src/cpp/flann/util/*.h',
      #         'FLANN/src/cpp/flann/util/cuda/*.h',
      #         'FLANN/src/cpp/flann/io/*.h',
      #         'FLANN/src/cpp/flann/nn/*.h',
      #         'FLANN/src/matlab/*.txt',
      #         'FLANN/src/matlab/*.m',
      #         'FLANN/src/matlab/*.cpp',
      #         'FLANN/src/python/*.txt',
      #         'FLANN/src/python/*.tpl',
      #         'FLANN/src/python/pyflann/*.py',
      #         'FLANN/test/*.txt',
      #         'FLANN/test/*.cpp',
      #         'FLANN/test/*.cu',
      #         'FLANN/test/*.h',
      #         'FLANN/test/*.py',
      #        ],
      #},
)

