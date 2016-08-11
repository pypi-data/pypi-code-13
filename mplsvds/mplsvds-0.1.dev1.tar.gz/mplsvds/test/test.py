# -*- coding: utf-8 -*-

import unittest

import mplsvds


class Tests(unittest.TestCase):

    def test_oranges(self):
        self.assertEqual(len(mplsvds.oranges), 4)


if __name__ == '__main__':
    unittest.main()
