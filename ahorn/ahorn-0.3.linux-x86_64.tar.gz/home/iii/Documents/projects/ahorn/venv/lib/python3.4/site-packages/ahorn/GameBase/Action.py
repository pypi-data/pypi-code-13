import abc

class Action(metaclass=abc.ABCMeta):
    """An action modifies one game state into the other.

    Parameters
    ----------

    Returns
    -------"""
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self, state):
        """Perform the action on a given state

        Parameters
        ----------
        State:
            The state that must be modified

        Returns
        -------
        State:
            The modified state
        """
        pass

    @abc.abstractmethod
    def __str__(self):
        """A string representation of this action.

        Parameters
        ----------

        Returns
        -------
        str
            String representation of this action."""
        pass

    def __hash__(self):
        """Get a hash of the current action.

        Parameters
        ----------

        Returns
        -------
        int
            The hash of the action"""
        return hash(str(self))
