# This file is part of PySpeed - flexible progress bars for Python
# Written in August 2005
# Copyright (c) 2010 Rani Hod
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""
The speed package: wraps iterators for progress tracking.
Can also replace built-in xrange().
"""

import sys, os, __builtin__, __main__

from base import *
from context import TextualIterationContext

__all__ = ['speedConfig', 'speed', 'xrange',
           'progress', 'trange', 'gprogress', 'grange', 'bprogress']

theManager = IterationManager(TextualIterationContext)

def speedConfig(mode=None, vis=None, delay=None, refresh=None):
    """
    Configure the speed package.

    mode can be one of the following:
    'auto' - replace the built-in xrange()
    'manual' - use speed.xrange explicitly or speed.speed() to wrap iterators.
              [default]

    vis can be one of the following:
    'none' - disable the progress indicator
    'text' - a single-line textual progress indicator
    'graph' - a graphical progress indicator

    delay is the minimum time (in seconds) after which the progress
    indicator is shown [default = 3 seconds]

    refresh is the minimum elapsed time (in seconds) between progress
    indicator visual updates [default = 0.5 seconds].
    """
    anything_changed = False

    if mode is None:
        pass
    elif mode == 'auto':
        anything_changed = True
        __main__.xrange = sys.modules['speed'].xrange
    elif mode == 'manual':
        anything_changed = True
        try:
            del __main__.xrange
        except AttributeError:
            # Mode is already manual
            pass
    else:
        raise ValueError, "mode must be 'auto' or 'manual'"

    if vis is None:
        pass
    elif vis == 'none':
        anything_changed = True
        theManager.set_context(IterationContextBase)
    elif vis == 'text':
        anything_changed = True
        theManager.set_context(TextualIterationContext)
    elif vis == 'graph':
        anything_changed = True
        from gtk_widget import GTKIterationContext
        theManager.set_context(GTKIterationContext)
    else:
        raise ValueError, "vis must be 'none', 'text' or 'graph'"

    if delay is None:
        pass
    elif not isinstance(delay, (int, float)):
        raise TypeError, "delay must be non-negative"
    else:
        anything_changed = True
        IteratorWrapper.BEGIN_AFTER = delay

    if refresh is None:
        pass
    elif not isinstance(refresh, (int, float)):
        raise TypeError, "refresh must be an integer or a floating-point number"
    elif refresh < 0.05:
        raise ValueError, "refresh must be at least 0.05"
    else:
        anything_changed = True
        IteratorWrapper.UPDATE_EVERY = refresh

    if not anything_changed:
        mode_is_auto = getattr(__main__, 'xrange', None) is sys.modules['speed'].xrange
        print 'mode = %s' % ('auto' if mode_is_auto else 'manual')
        print 'vis = %s' % theManager._iter_context_type.NAME
        print 'delay = %.1f seconds' % IteratorWrapper.BEGIN_AFTER
        print 'refresh = %.1f seconds' % IteratorWrapper.UPDATE_EVERY

def speed(iterable, size=None):
    """
    Speed wrapper for a generic iterable.
    If a size is not given it will be taken from the iterable.
    """
    if not isinstance(iterable, IteratorWrapper):
        iterable = IteratorWrapper(iterable, theManager, size)
    return iterable

def xrange(*args):
    """
    speed wrapper for xrange.

    xrange([start,] stop[, step]) -> xrange object

    Like range(), but instead of returning a list, returns an object that
    generates the numbers in the range on demand. This is slightly slower
    than range() but more memory efficient.
    """
    
    return speed(__builtin__.xrange(*args))


progressManager = IterationManager(TextualIterationContext)
def progress(iterable, delay=0, refresh=None, size=None):
    """
    Speed textual wrapper for a generic iterable.
    Ignores the settings set by speedConfig and is always textual.
    """
    if not isinstance(iterable, IteratorWrapper):
        iterable = IteratorWrapper(iterable, progressManager, size)

    if delay is not None:
        iterable.BEGIN_AFTER = delay

    if refresh is not None:
        iterable.UPDATE_EVERY = refresh

    return iterable

def trange(*args):
    """
    speed textual wrapper for xrange.
    """
    return progress(__builtin__.xrange(*args))


# Don't import GTK unless required
gprogressManager = None
def gprogress(iterable, delay=0, refresh=None, size=None, repr=None):
    """
    speed graphic wrapper for a generic iterable.
    Ignores the settings set by speedConfig and is always graphic.
    """
    global gprogressManager
    if gprogressManager is None:
        from gtk_widget import GTKIterationContext
        gprogressManager = IterationManager(GTKIterationContext)
    if not isinstance(iterable, IteratorWrapper):
        iterable = IteratorWrapper(iterable, gprogressManager, size, repr=repr)

    if delay is not None:
        iterable.BEGIN_AFTER = delay
    if refresh is not None:
        iterable.UPDATE_EVERY = refresh
    return iterable

def grange(*args):
    """
    speed graphic wrapper for xrange
    """
    return gprogress(__builtin__.xrange(*args))

def bprogress(*args, **kwargs):
    """
    frozen-bubble progress
    """
    a = os.system('frozen-bubble -nm&')
    return progress(*args, **kwargs)

