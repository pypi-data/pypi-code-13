from .Actor import Actor
import abc

class Player(Actor, metaclass=abc.ABCMeta):
    """A player is an actor that actively decides which action to take"""
    pass
