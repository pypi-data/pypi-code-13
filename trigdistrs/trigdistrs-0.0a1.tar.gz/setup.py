# -*- coding: utf-8 -*-

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(                                    \
    name = "trigdistrs",                  \
    version = "0.0a1",                    \
    description = 
        "Trigonometric Probability Distributions "
        "(see Souza 2016: NEW TRIGONOMETRIC CLASSES"
        " OF PROBABILISTIC DISTRIBUTIONS, PhD Thesis"
        "available at http://goo.gl/Z6nbJz)."
        "\n"
        "Uses symbolic computing with sympy.stats.",
    long_description = 
        "Probability distributions are elements of "
        "measure theory and general statistics,"
        "providing standardized formulas to compute"
        "odds of events happening."
        "\n"
        "This package presents new probability "
        "distributions produced by skewing regular"
        "distribution using trigonometric functions."        
        "\n"        
        "References:\n"
        "* http://goo.gl/Z6nbJz\n"
        "* CosW: https://cran.r-project.org/web/packages/CosW/index.html\n"
        "* SecKW: https://cran.r-project.org/web/packages/SecKW/index.html\n"
        "* SinIW: https://cran.r-project.org/web/packages/SinIW/index.html\n"
        "* TanB: https://cran.r-project.org/web/packages/TanB/index.html\n",
    classifiers = [
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "License :: DFSG approved",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research"
      ],
    keywords="Statistics Probability Distribution",
    url = "https://github.com/TrigonometricDistribution",
    author = "Lucas M. Soares Gallindo",
    author_email = "lucas.soares@ufpe.br",
    license = "GPLv3+",
    packages = ["trigdistrs"],
    install_requires = [
        "sympy",
    ],
    test_suite = "nose.collector",
    tests_require = ["nose"],
    include_package_data = True,
    zip_safe = False)