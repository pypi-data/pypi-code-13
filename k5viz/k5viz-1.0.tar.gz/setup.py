from setuptools import setup
setup(
  name = 'k5viz',
  packages = ['k5viz'],
  version = '1.0',
  description = 'k5viz is a simple application that can read in a k5 file or JSON graph file and visualize the Deep Learning neural network for you',
  author = 'sio2boss',
  author_email = 'sio2boss@hotmail.com',
  url = 'https://github.com/sio2boss/k5viz',
  download_url = 'https://github.com/sio2boss/k5viz/tarball/1.0',
  keywords = ['k5', 'visualization', 'visualize', 'deep learning', 'neural network'],
  classifiers = [],
  entry_points = {
    "console_scripts": ['k5viz = k5viz:main']
  },
  install_requires=[
    "graphviz",
    "docopt",
    "h5py",
    "numpy",
  ],
)
