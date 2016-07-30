# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
#  Copyright (c) 2016, Robert Whitinger <cva_account@wmkt.com>
#
#  Distributed under the terms of the LGPL license either version 2.1 or
#  (at your option) any later version.
#
#  The full license is in the file LICENSE.txt, distributed with this software,
#  and is also available at <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------
"""
cva -- Calculus of Variations
=============================

The cva library (pronounced see-va) implements a solver for problems
in the domain of the calculus of variations.  This includes such
problems as finding geodesics on arbitrary surfaces, finding minimal
paths in curved spacetime, or basically any path minimization problem
that can be defined in terms of a surface or hypersurface model with an
attached metric.

Quickstart
----
import cva
cva.examples.case01_torus()
----

Provides:
  1. Models
  2. Metrics
  3. Views
  4. Solver

Documentation:
  1. The mathematical foundations on which the cva library is based:

  Whitinger, Robert, "An Algorithm for the Machine Calculation of Minimal Paths" (2016). 
    Electronic Theses and Dissertations. Paper 3119.   http://dc.etsu.edu/etd/3119

  Download pdf: http://dc.etsu.edu/cgi/viewcontent.cgi?article=4521&context=etd

  2. Docstrings are provided with the library functions
  3. Runable examples are provided as starting points

"""

__all__ = ('model', 'metric', 'solve', 'view', 'examples')

from ._version import __version__
from . import model
from . import metric
from . import solve
from . import view
from . import examples
from . import test
