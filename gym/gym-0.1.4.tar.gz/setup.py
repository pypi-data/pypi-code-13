from setuptools import setup, find_packages
import sys, os.path

# Don't import gym module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gym'))
from version import VERSION

setup(name='gym',
      version=VERSION,
      description='The OpenAI Gym: A toolkit for developing and comparing your reinforcement learning agents.',
      url='https://github.com/openai/gym',
      author='OpenAI',
      author_email='gym@openai.com',
      license='',
      packages=[package for package in find_packages()
                if package.startswith('gym')],
      zip_safe=False,
      install_requires=[
          'numpy>=1.10.4', 'requests>=2.0', 'six', 'pyglet>=1.2.0',
      ],
      extras_require={
          'all': ['atari_py>=0.0.17', 'Pillow', 'PyOpenGL',
                  'pachi-py>=0.0.19',
                  'box2d-py',
                  'doom_py>=0.0.11',
                  'mujoco_py>=0.4.3', 'imageio',
                  'keras', 'theano'],

          # Environment-specific dependencies. Keep these in sync with
          # 'all'!
          'atari': ['atari_py>=0.0.17', 'Pillow', 'PyOpenGL'],
          'board_game' : ['pachi-py>=0.0.19'],
          'box2d': ['box2d-py'],
          'classic_control': ['PyOpenGL'],
          'doom': ['doom_py>=0.0.11'],
          'mujoco': ['mujoco_py>=0.4.3', 'imageio'],
          'parameter_tuning': ['keras', 'theano'],
      },
      package_data={'gym': ['envs/mujoco/assets/*.xml', 'envs/classic_control/assets/*.png', 'envs/doom/assets/*.cfg']},
      tests_require=['nose2', 'mock'],
)
