# Copyright (C) 2016 Pier Carlo Chiodi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Formatter(object):

    ID = None

    @staticmethod
    def add_args(parser):
        pass

    def __init__(self, args):
        self.args = args

    # The main program calls the init() function first;
    # if it returns True, it processes the block lists
    # entries and then it calls emit().

    def init(self):
        return True

    def emit(self, entries, output):
        raise NotImplementedError()
