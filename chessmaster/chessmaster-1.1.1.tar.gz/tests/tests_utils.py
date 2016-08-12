# coding: utf-8

import unittest

from masterchess import utils


class TestsUtils(unittest.TestCase):

    def test_board_rotate(self):

        data = utils.places_rotation([(0, 0), (0, 1), (0, 2), (0, 3)])

        expected = [
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 1), (0, 2), (0, 3), (0, 0)],
            [(0, 2), (0, 3), (0, 0), (0, 1)],
            [(0, 3), (0, 0), (0, 1), (0, 2)]
        ]

        self.assertEqual(data, expected)

    def test_pretty_print_matrix_1(self):

        data = [
            ['pawn', None, None],
            [None, None, 'king'],
            [None, None, None]
        ]

        expected = 'None\tking\tNone\r\nNone\tNone\tNone\r\npawn\tNone\tNone'

        self.assertEqual(utils.pretty_print(data), expected)

    def test_pretty_print_matrix_2(self):

        data = [
            ['pawn', None, None, None],
            [None, None, 'king', None],
            [None, None, None, 'kinight'],
            ['Queen', None, None, None]
        ]

        expected = 'None\tNone\tkinight\tNone\r\nNone\tking\tNone\tNone\r\nNone\tNone\tNone\tNone\r\npawn\tNone\tNone\tQueen'

        self.assertEqual(utils.pretty_print(data), expected)
