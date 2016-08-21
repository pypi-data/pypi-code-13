"""main installation setup file"""

from setuptools import setup

setup(name='YoutubetoMp3',
      description='Download Youtube Videos to Mp3 using Command Line',
      version='1.0.0',
      author='Pratik Patel',
      author_email='pratikpatel15133@gmail.com',
      packages=['YoutubetoMp3'],
      entry_points={
          'console_scripts': ['YoutubetoMp3=YoutubetoMp3:main'],
      },
      url='https://github.com/Pratik151/YoutubetoMp3/',
      keywords=['Youtube', 'Mp3', 'Videos'],
      classifiers=[
          'Operating System :: POSIX',
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
