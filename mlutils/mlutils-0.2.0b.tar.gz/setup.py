#!/usr/bin/env python

from distutils.core import setup
import wheel

description = """ Collection of utilities for machine learning and AI planning and not-supervised learning. Development is in progress. """

long_description = """
mlutils package is collection of various utilities for machine learning and AI planning. 
  -- N-Ary tree class supported various search algorithms: pre-order, post-order, breadth-first 
     heuristic (you should provide heuristic function) and random sampling. 
  -- State space generation/search.
  -- Basic graph class. Implements generic directed graph.
  -- Finite automata graph. Implements discrete finite automata state machine on base of BasicGraph class.
  -- Processing graph. Implements network of asynchronius processing units, running in separate threads. 
     Intended to be used as complex pipeline (pipenet) for machne learning or data processing.
  
Dependency:
   Package does not have extra dependencies except python standard library 
  
Installation:
   Standard installation for pure python modules
   
Usage examples:
   Each modute has test() function which implement brif self-testing and may serve as usage example       
"""

classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: BSD License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',   
],

setup(
      name = "mlutils",
      version = "0.2.0b",
      description = description,
      long_description=long_description,
      author = "Mark Eremeev",
      author_email = "m.eremeev@gmail.com",
      license = "BSD",
      url = "https://gitlab.com/m.eremeev/mlutils",
      packages=["mlutils"],    
      py_modules=[],
      keywords = "state space search, AI planning, machine learning pipeline, state machine, finite automaton"
    )
