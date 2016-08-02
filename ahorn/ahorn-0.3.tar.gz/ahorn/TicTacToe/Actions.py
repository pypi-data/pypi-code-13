from ..GameBase import Action as BaseAction


class TicTacToeAction(BaseAction):
    """In Tac-Tac-Toe the only action is puttin an O or an X in a free space

    Parameters
    ----------
        symbol: str
            Either "X" or "O"
        where: (int, int)
            A tuple with row and column index

    Returns
    -------"""
    def __init__(self, symbol, where):
        self.symbol = symbol
        self.where = where

    def execute(self, state):
        """Execute the action.

        Modifies the board of the state, and the current player index.

        Parameters
        ----------
        state: TTTState
            The state which to modify

        Returns
        -------"""
        (r, c) = self.where
        state.board[r][c] = self.symbol
        state.pi = (state.pi+1) % 2
        return state

    def __str__(self):
        """A string representation of this action.

        For example: "Put a X in position 1, 2"

        Parameters
        ----------

        Returns
        -------
        str
            String representation of this action."""
        return "Put a {} in position {}".format(self.symbol, self.where)
