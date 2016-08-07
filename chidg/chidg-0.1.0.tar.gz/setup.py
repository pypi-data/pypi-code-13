from setuptools import setup



setup(
      name='chidg',
      version='0.1.0',
      description='A Chimera-based, discontinuous Galerkin solver',
      long_description='A framework for solving partial differential equations using the discontinuous Galerkin discretization and Chimera overset grids. The framework includes a finite element library along with nonlinear and linear solvers, preconditioners and temporal advancement algorithms',
      url='https://github.com/nwukie/ChiDG',
      author='Nathan A. Wukie',
      author_email='nwukie@gmail.com',
      license='BSD 3-Clause',
      keywords='finite element DG galerkin chimera',
      scripts=['chidg.py']
      )
