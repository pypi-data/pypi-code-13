import unittest

from masterchess import chess


class TestsChessMasterPiece(unittest.TestCase):

    def test_instanciation_piece(self):

        pawn = chess.Pawn()

        expected = (0, 0)

        self.assertEqual(pawn.position, expected)

    def test_instanciation_preset_position(self):

        pawn = chess.Pawn((1, 1))

        expected = (1, 1)

        self.assertEqual(pawn.position, expected)

    def test_set_position(self):

        pawn = chess.Pawn()

        pawn.set_position((1, 2))

        expected = (1, 2)

        self.assertEqual(pawn.position, expected)

    def test_set_invalid_position_1(self):

        pawn = chess.Pawn()

        with self.assertRaises(ValueError):
            pawn.set_position((-1, 2))

    def test_set_invalid_position_2(self):

        pawn = chess.Pawn()

        with self.assertRaises(ValueError):
            pawn.set_position((1, -2))

    def test_set_invalid_position_3(self):

        pawn = chess.Pawn()

        with self.assertRaises(ValueError):
            pawn.set_position((-1, -2))

    def test_set_invalid_position_4(self):

        pawn = chess.Pawn()

        with self.assertRaises(ValueError):
            pawn.set_position(('a', 2))

    def test_set_invalid_position_5(self):

        pawn = chess.Pawn()

        with self.assertRaises(ValueError):
            pawn.set_position((1, 'a'))

    def test_set_invalid_position_6(self):

        pawn = chess.Pawn()

        with self.assertRaises(ValueError):
            pawn.set_position(('a', 'a'))

    def test_set_invalid_position_7(self):

        pawn = chess.Pawn()

        with self.assertRaises(ValueError):
            pawn.set_position((1, ))

    def test_set_invalid_position_8(self):

        pawn = chess.Pawn()

        with self.assertRaises(ValueError):
            pawn.set_position((1, 2, 4,))

    def test_pawn_threatening_zone(self):
        """
        Testing pawn when the piece is able to threatening other piece in both
        sides.
        """

        pawn = chess.Pawn((4, 0))

        expected = [
            (3, 1),
            (5, 1)
        ]

        self.assertEqual(
            sorted(pawn.threatening_zone(8)), sorted(expected)
        )

    def test_pawn_threatening_x_boundary_left(self):
        """
        Testing boundary where the pawn can not move to the left
        """

        pawn = chess.Pawn((0, 0))

        expected = [
            (1, 1)
        ]

        self.assertEqual(
            sorted(pawn.threatening_zone(8)), sorted(expected)
        )

    def test_pawn_threatening_x_boundary_right(self):
        """
        Testing boundary where the pawn can not move to the right
        """

        pawn = chess.Pawn((7, 0))

        expected = [
            (6, 1)
        ]

        self.assertEqual(
            sorted(pawn.threatening_zone(8)), sorted(expected)
        )

    def test_pawn_threatening_zone_y_boundary(self):
        """
        Testing boundary where the pawn can not move forward
        """

        pawn = chess.Pawn((4, 7))

        expected = []

        self.assertEqual(
            sorted(pawn.threatening_zone(8)), sorted(expected)
        )

    def test_pawn_threatening_zone_y_boundary_last_move(self):
        """
        Testing boundary where the pawn can make your last move forward
        """

        pawn = chess.Pawn((4, 6))

        expected = [
            (3, 7),
            (5, 7)
        ]

        self.assertEqual(
            sorted(pawn.threatening_zone(8)), sorted(expected)
        )

    def test_w_positions(self):

        piece = chess.Pieces((3, 4))

        expected = [
            (2, 4),
            (1, 4),
            (0, 4)
        ]

        self.assertEqual(
            sorted(piece._w_positions(8)), sorted(expected)
        )

    def test_e_positions(self):

        piece = chess.Pieces((3, 4))

        expected = [
            (4, 4),
            (5, 4),
            (6, 4),
            (7, 4)
        ]

        self.assertEqual(
            sorted(piece._e_positions(8)), sorted(expected)
        )

    def test_n_positions(self):

        piece = chess.Pieces((3, 4))

        expected = [
            (3, 5),
            (3, 6),
            (3, 7)
        ]

        self.assertEqual(
            sorted(piece._n_positions(8)), sorted(expected)
        )

    def test_s_positions(self):

        piece = chess.Pieces((3, 4))

        expected = [
            (3, 3),
            (3, 2),
            (3, 1),
            (3, 0),
        ]

        self.assertEqual(
            sorted(piece._s_positions(8)), sorted(expected)
        )

    def test_se_positions(self):

        piece = chess.Pieces((3, 4))

        expected = [
            (4, 3),
            (5, 2),
            (6, 1),
            (7, 0),
        ]

        self.assertEqual(
            sorted(piece._se_positions(8)), sorted(expected)
        )

    def test_ne_positions(self):

        piece = chess.Pieces((3, 4))

        expected = [
            (4, 5),
            (5, 6),
            (6, 7)
        ]

        self.assertEqual(
            sorted(piece._ne_positions(8)), sorted(expected)
        )

    def test_nw_positions(self):

        piece = chess.Pieces((3, 4))

        expected = [
            (2, 5),
            (1, 6),
            (0, 7)
        ]

        self.assertEqual(
            sorted(piece._nw_positions(8)), sorted(expected)
        )

    def test_sw_positions(self):

        piece = chess.Pieces((3, 4))

        expected = [
            (2, 3),
            (1, 2),
            (0, 1)
        ]

        self.assertEqual(
            sorted(piece._sw_positions(8)), sorted(expected)
        )

    def test_bishop_threatening_zone(self):
        """
        Testing gather the bishop allowed moves
        """

        bishop = chess.Bishop((3, 4))

        expected = [
            (0, 1),
            (0, 7),
            (1, 2),
            (1, 6),
            (2, 3),
            (2, 5),
            (4, 3),
            (4, 5),
            (5, 2),
            (5, 6),
            (6, 1),
            (6, 7),
            (7, 0)
        ]

        self.assertEqual(
            sorted(bishop.threatening_zone(8)), sorted(expected)
        )

    def test_rook_threatening_zone(self):
        """
        Testing gather the rook allowed moves
        """

        rook = chess.Rook((3, 4))

        expected = [
            (0, 4),
            (1, 4),
            (2, 4),
            (4, 4),
            (5, 4),
            (6, 4),
            (7, 4),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 5),
            (3, 6),
            (3, 7)
        ]

        self.assertEqual(
            sorted(rook.threatening_zone(8)), sorted(expected)
        )

    def test_queen_threatening_zone(self):
        """
        Testing gather the rook allowed moves
        """

        queen = chess.Queen((3, 4))

        expected = [
            (0, 4),
            (1, 4),
            (2, 4),
            (4, 4),
            (5, 4),
            (6, 4),
            (7, 4),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 5),
            (3, 6),
            (3, 7),
            (0, 1),
            (0, 7),
            (1, 2),
            (1, 6),
            (2, 3),
            (2, 5),
            (4, 3),
            (4, 5),
            (5, 2),
            (5, 6),
            (6, 1),
            (6, 7),
            (7, 0)
        ]

        self.assertEqual(
            sorted(queen.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone(self):
        """
        Testing gather the kinight allowed moves
        """

        kinight = chess.Kinight((3, 4))

        expected = [
            (2, 6),
            (4, 6),
            (1, 5),
            (5, 5),
            (1, 3),
            (5, 3),
            (2, 2),
            (4, 2)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_0_0(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((0, 0))

        expected = [
            (1, 2),
            (2, 1)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_1_0(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((1, 0))

        expected = [
            (0, 2),
            (2, 2),
            (3, 1),
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_2_0(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((2, 0))

        expected = [
            (1, 2),
            (3, 2),
            (0, 1),
            (4, 1)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_7_0(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((7, 0))

        expected = [
            (6, 2),
            (5, 1)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_6_0(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((6, 0))

        expected = [
            (5, 2),
            (7, 2),
            (4, 1)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_5_0(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((5, 0))

        expected = [
            (4, 2),
            (6, 2),
            (3, 1),
            (7, 1)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_0_1(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((0, 1))

        expected = [
            (1, 3),
            (2, 2),
            (2, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_1_1(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((1, 1))

        expected = [
            (0, 3),
            (2, 3),
            (3, 2),
            (3, 0),
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_2_1(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((2, 1))

        expected = [
            (1, 3),
            (3, 3),
            (0, 2),
            (4, 2),
            (0, 0),
            (4, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_7_1(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((7, 1))

        expected = [
            (6, 3),
            (5, 2),
            (5, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_6_1(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((6, 1))

        expected = [
            (5, 3),
            (7, 3),
            (4, 2),
            (4, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_5_1(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((5, 1))

        expected = [
            (4, 3),
            (6, 3),
            (3, 2),
            (7, 2),
            (3, 0),
            (7, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_0_2(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((0, 2))

        expected = [
            (1, 4),
            (2, 3),
            (2, 1),
            (1, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_1_2(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((1, 2))

        expected = [
            (0, 4),
            (2, 4),
            (3, 3),
            (3, 1),
            (2, 0),
            (0, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_2_2(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((2, 2))

        expected = [
            (1, 4),
            (3, 4),
            (0, 3),
            (4, 3),
            (0, 1),
            (4, 1),
            (1, 0),
            (3, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_7_2(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((7, 2))

        expected = [
            (6, 4),
            (5, 3),
            (5, 1),
            (6, 0),
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_6_2(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((6, 2))

        expected = [
            (5, 4),
            (7, 4),
            (4, 3),
            (4, 1),
            (5, 0),
            (7, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_5_2(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((5, 2))

        expected = [
            (4, 4),
            (6, 4),
            (3, 3),
            (7, 3),
            (3, 1),
            (7, 1),
            (4, 0),
            (6, 0)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_0_7(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((0, 7))

        expected = [
            (2, 6),
            (1, 5)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_1_7(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((1, 7))

        expected = [
            (3, 6),
            (0, 5),
            (2, 5)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_2_7(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((2, 7))

        expected = [
            (0, 6),
            (4, 6),
            (1, 5),
            (3, 5)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_7_7(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((7, 7))

        expected = [
            (5, 6),
            (6, 5)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_6_7(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((6, 7))

        expected = [
            (4, 6),
            (5, 5),
            (7, 5)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_5_7(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((5, 7))

        expected = [
            (3, 6),
            (7, 6),
            (4, 5),
            (6, 5)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_0_6(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((0, 6))

        expected = [
            (2, 7),
            (2, 5),
            (1, 4)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_1_6(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((1, 6))

        expected = [
            (3, 7),
            (3, 5),
            (0, 4),
            (2, 4)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_2_6(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((2, 6))

        expected = [
            (0, 7),
            (4, 7),
            (0, 5),
            (4, 5),
            (1, 4),
            (3, 4)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_7_6(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((7, 6))

        expected = [
            (5, 7),
            (5, 5),
            (6, 4)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_6_6(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((6, 6))

        expected = [
            (4, 7),
            (4, 5),
            (5, 4),
            (7, 4)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_5_6(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((5, 6))

        expected = [
            (3, 7),
            (7, 7),
            (3, 5),
            (7, 5),
            (4, 4),
            (6, 4)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_0_5(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((0, 5))

        expected = [
            (1, 7),
            (2, 6),
            (2, 4),
            (1, 3)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_1_5(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((1, 5))

        expected = [
            (0, 7),
            (2, 7),
            (3, 6),
            (3, 4),
            (0, 3),
            (2, 3)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_2_5(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((2, 5))

        expected = [
            (1, 7),
            (3, 7),
            (0, 6),
            (4, 6),
            (0, 4),
            (4, 4),
            (1, 3),
            (3, 3)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_7_5(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((7, 5))

        expected = [
            (6, 7),
            (5, 6),
            (5, 4),
            (6, 3)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_6_5(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((6, 5))

        expected = [
            (5, 7),
            (7, 7),
            (4, 6),
            (4, 4),
            (5, 3),
            (7, 3)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_kinight_threatening_zone_boundary_5_5(self):
        """
        Kinight Boundary Testing
        """

        kinight = chess.Kinight((5, 5))

        expected = [
            (4, 7),
            (6, 7),
            (3, 6),
            (7, 6),
            (3, 4),
            (7, 4),
            (4, 3),
            (6, 3)
        ]

        self.assertEqual(
            sorted(kinight.threatening_zone(8)), sorted(expected)
        )

    def test_king_threatening_zone(self):
        """
        Testing gather the king allowed moves
        """

        king = chess.King((3, 4))

        expected = [
            (2, 5),
            (3, 5),
            (4, 5),
            (2, 4),
            (4, 4),
            (2, 3),
            (3, 3),
            (4, 3)
        ]

        self.assertEqual(
            sorted(king.threatening_zone(8)), sorted(expected)
        )

    def test_king_threatening_zone_boundary_bottom(self):
        """
        Testing gather the king allowed moves
        """

        king = chess.King((3, 0))

        expected = [
            (2, 1),
            (3, 1),
            (4, 1),
            (2, 0),
            (4, 0)
        ]

        self.assertEqual(
            sorted(king.threatening_zone(8)), sorted(expected)
        )

    def test_king_threatening_zone_boundary_top(self):
        """
        Testing gather the king allowed moves
        """

        king = chess.King((3, 7))

        expected = [
            (2, 7),
            (4, 7),
            (2, 6),
            (3, 6),
            (4, 6)
        ]

        self.assertEqual(
            sorted(king.threatening_zone(8)), sorted(expected)
        )

    def test_king_threatening_zone_boundary_top_left(self):
        """
        Testing gather the king allowed moves
        """

        king = chess.King((0, 7))

        expected = [
            (1, 7),
            (0, 6),
            (1, 6)
        ]

        self.assertEqual(
            sorted(king.threatening_zone(8)), sorted(expected)
        )

    def test_king_threatening_zone_boundary_top_right(self):
        """
        Testing gather the king allowed moves
        """

        king = chess.King((7, 7))

        expected = [
            (6, 7),
            (6, 6),
            (7, 6)
        ]

        self.assertEqual(
            sorted(king.threatening_zone(8)), sorted(expected)
        )

    def test_king_threatening_zone_boundary_bottom_left(self):
        """
        Testing gather the king allowed moves
        """

        king = chess.King((0, 0))

        expected = [
            (0, 1),
            (1, 1),
            (1, 0)
        ]

        self.assertEqual(
            sorted(king.threatening_zone(8)), sorted(expected)
        )

    def test_king_threatening_zone_boundary_bottom_right(self):
        """
        Testing gather the king allowed moves
        """

        king = chess.King((7, 0))

        expected = [
            (6, 0),
            (6, 1),
            (7, 1)
        ]

        self.assertEqual(
            sorted(king.threatening_zone(8)), sorted(expected)
        )


class TestsChessMasterBoard(unittest.TestCase):

    def test_place_1_piece(self):

        pawn = chess.Pawn()

        board = chess.Board(3)

        board.place_piece(pawn)

        expected = [
            ['pawn', None, None],
            [None, None, None],
            [None, None, None]
        ]

        self.assertEqual(board.picture(), expected)

    def test_place_2_pieces(self):

        pawn = chess.Pawn()
        king = chess.King((1, 2))

        board = chess.Board(3)

        board.place_piece(pawn)
        board.place_piece(king)

        expected = [
            ['pawn', None, None],
            [None, None, 'king'],
            [None, None, None]
        ]

        self.assertEqual(board.picture(), expected)

    def test_place_2_pieces(self):

        pawn = chess.Pawn()
        king = chess.King((1, 2))

        board = chess.Board(3)

        board.place_piece(pawn)
        board.place_piece(king)

        expected = [
            ['pawn', None, None],
            [None, None, 'king'],
            [None, None, None]
        ]

        self.assertEqual(board.picture(), expected)

    def test_replace_1_piece(self):
        """
        Chanfe the position of a piece in a different position if it is already
        in the table.
        """
        king = chess.King((1, 0))
        board = chess.Board(3)
        board.place_piece(king)

        expected = [
            [None, None, None],
            ['king', None, None],
            [None, None, None]
        ]

        self.assertEqual(board.picture(), expected)

        king.set_position((1, 1))
        board.place_piece(king)

        expected = [
            [None, None, None],
            [None, 'king', None],
            [None, None, None]
        ]

        self.assertEqual(board.picture(), expected)

    def test_replace_2_piece(self):
        """
        Change the position of a piece to a threatened position in different.
        """
        king1 = chess.King((1, 0))
        king2 = chess.King((1, 2))
        board = chess.Board(3)
        board.place_piece(king1)
        board.place_piece(king2)

        expected = [
            [None, None, None],
            ['king', None, 'king'],
            [None, None, None]
        ]

        # Creating table with 2 kings
        self.assertEqual(board.picture(), expected)

        # Moving king to a threatend area raises a Threatened execption
        king1.set_position((1, 1))
        with self.assertRaises(chess.Threatened):
            board.place_piece(king1)

        # Board is the same before moving attempt
        self.assertEqual(board.picture(), expected)

    def test_replace_3_piece(self):
        """
        Change the position of a piece to a available position.
        """
        king1 = chess.King((1, 0))
        king2 = chess.King((1, 2))
        board = chess.Board(3)
        board.place_piece(king1)
        board.place_piece(king2)

        expected = [
            [None, None, None],
            ['king', None, 'king'],
            [None, None, None]
        ]

        # Creating table with 2 kings
        self.assertEqual(board.picture(), expected)

        # Moving king to a threatend area raises a Threatened execption
        king1.set_position((0, 0))
        board.place_piece(king1)

        expected = [
            ['king', None, None],
            [None, None, 'king'],
            [None, None, None]
        ]

        self.assertEqual(board.picture(), expected)

    def test_picture_threat_1(self):

        board = chess.Board(8)
        king = chess.King((1, 2))
        board.place_piece(king)

        expected = [
            [None, 'T', 'T', 'T', None, None, None, None],
            [None, 'T', 'king', 'T', None, None, None, None],
            [None, 'T', 'T', 'T', None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]
        self.assertEqual(board.picture_threat(), expected)

    def test_picture_threat_2(self):

        board = chess.Board(4)
        king = chess.King((0, 3))
        board.place_piece(king)

        expected = [
            [None, None, 'T', 'king'],
            [None, None, 'T', 'T'],
            [None, None, None, None],
            [None, None, None, None]
        ]
        self.assertEqual(board.picture_threat(), expected)

    def test_picture_threat_3(self):

        board = chess.Board(8)
        queen = chess.Queen((4, 3))
        board.place_piece(queen)

        expected = [
            [None, None, None, 'T', None, None, None, 'T'],
            ['T', None, None, 'T', None, None, 'T', None],
            [None, 'T', None, 'T', None, 'T', None, None],
            [None, None, 'T', 'T', 'T', None, None, None],
            ['T', 'T', 'T', 'queen', 'T', 'T', 'T', 'T'],
            [None, None, 'T', 'T', 'T', None, None, None],
            [None, 'T', None, 'T', None, 'T', None, None],
            ['T', None, None, 'T', None, None, 'T', None]
        ]

        self.assertEqual(board.picture_threat(), expected)

    def test_picture_threat_4_with_2_pieces(self):

        board = chess.Board(8)
        queen = chess.Queen((4, 3))
        king = chess.King((1, 1))
        board.place_piece(queen)
        board.place_piece(king)

        expected = [
            ['T', 'T', 'T', 'T', None, None, None, 'T'],
            ['T', 'king', 'T', 'T', None, None, 'T', None],
            ['T', 'T', 'T', 'T', None, 'T', None, None],
            [None, None, 'T', 'T', 'T', None, None, None],
            ['T', 'T', 'T', 'queen', 'T', 'T', 'T', 'T'],
            [None, None, 'T', 'T', 'T', None, None, None],
            [None, 'T', None, 'T', None, 'T', None, None],
            ['T', None, None, 'T', None, None, 'T', None]
        ]

        self.assertEqual(board.picture_threat(), expected)

    def test_picture_threat_4_with_3_pieces(self):

        board = chess.Board(8)
        queen = chess.Queen((4, 3))
        king = chess.King((1, 1))
        kinight = chess.Kinight((7, 7))
        board.place_piece(queen)
        board.place_piece(king)
        board.place_piece(kinight)

        expected = [
            ['T', 'T', 'T', 'T', None, None, None, 'T'],
            ['T', 'king', 'T', 'T', None, None, 'T', None],
            ['T', 'T', 'T', 'T', None, 'T', None, None],
            [None, None, 'T', 'T', 'T', None, None, None],
            ['T', 'T', 'T', 'queen', 'T', 'T', 'T', 'T'],
            [None, None, 'T', 'T', 'T', None, 'T', None],
            [None, 'T', None, 'T', None, 'T', None, None],
            ['T', None, None, 'T', None, None, 'T', 'kinight']
        ]

        self.assertEqual(board.picture_threat(), expected)

    def test_put_piece_in_occupied_square(self):
        pawn1 = chess.Pawn((1, 2))
        pawn2 = chess.Pawn((1, 2))

        board = chess.Board(3)

        board.place_piece(pawn1)

        with self.assertRaises(chess.OccupiedSquare):
            board.place_piece(pawn2)

    def test_put_piece_in_threatened_square(self):
        """
        Test ThretenedException while trying to put a rook in an place
        threatened by a queen.
        [
            [None, None, None, 'T', None, None, None, 'T'],
            ['T (trying to put rook here)', None, None, 'T', None, None, 'T', None],
            [None, 'T', None, 'T', None, 'T', None, None],
            [None, None, 'T', 'T', 'T', None, None, None],
            ['T', 'T', 'T', 'queen', 'T', 'T', 'T', 'T'],
            [None, None, 'T', 'T', 'T', None, None, None],
            [None, 'T', None, 'T', None, 'T', None, None],
            ['T', None, None, 'T', None, None, 'T', None]
        ]

        """

        board = chess.Board(8)
        queen = chess.Queen((4, 3))
        board.place_piece(queen)

        with self.assertRaises(chess.Threatened):
            rook = chess.Rook((1, 0))
            board.place_piece(rook)

    def test_put_piece_in_threatening_square(self):
        """
        Test ThreteningException while trying to put a kinight in an place that
        will threatening queen.
        [
            [None, None, None, 'T', None, None, None, 'T'],
            ['T', None, None, 'T', None, None, 'T', None],
            [None, 'T', None (trying to put kinight here), 'T', None, 'T', None, None],
            [None, None, 'T', 'T', 'T', None, None, None],
            ['T', 'T', 'T', 'queen', 'T', 'T', 'T', 'T'],
            [None, None, 'T', 'T', 'T', None, None, None],
            [None, 'T', None, 'T', None, 'T', None, None],
            ['T', None, None, 'T', None, None, 'T', None]
        ]

        """

        board = chess.Board(8)
        queen = chess.Queen((4, 3))
        board.place_piece(queen)

        with self.assertRaises(chess.Threatening):
            kinight = chess.Kinight((2, 2))
            board.place_piece(kinight)

    def test_instanciating_board_wrong_size(self):

        with self.assertRaises(ValueError):
            board = chess.Board('wrong size')

    def test_instanciating_board_size_3(self):

        board = chess.Board(3)

        expected = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

        self.assertEqual(board.picture(), expected)

    def test_instanciating_board_size_7(self):

        board = chess.Board(7)

        expected = [
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None]
        ]

        self.assertEqual(board.picture(), expected)

if __name__ == '__main__':
    unittest.main()
