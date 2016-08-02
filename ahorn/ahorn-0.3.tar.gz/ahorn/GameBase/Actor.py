import abc

class Actor(metaclass=abc.ABCMeta):
    """An actor performs actions and drives a game from state to state.

    Parameters
    ----------

    Returns
    -------
    """
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_action(self, state):
        """Return the action the actor wants to take in a given state.

        Parameters
        ----------
        State:
            The state in which the actor must perform an action

        Returns
        -------
        action: Action
            The action the actor wants to take in this state."""
        pass

    @abc.abstractmethod
    def __str__(self):
        """A name for this actor

        Parameters
        ----------

        Returns
        -------
        name: str
            The name for this actor."""
        pass
