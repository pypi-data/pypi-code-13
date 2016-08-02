from ahorn import Controller
from ahorn.TicTacToe import TTTState
from ahorn.Actors import RandomPlayer


if __name__ == "__main__":
    players = [RandomPlayer(), RandomPlayer()]
    initial_state = TTTState(players)
    controller = Controller(initial_state, verbose=True)
    end_state = controller.play()
