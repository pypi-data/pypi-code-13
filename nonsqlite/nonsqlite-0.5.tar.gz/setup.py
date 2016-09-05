from setuptools import setup

setup(name='nonsqlite',
      version='0.5',
      description='Non SQL Database',
      url='https://github.com/emilianobilli/nonsqlite',
      author='Emiliano Billi',
      author_email='emiliano.billi@gmail.com',
      license='GPL',
      packages=['nonsqlite'],
      install_requires=[
          'sqlite3',
      ],
      zip_safe=False)