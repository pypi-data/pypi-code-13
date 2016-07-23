# Copyright 2016 Louis Paternault
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

"""Calcule la probabilité de victoire des innocents dans le jeu mafia."""

from math import sqrt
import sys

from jouets import mafia
from jouets.utils.aargparse import analyseur, type_naturel

def analyse():
    """Renvoie un analyseur de ligne de commande."""
    parser = analyseur(mafia.VERSION, prog="mafia")

    parser.add_argument(
        '-m', '--mafiosi',
        type=type_naturel, default=None,
        help='Number of mafiosi.'
        )
    parser.add_argument(
        '-d', '--detectives',
        type=type_naturel, default=1,
        help='Number of detectives'
        )
    parser.add_argument(
        '-p', '--players',
        type=type_naturel,
        help='Total number of players.',
        required=True,
        )

    return parser

def main():
    """Fonction principale, appelée depuis la ligne de commande."""
    arguments = analyse().parse_args()
    if arguments.mafiosi is None:
        arguments.mafiosi = int(sqrt(float(arguments.players)))

    sys.setrecursionlimit(
        sys.getrecursionlimit() + 4 * arguments.players
    )

    print(mafia.proba_soir(
        arguments.mafiosi,
        arguments.players - arguments.mafiosi - arguments.detectives,
        arguments.detectives,
        ))

if __name__ == "__main__":
    main()
