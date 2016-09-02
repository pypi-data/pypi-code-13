# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# Author: Anne Mulhern <mulhern@cs.wisc.edu>

""" Test for utility functions. """

import string
import unittest

from justbases_string import BaseDisplayError
from justbases_string import DisplayConfig
from justbases_string import String
from justbases_string import StripConfig

from justbases_string._string import Digits
from justbases_string._string import Number
from justbases_string._string import Strip

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from ._utils import build_base
from ._utils import build_base_config
from ._utils import build_digits_config
from ._utils import build_nat
from ._utils import build_nat_with_base
from ._utils import build_relation
from ._utils import build_sign
from ._utils import build_strip_config


class TestDigits(unittest.TestCase):
    """
    Test Digits methods.
    """

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(BaseDisplayError):
            Digits(
               DisplayConfig().digits_config,
               Digits.MAX_SIZE_BASE_FOR_CHARS + 1
            )

    @given(
       build_digits_config(),
       build_nat_with_base(Digits.MAX_SIZE_BASE_FOR_CHARS, 10)
    )
    @settings(max_examples=50)
    def testChars(self, config, subject):
        """
        Test transformation to string of chars.
        """
        (number, base) = subject
        digits = Digits(config, base)
        result = digits.xform(number)

        def excludes(forbidden):
            """
            Verify that unused letters are excluded unless used as separator.
            """
            self.assertTrue(
               config.separator in forbidden or set(result) & forbidden == set()
            )

        if config.use_caps:
            excludes(set(string.ascii_lowercase))
        else:
            excludes(set(string.ascii_uppercase))

        if not config.use_letters:
            excludes(set(string.ascii_lowercase + string.ascii_uppercase))

        if base > 10 and not config.use_letters and len(number) > 1:
            self.assertIn(config.separator, result)


class TestNumber(unittest.TestCase):
    """
    Test Number.
    """

    @given(
       strategies.text(alphabet=strategies.characters(), max_size=10),
       strategies.text(
          alphabet=strategies.characters(),
          min_size=1,
          max_size=10
       ),
       strategies.text(alphabet=strategies.characters(), max_size=10),
       build_base_config(),
       build_base(16),
       build_sign()
    )
    @settings(max_examples=100)
    def testXform(
       self,
       integer_part,
       non_repeating_part,
       repeating_part,
       config,
       base,
       sign
    ):
        """
        Test xform.
        """
        # pylint: disable=too-many-arguments

        result = Number(config, base).xform(
           integer_part,
           non_repeating_part,
           repeating_part,
           sign
        )
        if config.use_prefix and base == 16 and sign != -1:
            self.assertTrue(result.startswith('0x'))
        if config.use_prefix and base == 8 and sign != -1:
            self.assertTrue(result.startswith('0'))
        if config.use_subscript:
            base_str = str(base)
            self.assertEqual(
               result.rfind(base_str) + len(base_str),
               len(result)
            )


class TestStrip(unittest.TestCase):
    """
    Test Strip.
    """

    @given(
       build_nat(10, 3),
       build_strip_config(),
       build_relation(),
       build_base(16),
    )
    @settings(max_examples=100)
    def testXform(self, number, config, relation, base):
        """
        Confirm that option strip strips more than other options.
        """
        result = Strip(config, base).xform(number, relation)
        most = Strip(StripConfig(strip=True), base).xform(number, relation)

        self.assertTrue(len(most) <= len(result))

        if config.strip and number != []:
            self.assertTrue(result[-1] != 0)


class TestString(unittest.TestCase):
    """
    Test operation of String class.
    """

    def testExceptions(self):
        """
        Verify that exceptions are properly thrown.
        """
        xformer = String(DisplayConfig(), 2)
        with self.assertRaises(BaseDisplayError):
            xformer.xform(-1, [0, 2], [], [], 0)
        with self.assertRaises(BaseDisplayError):
            xformer.xform(-1, [], [0, 2], [], 0)
        with self.assertRaises(BaseDisplayError):
            xformer.xform(-1, [], [], [0, 2], 0)

    @given(
       build_sign(),
       build_base(Digits.MAX_SIZE_BASE_FOR_CHARS),
       build_relation(),
       strategies.data()
    )
    def testXform(self, sign, base, relation, data):
        """
        Test that xform runs. Other tests check functionality.
        """
        length = 32

        config = DisplayConfig()
        integer_part = data.draw(build_nat(base, length))
        non_repeating_part = data.draw(build_nat(base, length))
        repeating_part = data.draw(build_nat(base, length))

        result = String(config, base).xform(
           sign,
           integer_part,
           non_repeating_part,
           repeating_part,
           relation
        )

        self.assertIsNotNone(result)
