from setuptools import setup

setup(
    name = 'stra',
    version = '0.0.1',
    author = 'toastedcornflakes',
    author_email = 'toastedcornflakes@gmail.com',
    description = 'Annotates the output of running a command with the name of the corresponding stream',
    license = 'BSD',
    url = 'https://github.com/toastedcornflakes/STReam-Annotate',

    packages=['stra'],
    entry_points={
        'console_scripts': [
            'stra=stra:entrypoint'
    ]}
)
