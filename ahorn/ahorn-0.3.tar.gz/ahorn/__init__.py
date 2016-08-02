"""
Ahorn
===================

A game description framework and game playing AI library,
written entirely in Python.

Quickstart
==========
    import ahorn, ahorn.Actors, ahorn.TicTacToe
    player_a, player_b = ahorn.Actors.MCTSPlayer(), ahorn.Actors.MCTSPlayer()
    starting_state = ahorn.TicTacToe.TicTacToeState([player_a, player_b])
    controller = ahorn.Controller(starting_state, verbose=True)
    controller.play()

Installation
============
    pip3 install -r requirements.txt
    python3 setup.py install
    python3 run.py  # should start playing a game

Running the tests
=================
    python3 -m pytest tests

Adding a new game
=================

A game is described by states and actions.
To describe a new game, subclass ahorn.GameBase.State and ahorn.GameBase.Action.
Take a look at the example: ahorn.TicTacToe.

Adding new AI
=============

Ahorn comes with a generic AI based on the Monte Carlo Tree Search algorithm:
 ahorn.Actors.MCTSPlayer.
To create a new AI, subclass ahorn.GameBase.Player. Take a look at the
example: ahorn.Actors.RandomPlayer.

"""
from .Controller import Controller
