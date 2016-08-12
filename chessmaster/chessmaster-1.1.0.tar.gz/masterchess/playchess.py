# coding: utf-8
import argparse
import logging
import logging.config

from masterchess import chess

logger = logging.getLogger(__name__)

LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'masterchess': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

logging.config.dictConfig(LOGGING)


def voala(board_size, pieces, reverse=False, show_threatening=False):
    board = chess.Board(board_size)
    board_places = sorted(board.places, reverse=reverse)

    for piece_master in pieces:
        for place_master in board_places:
            piece_master.set_position(place_master)
            board.place_piece(piece_master)
            for piece in pieces:
                if piece.__hash__() == piece_master.__hash__():
                    continue
                for place in board_places:
                    try:
                        piece.set_position(place)
                        board.place_piece(piece)
                        break
                    except:
                        continue
            if len(board.pieces) == len(pieces):
                if show_threatening:
                    yield(board.picture_threat(pretty_print=True))
                else:
                    yield(board.picture(pretty_print=True))
            board.remove_pieces()

def run(board_size, pieces, show_threatening=False):

    logger.info('Playing Chess')
    logger.info('Board size: %d' % board_size)
    logger.info('Pieces of bishops: %s' % len(
        [piece for piece in pieces if str(piece) == 'bishop']))
    logger.info('Pieces of kinights: %s' % len(
        [piece for piece in pieces if str(piece) == 'kinight']))
    logger.info('Pieces of kings: %s' % len(
        [piece for piece in pieces if str(piece) == 'king']))
    logger.info('Pieces of pawns: %s' % len(
        [piece for piece in pieces if str(piece) == 'pawn']))
    logger.info('Pieces of queens: %s' % len(
        [piece for piece in pieces if str(piece) == 'queen']))
    logger.info('Pieces of rooks: %s' % len(
        [piece for piece in pieces if str(piece) == 'rook']))

    games = [i for i in voala(board_size, pieces, reverse=False, show_threatening=show_threatening)]
    games += [i for i in voala(board_size, pieces, reverse=True, show_threatening=show_threatening)]
    games = set(games)
    print('Number of possibilities: %s' % len(games))
    for ndx, game in enumerate(games):
        print('')
        print('Game %d:' % (ndx+1))
        print(game)

def main():

    parser = argparse.ArgumentParser(
        description='Build a chess board with pieces which will not threatening one to another.'
    )

    parser.add_argument(
        '--board_size',
        '-s',
        default=3,
        type=int,
        help='Number of squares in the board'
    )

    parser.add_argument(
        '--bishops',
        '-b',
        default=0,
        type=int,
        help='Number of bishops'
    )

    parser.add_argument(
        '--kinights',
        '-i',
        default=0,
        type=int,
        help='Number of kinights'
    )

    parser.add_argument(
        '--kings',
        '-k',
        default=0,
        type=int,
        help='Number of kings'
    )

    parser.add_argument(
        '--pawns',
        '-p',
        default=0,
        type=int,
        help='Number of pawns'
    )

    parser.add_argument(
        '--queens',
        '-q',
        default=0,
        type=int,
        help='Number of Queens'
    )

    parser.add_argument(
        '--rooks',
        '-r',
        default=0,
        type=int,
        help='Number of rooks'
    )

    parser.add_argument(
        '--show_threatening',
        '-t',
        action="store_true",
        help='Show threatening places display T in the board when printing the results, otherwise None will be displayed'
    )
    args = parser.parse_args()

    pieces = []
    pieces += [chess.Bishop() for x in range(args.bishops)]
    pieces += [chess.Kinight() for x in range(args.kinights)]
    pieces += [chess.King() for x in range(args.kings)]
    pieces += [chess.Pawn() for x in range(args.pawns)]
    pieces += [chess.Queen() for x in range(args.queens)]
    pieces += [chess.Rook() for x in range(args.rooks)]

    if len(pieces) <= 1:
        logger.error('You must select at least 2 pieces')
        exit()

    run(args.board_size, pieces, show_threatening=args.show_threatening)
