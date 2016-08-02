from . import RandomActor
from ..GameBase import Player

class RandomPlayer(RandomActor, Player):
    """A player who takes a random action from the list of legal actions."""
    pass
    def __str__(self):
        return "RandomPlayer"
