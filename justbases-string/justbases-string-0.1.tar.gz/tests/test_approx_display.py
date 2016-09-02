""" Test manipulations to show approximation. """

import unittest

from justbases_string import ApproxPrefix

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

class TestApproxPrefix(unittest.TestCase):
    """
    Test calculation of approximation prefix.
    """

    @given(
       strategies.fractions().filter(lambda x: x > -1 and x < 1),
       strategies.lists(
          elements=strategies.fractions().filter(lambda x: x > 0 and x < 1),
          max_size=3
       ).map(sorted)
    )
    @settings(max_examples=50)
    def testXformValue(self, relation, limits):
        """
        Make sure xform() yields the correct sort of characters.
        """
        result = ApproxPrefix(limits).xform(relation, '')
        if relation == 0:
            assert result == ''
        elif relation < 0:
            assert result.startswith('>')
        elif relation > 0:
            assert result.startswith('<')

    @given(
       strategies.fractions().filter(lambda x: x > -1 and x < 1),
       strategies.lists(
          elements=strategies.fractions().filter(lambda x: x > 0 and x < 1),
          max_size=3
       ).map(sorted)
    )
    @settings(max_examples=50)
    def testXformMagnitude(self, relation, limits):
        """
        Make sure xform() yields the correct amount of characters.
        """
        result = ApproxPrefix(limits).xform(relation, '')
        if relation == 0:
            assert result == ''
        else:
            num_chars = len(result) - 1
            abs_relation = abs(relation)
            assert (num_chars == len(limits) + 1 and \
               (limits == [] or abs_relation >= limits[-1])) or \
               abs_relation < limits[num_chars - 1]
