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
Infrastructure for speed iterators.
Part of the speed package.

defines basic interation classes
"""

from __future__ import generators
import time, weakref

__all__ = ['IteratorWrapper', 'BetterEstimatingIteratorWrapper',
           'IterationContextBase', 'IterationManager']

# --------------------------------------------------------------------------

class IteratorWrapper(object):
    BEGIN_AFTER  = 3    # seconds
    UPDATE_EVERY = 0.5  # seconds
    
    # O.S.: I didn't want to add the repr argument here,
    # But it was the only way to do it without completely changing the design...
    def __init__(self, iterable, manager=None, size=None, repr=None):
        self._iterable = iterable
        if size is None:
            try:
                size = len(iterable)
            except TypeError:
                # No length for the iterable
                pass
        self._len = size
        self._manager = manager
        if self._manager is not None:
            if repr:
                self._manager.register(self, repr)
            else:
                self._manager.register(self)

    def __del__(self):
        self.cleanup_iteration()

    def __len__(self):
        if self._len is None:
            raise TypeError, "len() of unsized object"
        else:
            return self._len

    def __repr__(self):
        name = self.__class__.__name__
        if self._len:
            return '<%s (len=%d) of %r>' % (name, self._len, self._iterable)
        else:
            return '<%s of %r>' % (name, self._iterable)

    def __iter__(self):
        try:
            n = 0
            self.init_iteration()
            for elem in self._iterable:
                t = time.time()
                if t - self._last_update[1] > self.UPDATE_EVERY:
                    self._last_update = n, t
                    self.update_iteration(elem)
                yield elem
                n += 1
        except KeyboardInterrupt:
            self.cleanup_iteration()
            raise
    
    #
    # overload these in descendants
    #
    def init_iteration(self):
        self._init_time = time.time()
        self._last_update = (0,0)
    
    def cleanup_iteration(self):
        if self._manager is not None:
            self._manager.unregister(self)
            self._manager = None
    
    def update_iteration(self,elem):
        # last update index and time are kept in self._last_update
        if self._manager is not None:
            self._manager.update(self, elem)

    # returns (fraction, iter_rate, elapsed_time, remaining_time)
    def estimate_remaining(self):
        n, t = self._last_update
        elapsed_time = t - self._init_time
        iter_rate = n / elapsed_time # maybe check for DivideByZero
        
        if self._len <= 0 or not n:
            fraction = 0.
            remaining_time = 0.
        else:
            fraction = float(n) / self._len
            projected_time = elapsed_time / fraction
            remaining_time = projected_time - elapsed_time
        
        return fraction, iter_rate, elapsed_time, remaining_time

# --------------------------------------------------------------------------

class BetterEstimatingIteratorWrapper(IteratorWrapper):
    def init_iteration(self, *args):
        IteratorWrapper._init_iteration(self, *args)
        self._timestamps = [(0, self._init_time)]

    def update_iteration(self, elem):
        IteratorWrapper.update_iteration(self, elem)
        # cache O(log2(len(self))) timestamps
        if 1 + 2 * self._last_update[0] >= (1 << len(self._timestamps)):
            self._timestamps.append(self._last_update)

    def estimate_remaining(self):
        raise NotImplementedError

# --------------------------------------------------------------------------

class IterationContextBase(object):
    NAME = 'none'

    def __init__(self, it, level):
        self._level = level
        self._it = weakref.proxy(it)

    def __del__(self):
        self.cleanup()

    def update(self, elem):
        pass

    def cleanup(self):
        pass

# --------------------------------------------------------------------------

class IterationManager(object):
    def __init__(self, IterationContext):
        assert issubclass(IterationContext, IterationContextBase)
        self._iter_context_type = IterationContext
        self._iterations = []
        self._iter_contexts = weakref.WeakKeyDictionary()
    
    def __len__(self):
        return len(self._iterations)

    def __repr__(self):
        result = ["<IterationManager: %d iterations in progress>" % len(self)]
        for ctx in self._iterations:
            result.append("%d) %r" % (ctx._level, ctx._it))
        return "\n".join(result)

    def register(self, it, *args):
        assert it not in self._iter_contexts

        level = len(self._iterations)
        context = self._iter_context_type(it, level, *args)
        self._iterations.append(context)
        self._iter_contexts[it] = context

    def unregister(self, it):
        it2 = self._iterations.pop()
        #assert it2 is self._iter_contexts(it)
        #del self._iter_contexts[it]
        if it in self._iter_contexts:
            del self._iter_contexts[it]

    def update(self, it, elem):
        # BEGIN_AFTER should only affect level 0
        ctx = self._iter_contexts[it]
        if ctx._level or it._last_update[1] > it._init_time + it.BEGIN_AFTER:
            ctx.update(elem)

    def set_context(self, IterationContext):
        assert issubclass(IterationContext, IterationContextBase)
        if self._iter_context_type is IterationContext:
            return # no need to argue

        other = IterationManager(IterationContext)
        for ctx in self._iterations:
            other.register(ctx._it)

        self._iterations        = other._iterations
        self._iter_contexts     = other._iter_contexts
        self._iter_context_type = other._iter_context_type
