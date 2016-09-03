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
A textual iteration context.
Part of the speed package.
"""

import sys, time
from base import IterationContextBase

# -------------------------------------------------------------------

class TextualIterationContext(IterationContextBase):
    NAME = 'text'
    
    def __init__(self, it, level):
        IterationContextBase.__init__(self, it, level)
        self._last_output_len = 0
    
    def update(self, elem):
        if self._level == 0:
            est = self._it.estimate_remaining()
            fraction, iter_rate, elapsed_time, remaining_time = est
            
            n = self._it._last_update[0]
            elapsed_str = self._format_time(elapsed_time)
            
            if self._it._len is None:
                # length unknown
                s = "%d/? [elapsed: %s left: ?, %5.2f iters/sec]" \
                    % (n, elapsed_str, iter_rate)
            
            else:
                # length known
                max_n = len(self._it)
                width = len(str(max_n))
                percent = int(100 * fraction)
                left_str = self._format_time(remaining_time)

                tmp = int(10 * fraction)
                bar = "|" + "#" * tmp + "-" * (10 - tmp) + "|"
                s = "%s%*d/%*d %3d%% [elapsed: %s left: %s, %5.2f iters/sec]" \
                    % (bar, width, n, width, max_n, percent,
                       elapsed_str, left_str, iter_rate)
            
            s = s[:80]
            sys.stdout.write("\r%-*s\r" % (self._last_output_len, s))
            sys.stdout.flush()
            self._last_output_len = len(s)
    
    def cleanup(self):
        if self._level == 0:
            sys.stdout.write("\r%*s\r" % (self._last_output_len, ""))
            sys.stdout.flush()

    def _format_time(secs):
        gm = time.gmtime(secs)
        if secs < 60*60:
            return time.strftime("%M:%S", gm)
        else:
            res = time.strftime("%H:%M:%S", gm)
            days = secs // (60*60*24)
            if days:
                res = "%dd " % days + res
            return res
    _format_time = staticmethod(_format_time)
