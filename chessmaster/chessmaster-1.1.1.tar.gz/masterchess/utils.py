# coding: utf-8
from collections import deque


def places_rotation(base_places):
    """
    This method rotates the places in the board to increase the range of
    possibilities while attempting to put the pieces in the board
    """

    rotate = []

    itens = deque(base_places)
    for item in base_places:
        rotate.append(list(itens))
        itens.rotate(-1)

    return rotate


def pretty_print(matrix):
    """
    Print a matrix in a pretty print format:

    Atributes:

    matrix -- convensional x, y 2D list
    input ex:
        [
            ['pawn', None, None],
            [None, None, 'king'],
            [None, None, None]
        ]
    output ex:
        None    king    None
        None    None    None
        pawn    None    None
    """

    return '\r\n'.join(
        ['\t'.join([str(x) for x in i]) for i in zip(*matrix)][::-1]
    )
