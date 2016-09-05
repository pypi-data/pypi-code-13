from distutils.core import setup

import apather_do as ad

setup(
    name='fwpt_apatcher',
    version=ad.__version__,
    packages=[''],
    install_requires=[
        "pymorphy2",
        "docx"
    ],
    url='',
    license='MIT',
    author='alex1ops',
    author_email='ale51098223@yandex.ru',
    description='Программа формирования template и сопроводительной документации для патчей '
)
