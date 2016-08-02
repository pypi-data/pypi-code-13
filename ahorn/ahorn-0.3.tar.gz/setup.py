from distutils.core import setup

setup(
  name = 'ahorn',
  packages = ['ahorn', 'ahorn.Actors', 'ahorn.GameBase', 'ahorn.TicTacToe'],
  version = '0.3',
  description = 'A game playing and game AI library',
  author = 'Dries Wijns',
  author_email = 'dries.wijns@gmail.com',
  url = 'https://github.com/drieswijns/ahorn',
  download_url = 'https://github.com/drieswijns/ahorn/tarball/master',
  keywords = ['game', 'playing', 'AI', 'MCTS'],
  classifiers = [],
  package_data={"ahorn": ["ahorn/*"]},
)
