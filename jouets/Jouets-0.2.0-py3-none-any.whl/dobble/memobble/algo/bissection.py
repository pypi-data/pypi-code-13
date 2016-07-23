# Copyright 2014-2015 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Génération d'un sous-jeu de base, en utilisant une bissection de l'ensemble des cartes.
"""

import itertools

from jouets.dobble import Carte
from jouets.dobble.memobble import Jeu
from jouets.dobble.memobble import errors
from jouets.dobble.memobble.mmath import est_pair

def genere(num):
    """Genère un sous-jeu, en utilisant l'algorithme 1.

    """
    if not est_pair(num):
        raise errors.TailleNonGeree("Argument '{}' must be even.".format(num))
    if num <= 2:
        raise errors.TailleNonGeree("Argument '{}' must be greater than 2.".format(num))
    symboles = itertools.count()
    cartes1 = [Carte() for i in range(num//2)]
    cartes2 = [Carte() for i in range(num//2)]
    for i in cartes1:
        for j in cartes2:
            symbole = next(symboles)
            i.symboles.append(symbole)
            j.symboles.append(symbole)
    return Jeu(cartes1 + cartes2)


ALGO = {
    'bissection': {
        'genere': genere,
        'default': {
            'num': 6,
            'sub': 4,
            }
        }
    }
