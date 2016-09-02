# Copyright (C) 2016 Anne Mulhern
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# Anne Mulhern <mulhern@cs.wisc.edu>

""" Test utilities. """

from __future__ import absolute_import

import itertools

from justbases_string import BaseConfig
from justbases_string import DigitsConfig
from justbases_string import StripConfig

from hypothesis import strategies


def build_nat(base, max_len):
    """
    Build a well-formed nat strategy from ``base``.
    """
    ints = strategies.integers(min_value=0, max_value=(base - 1))
    nats = strategies.lists(ints, min_size=1, max_size=max_len)
    return \
       nats.map(lambda l: list(itertools.dropwhile(lambda x: x == 0, l)))

def build_base(max_base):
    """
    Builds a base.

    :param int max_base: the maximum base
    """
    return strategies.integers(min_value=2, max_value=max_base)

def build_nat_with_base(max_base, max_len):
    """
    Builds a nat and its base.
    :param int max_base: the maximum base
    :param int max_len: the maximum number of digits in the nat

    :returns: a strategy from which can be drawn a pair, a nat and its base
    """
    return build_base(max_base).flatmap(
       lambda n: strategies.tuples(
          build_nat(n, max_len),
          strategies.just(n)
       )
    )


def build_sign():
    """
    Build a sign value.
    """
    return strategies.integers(min_value=-1, max_value=1)

build_relation = build_sign

def build_digits_config():
    """
    Build an arbitrary digits config.
    """
    return strategies.builds(
       DigitsConfig,
       separator=strategies.characters(),
       use_caps=strategies.booleans(),
       use_letters=strategies.booleans()
    )

def build_strip_config():
    """
    Build strip config.
    """
    return strategies.builds(
       StripConfig,
       strategies.booleans(),
       strategies.booleans(),
       strategies.booleans()
    )

def build_base_config():
    """
    Build base config.
    """
    return strategies.builds(
       BaseConfig,
       strategies.booleans(),
       strategies.booleans()
    )
